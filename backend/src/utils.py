import base64
import json
import random
import re
from collections import OrderedDict
from copy import deepcopy
from enum import Enum
from io import BytesIO
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import numpy as np
import pandas as pd
import tiktoken
from _datetime import datetime, timedelta
from PIL import Image
from transactions.models import Transaction
from transactions.schemas import (
    GetTagStatisticTransactionSchema,
    GetTransactionLatencyStatisticsSchema,
    GetTransactionStatusStatisticsSchema,
    GetTransactionUsageStatisticsSchema,
    StatisticTransactionSchema,
    TagStatisticTransactionSchema,
)


def serialize_data(obj):
    obj["_id"] = obj["id"]
    del obj["id"]
    return obj


def deserialize_data(obj):
    obj["id"] = obj["_id"]
    del obj["_id"]
    return obj


def extract_tags_from_url(url_str: str) -> tuple[str, dict[str, str]]:
    """
    Extract tags and relevant information from the provided URL.

    :param url_str: The URL string to extract tags from.
    :return: A tuple containing the modified URL (scheme + netloc) and a dictionary with extracted information.
             The dictionary includes 'model', 'experiment', and 'tags'.
    """
    parsed_url = urlparse(url_str)
    query_params = parse_qs(parsed_url.query)
    model = str(query_params.get("model", [""])[0])
    experiment = str(query_params.get("experiment", [""])[0])
    tags = query_params.get("tags", [""])
    tags = tags[0].split(",") if tags else []
    result_dict = {"model": model, "experiment": experiment, "tags": tags}
    return parsed_url.scheme + "://" + parsed_url.netloc, result_dict


def detect_subdomain(host, base_url) -> str | None:
    """
    Detect and extract the subdomain from the given host and base URL.

    :param host: The host obtained from `request.headers.get("host")`, e.g., mydomain.com:8000.
    :param base_url: The base URL from the configuration, e.g., https://mydomain.com or http://localhost:8000.
    :return: The extracted subdomain, if present; otherwise, returns None.
    """
    host = host.split(":")[0]
    base_name = base_url.split("://")[-1].split(":")[0]
    if host.endswith(base_name):
        subdomain = host.replace(base_name, "").split(".")[0]
        return subdomain or None
    return None


def create_transaction_query_from_filters(
    tags: list[str] | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    null_generation_speed: bool = True,
    status_codes: list[int] | None = None,
    providers: list[str] | None = None,
    models: list[str] | None = None,
) -> dict:
    """
    Create a MongoDB query dictionary based on specified filters for transactions.

    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param null_generation_speed: Optional. Flag to include transactions with null generation speed.
    :param status_codes: Optional. List of status codes of the transactions.
    :param providers: Optional. List of providers of the transactions.
    :param models: Optional. List of models of the transactions.
    :return: MongoDB query dictionary representing the specified filters.
    """
    query = {}
    or_conditions = []
    if project_id is not None:
        query["project_id"] = project_id
    if tags is not None:
        query["tags"] = {"$all": tags}
    if date_from is not None or date_to is not None:
        query["response_time"] = {}
    if date_from is not None:
        query["response_time"]["$gte"] = date_from
    if date_to is not None:
        query["response_time"]["$lte"] = date_to
    if not null_generation_speed:
        query["generation_speed"] = {"$ne": None}
    if status_codes is not None:
        for code in status_codes:
            if code % 100 == 0:
                or_conditions.append({"status_code": {"$gte": code, "$lt": code + 100}})
    if providers is not None:
        query["provider"] = {"$in": providers}
    if models is not None:
        query["model"] = {"$in": models}
    if or_conditions:
        query["$or"] = or_conditions
    return query


def create_transaction_list_query_from_filters(
    tags: list[str] | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    null_generation_speed: bool = True,
    status_codes: list[int] | None = None,
    provider_models: list[dict[str, list[str]]] = None,
) -> dict:
    """
    Create a MongoDB query dictionary based on specified filters for transactions.

    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param null_generation_speed: Optional. Flag to include transactions with null generation speed.
    :param status_codes: Optional. List of status codes of the transactions.
    :param provider_models: Optional. List of providers and models of the transactions.
    :return: MongoDB query dictionary representing the specified filters.
    """
    base_query = {}

    if project_id is not None:
        base_query["project_id"] = project_id

    if tags is not None:
        base_query["tags"] = {"$all": tags}

    if date_from is not None or date_to is not None:
        base_query["response_time"] = {}

    if date_from is not None:
        base_query["response_time"]["$gte"] = date_from

    if date_to is not None:
        base_query["response_time"]["$lte"] = date_to

    if not null_generation_speed:
        base_query["generation_speed"] = {"$ne": None}

    or_conditions = []

    if provider_models is not None:
        for provider, models in provider_models.items():
            provider_model_conditions = []
            if models:
                provider_model_conditions.append(
                    {"provider": provider, "model": {"$in": models}}
                )
            else:
                provider_model_conditions.append({"provider": provider})
            for code in status_codes or []:
                if code % 100 == 0:
                    condition = base_query.copy()
                    condition["$and"] = [
                        *provider_model_conditions,
                        {"status_code": {"$gte": code, "$lt": code + 100}},
                    ]
                    or_conditions.append(condition)
            if not status_codes:
                condition = base_query.copy()
                condition["$and"] = provider_model_conditions
                or_conditions.append(condition)
    else:
        for code in status_codes or []:
            if code % 100 == 0:
                condition = base_query.copy()
                condition["status_code"] = {"$gte": code, "$lt": code + 100}
                or_conditions.append(condition)

    if or_conditions:
        query = {"$or": or_conditions}
    else:
        query = base_query

    return query


def parse_headers_to_dict(headers: list[tuple[bytes]]) -> dict:
    """
    Parse a list of header tuples into a dictionary.

    :param headers: List of header tuples where each tuple consists of (name: bytes, value: bytes).
    :return: A dictionary representing the parsed headers with names as keys and values as decoded strings.
    """
    return {header[0].decode("utf8"): header[2].decode("utf8") for header in headers}


class TransactionParamsBuilder:
    library: str | None = None
    status_code: int | None = None
    model: str | None = None
    model_type: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    prompt: str | None = None
    os: str | None = None
    provider: str | None = None
    messages: list[dict[str, Any]] | str | None = None
    last_message: str | None = None
    error_message: str | None = None

    def add_library(self, library: str):
        self.library = library
        return self

    def add_status_code(self, status_code: int):
        self.status_code = status_code
        return self

    def add_model(self, model: str):
        self.model = model
        return self

    def add_type(self, model_type: str):
        self.model_type = model_type
        return self

    def add_prompt(self, prompt: str):
        self.prompt = prompt
        return self

    def add_input_tokens(self, input_tokens: int):
        self.input_tokens = input_tokens
        return self

    def add_output_tokens(self, output_tokens: int):
        self.output_tokens = output_tokens
        return self

    def add_os(self, os: str | None):
        self.os = os
        return self

    def add_provider(self, provider: str):
        self.provider = provider
        return self

    def add_messages(self, messages: list[dict[str, str]]):
        self.messages = messages
        return self

    def add_last_message(self, last_message: str | None):
        self.last_message = last_message
        return self

    def add_error_message(self, error_message: str):
        self.error_message = error_message
        return self

    def build(self):
        return {
            "library": self.library,
            "status_code": self.status_code,
            "model": self.model,
            "type": self.model_type,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "prompt": self.prompt,
            "os": self.os,
            "provider": self.provider,
            "messages": self.messages,
            "last_message": self.last_message,
            "error_message": self.error_message,
        }


class UnsupportedProviderError(Exception):
    """Exception raised for unsupported providers."""

    def __init__(self, url):
        self.message = f"Unsupported provider for URL: {url}"
        super().__init__(self.message)


class TransactionParamExtractor:
    def __init__(self, request, response, response_content) -> None:
        self.response_headers = parse_headers_to_dict(
            response.__dict__["headers"].__dict__["_list"]
        )
        self.request_headers = parse_headers_to_dict(
            request.__dict__["headers"].__dict__["_list"]
        )
        self.request_content = self._decode_request_content(request)
        self.request_content_updated = deepcopy(self.request_content)

        self.response = response
        self.response_content = response_content
        self.response_content_updated = deepcopy(response_content)
        self.url = str(getattr(request, "url", ""))
        self.pattern = self._detect_pattern(self.url)

    @staticmethod
    def _decode_request_content(request):
        try:
            return json.loads(request.__dict__["_content"].decode("utf8"))
        except UnicodeDecodeError:
            data = {}
            parts = request.__dict__["_content"].split(
                request.__dict__["_content"].split(b"\r\n")[0]
            )[:-1]

            if b"mask" not in request.__dict__["_content"]:
                photo_part = parts[-1]
                parts = parts[:-1]
            else:
                mask_part = parts[-1]
                photo_part = parts[-2]
                parts = parts[:-2]
                mask_bytes = mask_part.split(b"\r\n\r\n")[1]
                data["mask"] = base64.b64encode(mask_bytes).decode("utf-8")

            for part in parts:
                if part:
                    part = part.strip().split(b"; ")[1]
                    header, value = part.split(b"\r\n\r\n")
                    header = header.split(b"=")[1].replace(b'"', b"").decode("utf-8")
                    data[header] = value.decode("utf-8")

            photo_bytes = photo_part.split(b"\r\n\r\n")[1]
            data["image"] = base64.b64encode(photo_bytes).decode("utf-8")

            return data

    @staticmethod
    def _detect_pattern(url):
        patterns = {
            "Azure Embeddings": r".*openai\.azure\.com.*embeddings.*",
            "Azure Completions": r".*openai\.azure\.com.*completions.*",
            "Azure Images Generations": r".*openai\.azure\.com.*images\/generations.*",
            "Azure Images Variations": r".*openai\.azure\.com.*images\/variations.*",
            "Azure Images Edits": r".*openai\.azure\.com.*images\/edits.*",
            "OpenAI Chat Completions": r".*api\.openai\.com.*chat.*completions.*",
            "OpenAI Completions": r".*api\.openai\.com(?!.*chat).*\/completions.*",
            "OpenAI Embeddings": r".*api\.openai\.com.*embeddings.*",
            "OpenAI Images Variations": r".*api\.openai\.com.*images.*variations.*",
            "OpenAI Images Generations": r".*api\.openai\.com.*images.*generations.*",
            "OpenAI Images Edits": r".*api\.openai\.com.*images.*edits.*",
            "Groq": r".*api\.groq\.com.*\/openai\/v1\/chat\/completions",
            "Anthropic": r".*anthropic\.com.*",
            "VertexAI": r".*-aiplatform\.googleapis\.com/v1.*",
            "Ollama": r".*(host\.docker\.internal|localhost).*\/api\/generate",
            "Huggingface": r".*huggingface\.cloud.*",
        }

        for pattern_name, pattern_regex in patterns.items():
            if re.match(pattern_regex, url):
                print(pattern_regex)
                print(url)
                return pattern_name
        return "Unsupported"

    def _extract_from_azure_embeddings(self) -> dict:
        extracted = {
            "type": "embedding",
            "provider": "Azure OpenAI",
        }
        messages = []
        if isinstance(self.request_content["input"], list):
            prompt = (
                "["
                + ", ".join(map(lambda x: str(x), self.request_content["input"]))
                + "]"
            )
        else:
            prompt = self.request_content["input"]
        extracted["prompt"] = prompt
        messages.append({"role": "user", "content": prompt})

        if self.response.__dict__["status_code"] > 200:
            last_message = self.response_content["error"]["message"]
            extracted["error_message"] = last_message
            extracted["last_message"] = last_message
            messages.append({"role": "error", "content": last_message})
        else:
            extracted["model"] = self.response_content["model"]
            if isinstance(self.response_content["data"][0]["embedding"], list):
                last_message = (
                    "["
                    + ", ".join(
                        map(
                            lambda x: str(x),
                            self.response_content["data"][0]["embedding"],
                        )
                    )
                    + "]"
                )
            else:
                last_message = self.response_content["data"][0]["embedding"]
            extracted["last_message"] = last_message
            messages.append({"role": "system", "content": last_message})
        extracted["messages"] = messages

        return extracted

    def _extract_from_azure_completions(self) -> dict:
        for idx_message, message in enumerate(self.request_content["messages"]):
            if (
                message["role"] == "user"
                and not isinstance(message["content"], str)
                and len(message["content"]) > 1
            ):
                for idx_content, content in enumerate(message["content"]):
                    if content["type"] == "image_url":
                        self.request_content_updated["messages"][idx_message][
                            "content"
                        ][idx_content]["image_url"]["url"] = resize_b64_image(
                            content["image_url"]["url"].replace(
                                "data:image/png;base64,", ""
                            ),
                            (128, 128),
                        )

        extracted = {
            "type": "completions",
            "provider": "Azure OpenAI",
        }
        prompt = [
            message["content"]
            for message in self.request_content_updated["messages"]
            if message["role"] == "user"
        ][::-1][0]

        if len(prompt) == 2:
            prompt = [cont for cont in prompt if cont["type"] == "text"][0]["text"]

        extracted["prompt"] = (
            prompt if prompt else self.request_content_updated["messages"][0]["content"]
        )
        messages = self.request_content_updated["messages"]
        if self.response.__dict__["status_code"] > 200:
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content["error"]["message"]
                    if "error" in self.response_content.keys()
                    else self.response_content["message"],
                }
            )
            extracted["error_message"] = (
                self.response_content["error"]["message"]
                if "error" in self.response_content.keys()
                else self.response_content["message"]
            )
            extracted["last_message"] = (
                self.response_content["error"]["message"]
                if "error" in self.response_content.keys()
                else self.response_content["message"]
            )
        else:
            messages.append(self.response_content["choices"][0]["message"])
            extracted["model"] = self.response_content["model"]
            extracted["last_message"] = self.response_content["choices"][0]["message"][
                "content"
            ]
        extracted["messages"] = messages
        return extracted

    def _extract_from_azure_images_generations(self) -> dict:
        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        extracted = {
            "type": "images generations",
            "provider": "Azure OpenAI",
            "prompt": self.request_content_updated["prompt"],
            "model": model,
        }
        messages = [{"role": "user", "content": self.request_content_updated["prompt"]}]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_azure_images_variations(self) -> dict:
        self.request_content_updated["image"] = resize_b64_image(
            self.request_content_updated["image"], (128, 128)
        )

        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        extracted = {
            "type": "images variations",
            "provider": "Azure OpenAI",
            "prompt": self.request_content["image"],
            "model": model,
        }

        messages = [{"role": "user", "content": self.request_content_updated["image"]}]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_azure_images_edit(self) -> dict:
        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        self.request_content_updated["image"] = resize_b64_image(
            self.request_content_updated["image"], (128, 128)
        )
        self.request_content_updated["mask"] = resize_b64_image(
            self.request_content_updated["mask"], (128, 128)
        )
        extracted = {
            "type": "images edits",
            "provider": "Azure OpenAI",
            "prompt": self.request_content_updated["prompt"],
            "model": model,
        }
        messages = [
            {
                "role": "user",
                "content": self.request_content_updated["prompt"],
                "image": self.request_content_updated["image"],
                "mask": self.request_content_updated["mask"],
            }
        ]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_openai_chat_completions(self) -> dict:
        for idx_message, message in enumerate(self.request_content["messages"]):
            if (
                message["role"] == "user"
                and not isinstance(message["content"], str)
                and len(message["content"]) > 1
            ):
                for idx_content, content in enumerate(message["content"]):
                    if content["type"] == "image_url":
                        self.request_content_updated["messages"][idx_message][
                            "content"
                        ][idx_content]["image_url"]["url"] = resize_b64_image(
                            content["image_url"]["url"].replace(
                                "data:image/png;base64,", ""
                            ),
                            (128, 128),
                        )

        extracted = {
            "type": "chat completions",
            "provider": "OpenAI",
        }
        prompt = [
            message["content"]
            for message in self.request_content_updated["messages"]
            if message["role"] == "user"
        ][::-1][0]

        if len(prompt) == 2:
            prompt = [cont for cont in prompt if cont["type"] == "text"][0]["text"]

        extracted["prompt"] = (
            prompt if prompt else self.request_content_updated["messages"][0]["content"]
        )
        messages = self.request_content_updated["messages"]
        if self.response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
        else:
            messages.append(self.response_content["choices"][0]["message"])
            extracted["model"] = (
                self.response_headers["openai-model"]
                if "openai-model" in self.response_headers
                else self.response_content["model"]
            )
            extracted["last_message"] = self.response_content["choices"][0]["message"][
                "content"
            ]
        extracted["messages"] = messages
        return extracted

    def _extract_from_openai_completions(self) -> dict:
        extracted = {
            "type": "completions",
            "provider": "OpenAI",
            "prompt": self.request_content["prompt"],
        }
        messages = [{"role": "user", "content": self.request_content["prompt"]}]
        if self.response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
        else:
            messages.append(
                {
                    "role": "system",
                    "content": self.response_content["choices"][0]["text"],
                }
            )
            extracted["model"] = (
                self.response_headers["openai-model"]
                if "openai-model" in self.response_headers
                else self.response_content["model"]
            )
            extracted["last_message"] = self.response_content["choices"][0]["text"]
        extracted["messages"] = messages
        return extracted

    def _extract_from_openai_images_variations(self) -> dict:
        self.request_content_updated["image"] = resize_b64_image(
            self.request_content_updated["image"], (128, 128)
        )

        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        extracted = {
            "type": "images variations",
            "provider": "OpenAI",
            "prompt": self.request_content["image"],
            "model": model,
        }

        messages = [{"role": "user", "content": self.request_content_updated["image"]}]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_openai_images_generations(self) -> dict:
        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        extracted = {
            "type": "images generations",
            "provider": "OpenAI",
            "prompt": self.request_content_updated["prompt"],
            "model": model,
        }
        messages = [{"role": "user", "content": self.request_content_updated["prompt"]}]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_openai_images_edit(self) -> dict:
        model = []
        if "quality" in self.request_content_updated.keys():
            model.append(self.request_content_updated["quality"])
        if "size" in self.request_content_updated.keys():
            model.append(self.request_content_updated["size"])
        model.append(self.request_content_updated["model"])
        model = "/".join(model)

        self.request_content_updated["image"] = resize_b64_image(
            self.request_content_updated["image"], (128, 128)
        )
        self.request_content_updated["mask"] = resize_b64_image(
            self.request_content_updated["mask"], (128, 128)
        )
        extracted = {
            "type": "images edits",
            "provider": "OpenAI",
            "prompt": self.request_content_updated["prompt"],
            "model": model,
        }
        messages = [
            {
                "role": "user",
                "content": self.request_content_updated["prompt"],
                "image": self.request_content_updated["image"],
                "mask": self.request_content_updated["mask"],
            }
        ]
        if self.response.__dict__["status_code"] > 200:
            # possible TOFIX
            messages.append(
                {
                    "role": "error",
                    "content": self.response_content_updated["error"]["message"],
                }
            )
            extracted["error_message"] = self.response_content_updated["error"][
                "message"
            ]
            extracted["last_message"] = self.response_content_updated["error"][
                "message"
            ]
        else:
            try:
                for data in self.response_content_updated["data"]:
                    messages.append(
                        {
                            "role": "system",
                            "content": data["url"],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1][
                    "url"
                ]
            except KeyError:
                for idx, data in enumerate(self.response_content_updated["data"]):
                    self.response_content_updated["data"][idx] = resize_b64_image(
                        data["b64_json"], (128, 128)
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": self.response_content_updated["data"][idx],
                        }
                    )
                extracted["last_message"] = self.response_content_updated["data"][-1]
        extracted["messages"] = messages

        return extracted

    def _extract_from_openai_embeddings(self) -> dict:
        extracted = {"type": "embedding", "provider": "OpenAI"}
        messages = []
        if isinstance(self.request_content["input"], list):
            prompt = (
                "["
                + ", ".join(map(lambda x: str(x), self.request_content["input"]))
                + "]"
            )
        else:
            prompt = self.request_content["input"]
        messages.append({"role": "user", "content": prompt})
        extracted["prompt"] = prompt
        if self.response.__dict__["status_code"] > 200:
            last_message = self.response_content["error"]["message"]
            extracted["error_message"] = last_message
            extracted["last_message"] = last_message
            messages.append({"role": "error", "content": last_message})
        else:
            extracted["model"] = self.response_content["model"]
            if isinstance(self.response_content["data"][0]["embedding"], list):
                last_message = (
                    "["
                    + ", ".join(
                        map(
                            lambda x: str(x),
                            self.response_content["data"][0]["embedding"],
                        )
                    )
                    + "]"
                )
            else:
                last_message = self.response_content["data"][0]["embedding"]
            extracted["last_message"] = last_message
            messages.append({"role": "system", "content": last_message})
        extracted["messages"] = messages

        return extracted

    def _extract_from_anthropic(self) -> dict:
        extracted = {
            "type": "chat",
            "provider": "Anthropic",
            "prompt": self.request_content["messages"][0]["content"],
        }
        messages = self.request_content["messages"]

        if self.response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
        else:
            messages.append(
                {
                    "role": "assistant",
                    "content": self.response_content["content"][0]["text"],
                }
            )
            extracted["model"] = self.response_content["model"]
            extracted["last_message"] = self.response_content["content"][0]["text"]
            extracted["input_tokens"] = self.response_content["usage"].get(
                "input_tokens", 0
            )
            extracted["output_tokens"] = self.response_content["usage"].get(
                "output_tokens", 0
            )
        extracted["messages"] = messages
        return extracted

    def _extract_from_vertexai(self) -> dict:
        extracted = {
            "type": "chat",
            "provider": "Google VertexAI",
            "prompt": self.request_content["contents"][::-1][0]["parts"]["text"],
            "model": self.url.split("/")[-1].split(":")[0],
        }
        messages = [
            {"role": message["role"], "content": message["parts"]["text"]}
            for message in self.request_content["contents"]
        ]
        if self.response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
        else:
            messages.append(
                {
                    "role": self.response_content["candidates"][0]["content"]["role"],
                    "content": " ".join(
                        [
                            message["text"]
                            for message in self.response_content["candidates"][0][
                                "content"
                            ]["parts"]
                        ]
                    ),
                }
            )
            extracted["last_message"] = " ".join(
                [
                    part["text"]
                    for part in self.response_content["candidates"][0]["content"][
                        "parts"
                    ]
                ]
            )
            extracted["input_tokens"] = self.response_content["usageMetadata"].get(
                "promptTokenCount", 0
            )
            extracted["output_tokens"] = self.response_content["usageMetadata"].get(
                "candidatesTokenCount", 0
            )
        extracted["messages"] = messages
        return extracted

    def _extract_from_ollama(self) -> dict:
        extracted = {
            "type": "chat",
            "provider": "Ollama",
            "model": self.response_content["model"]
            if "model" in self.response_content
            else self.request_content["model"],
            "prompt": self.request_content["prompt"],
        }

        messages = [{"role": "user", "content": self.request_content["prompt"]}]

        if self.response.__dict__["status_code"] > 200:
            # TODO: Find the way to make error, then handle it
            print(self.response.__dict__)
        else:
            messages.append(
                {"role": "system", "content": self.response_content["response"]}
            )
            extracted["last_message"] = self.response_content["response"]
        extracted["messages"] = messages
        return extracted

    def _extract_from_groq(self) -> dict:
        extracted = {
            "type": "chat completion",
            "provider": "Groq",
            "prompt": self.request_content["messages"][-1]["content"],
            "model": self.request_content["model"],
            "input_tokens": self.response_content["usage"]["prompt_tokens"],
            "output_tokens": self.response_content["usage"]["completion_tokens"],
        }

        messages = self.request_content["messages"]

        if self.response.__dict__["status_code"] > 200:
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
        else:
            messages.append(
                {
                    "role": self.response_content["choices"][0]["message"]["role"],
                    "content": self.response_content["choices"][0]["message"][
                        "content"
                    ],
                }
            )
            extracted["last_message"] = self.response_content["choices"][0]["message"][
                "content"
            ]
        extracted["messages"] = messages

        return extracted

    def _extract_from_huggingface(self) -> dict:
        extracted = {
            "type": "chat",
            "provider": "Huggingface",
            "prompt": self.request_content["inputs"],
            "model": "Unknown",
        }

        messages = [{"role": "user", "content": self.request_content["inputs"]}]

        if self.response.__dict__["status_code"] > 200:
            extracted["error_message"] = self.response_content["error"]["message"]
            extracted["last_message"] = self.response_content["error"]["message"]
            messages.append(
                {"role": "error", "content": self.response_content["error"]["message"]}
            )
        else:
            extracted["last_message"] = self.response_content["generated_text"]
            messages.append(
                {"role": "system", "content": self.response_content["generated_text"]}
            )
        extracted["messages"] = messages

        return extracted

    def extract(self) -> dict:
        transaction_params = TransactionParamsBuilder()
        transaction_params.add_library(
            self.request_headers["user-agent"]
        ).add_status_code(self.response.__dict__["status_code"]).add_model(
            self.request_content.get("model", None)
        ).add_os(
            self.request_headers.get("x-stainless-os", None)
        )

        if "usage" in self.response_content:
            transaction_params.add_input_tokens(
                self.response_content["usage"].get("prompt_tokens", 0)
            )
            output_tokens = self.response_content["usage"].get("completion_tokens", 0)
            transaction_params.add_output_tokens(output_tokens)

        if self.pattern == "Azure Embeddings":
            extracted = self._extract_from_azure_embeddings()
        if self.pattern == "Azure Completions":
            extracted = self._extract_from_azure_completions()
        if self.pattern == "Azure Images Generations":
            extracted = self._extract_from_azure_images_generations()
        if self.pattern == "Azure Images Variations":
            extracted = self._extract_from_azure_images_variations()
        if self.pattern == "Azure Images Edits":
            extracted = self._extract_from_azure_images_edit()
        if self.pattern == "OpenAI Chat Completions":
            extracted = self._extract_from_openai_chat_completions()
        if self.pattern == "OpenAI Completions":
            extracted = self._extract_from_openai_completions()
        if self.pattern == "OpenAI Embeddings":
            extracted = self._extract_from_openai_embeddings()
        if self.pattern == "Anthropic":
            extracted = self._extract_from_anthropic()
        if self.pattern == "VertexAI":
            extracted = self._extract_from_vertexai()
        if self.pattern == "OpenAI Images Variations":
            extracted = self._extract_from_openai_images_variations()
        if self.pattern == "OpenAI Images Generations":
            extracted = self._extract_from_openai_images_generations()
        if self.pattern == "OpenAI Images Edits":
            extracted = self._extract_from_openai_images_edit()
        if self.pattern == "Ollama":
            extracted = self._extract_from_ollama()
        if self.pattern == "Groq":
            extracted = self._extract_from_groq()
        if self.pattern == "Huggingface":
            extracted = self._extract_from_huggingface()
        if self.pattern == "Unsupported":
            raise UnsupportedProviderError(self.url)

        # "Azure Images Variations": r".*openai\.azure\.com.*images\/variations.*",
        # "Azure Images Edits": r".*openai\.azure\.com.*images\/edits.*",

        transaction_params.add_type(extracted["type"])
        transaction_params.add_provider(extracted["provider"])
        transaction_params.add_prompt(extracted["prompt"])

        if self.response.__dict__["status_code"] > 200:
            transaction_params.add_error_message(extracted["error_message"])
        else:
            transaction_params.add_last_message(extracted["last_message"])

        if "model" in extracted:
            transaction_params.add_model(extracted["model"])
        if "input_tokens" in extracted:
            transaction_params.add_input_tokens(extracted["input_tokens"])
        if "output_tokens" in extracted:
            transaction_params.add_output_tokens(extracted["output_tokens"])

        transaction_params.add_messages(extracted["messages"])
        return transaction_params.build()


def token_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    cumulative_total_cost: bool = True,
) -> list[GetTransactionUsageStatisticsSchema]:
    """
    Calculate token usage statistics based on a given period.

    This function takes a list of transactions and calculates token usage statistics
    aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :param cumulative_total_cost: The switch that decides if total cost is cumulative or not.
    :return: A list of GetTransactionUsageStatisticsSchema objects containing token usage statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    project_id = data_dicts[0]["project_id"]
    pairs = list(set([(data["provider"], data["model"]) for data in data_dicts]))
    if date_from:
        for pair_idx in range(len(pairs)):
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_from),
                "project_id": project_id,
                "provider": pairs[pair_idx][0],
                "model": pairs[pair_idx][1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    if date_to:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_to),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }

    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = (
        df.groupby(["provider", "model"])
        .resample(period)
        .agg(
            {
                "project_id": "first",
                "provider": "first",
                "model": "first",
                "total_input_tokens": "sum",
                "total_output_tokens": "sum",
                "total_input_cost": "sum",
                "total_output_cost": "sum",
                "total_cost": "sum",
                "status_code": "sum",
                "latency": "sum",
                "total_transactions": "sum",
                "generation_speed": "sum",
            }
        )
    )

    del result["provider"]
    del result["model"]

    result = result.reset_index()

    result["output_cumulative_total"] = result.groupby(["provider", "model"])[
        "total_output_tokens"
    ].cumsum()
    result["input_cumulative_total"] = result.groupby(["provider", "model"])[
        "total_input_tokens"
    ].cumsum()
    result["total_cumulative_cost"] = result.groupby(["provider", "model"])[
        "total_cost"
    ].cumsum()

    data_dicts = result.to_dict(orient="records")

    result_list = [
        GetTransactionUsageStatisticsSchema(
            provider=data["provider"],
            model=data["model"],
            date=data["date"],
            total_input_tokens=data["total_input_tokens"],
            total_output_tokens=data["total_output_tokens"],
            input_cumulative_total=data["input_cumulative_total"],
            output_cumulative_total=data["output_cumulative_total"],
            total_transactions=data["total_transactions"],
            total_cost=data["total_cumulative_cost"]
            if cumulative_total_cost
            else data["total_cost"],
        )
        for data in data_dicts
    ]

    return result_list


def status_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[GetTransactionStatusStatisticsSchema]:
    """
    Calculate transaction status statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction statuses aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :return: A list of GetTransactionStatusStatisticsSchema objects containing status statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    for x in range(len(data_dicts)):
        data_dicts[x]["status_code"] = (data_dicts[x]["status_code"] // 100) * 100
    df = pd.DataFrame(data_dicts)
    df.set_index("date", inplace=True)

    if date_from:
        date_from = str(date_from)
        df.loc[pd.Timestamp(date_from)] = pd.NA
    if date_to:
        date_to = str(date_to)
        df.loc[pd.Timestamp(date_to)] = pd.NA

    period = pandas_period_from_string(period)

    result = df.resample(period).agg(
        {
            "project_id": "first",
            "provider": "first",
            "model": "first",
            "total_input_tokens": "sum",
            "total_output_tokens": "sum",
            "total_input_cost": "sum",
            "total_output_cost": "sum",
            "total_cost": "sum",
            "status_code": [
                ("status_200", lambda code: (code == 200).sum()),
                ("status_300", lambda code: (code == 300).sum()),
                ("status_400", lambda code: (code == 400).sum()),
                ("status_500", lambda code: (code == 500).sum()),
            ],
            "latency": "sum",
            "total_transactions": "sum",
            "generation_speed": "sum",
        }
    )
    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")

    new_data_dicts = []
    for data in data_dicts:
        new_data = {}
        for key, value in data.items():
            if key[0] == "status_code":
                new_key = key[1]
            else:
                new_key = key[0]
            new_data[new_key] = value
        new_data_dicts.append(new_data)

    result_list = [
        GetTransactionStatusStatisticsSchema(
            date=data["date"],
            status_200=data["status_200"],
            status_300=data["status_300"],
            status_400=data["status_400"],
            status_500=data["status_500"],
            total_transactions=data["total_transactions"],
        )
        for data in new_data_dicts
    ]

    return result_list


def speed_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[GetTransactionLatencyStatisticsSchema]:
    """
    Calculate transaction latency statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction latency aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :return: A list of GetTransactionLatencyStatisticsSchema objects containing latency statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    project_id = data_dicts[0]["project_id"]
    pairs = set([(data["provider"], data["model"]) for data in data_dicts])
    if date_from:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_from),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    if date_to:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_to),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = (
        df.assign(
            transactions_code_200=lambda x: np.where(x["status_code"] == 200, 1, 0)
        )
        .groupby(["provider", "model"])
        .resample(period)
        .agg(
            {
                "project_id": "first",
                "provider": "first",
                "model": "first",
                "total_input_tokens": "sum",
                "total_output_tokens": "sum",
                "total_input_cost": "sum",
                "total_output_cost": "sum",
                "total_cost": "sum",
                "status_code": "first",
                "latency": "sum",
                "total_transactions": "sum",
                "generation_speed": "sum",
                "transactions_code_200": "sum",
            }
        )
    )

    del result["provider"]
    del result["model"]

    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")
    result_list = [
        GetTransactionLatencyStatisticsSchema(
            provider=data["provider"],
            model=data["model"],
            date=data["date"],
            mean_latency=data["latency"].total_seconds() / data["total_transactions"]
            if data["latency"].total_seconds() > 0
            else 0,
            tokens_per_second=data["generation_speed"] / data["transactions_code_200"]
            if data["generation_speed"] > 0 and data["transactions_code_200"] > 0
            else 0,
            total_transactions=data["total_transactions"],
        )
        for data in data_dicts
    ]

    return result_list


def token_counter_for_transactions_by_tag(
    transactions: list[TagStatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    cumulative_total_cost: bool = True,
) -> list[GetTagStatisticTransactionSchema]:
    """
    Calculate token usage statistics based on a given period.

    This function takes a list of transactions and calculates token usage statistics
    aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :param cumulative_total_cost: The switch that decides if total cost is cumulative or not.
    :return: A list of GetTransactionUsageStatisticsSchema objects containing token usage statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    tags = list(set([transaction.tag for transaction in transactions]))
    if date_from:
        for tag in tags:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_from),
                "tag": tag,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "total_transactions": 0,
            }
    if date_to:
        for tag in tags:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_to),
                "tag": tag,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "total_transactions": 0,
            }

    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = (
        df.groupby("tag")
        .resample(period)
        .agg(
            {
                "tag": "first",
                "total_input_tokens": "sum",
                "total_output_tokens": "sum",
                "total_input_cost": "sum",
                "total_output_cost": "sum",
                "total_cost": "sum",
                "total_transactions": "sum",
            }
        )
    )

    del result["tag"]

    result = result.reset_index()

    result["output_cumulative_total"] = result.groupby("tag")[
        "total_output_tokens"
    ].cumsum()
    result["input_cumulative_total"] = result.groupby("tag")[
        "total_input_tokens"
    ].cumsum()
    result["total_cumulative_cost"] = result.groupby("tag")["total_cost"].cumsum()

    data_dicts = result.to_dict(orient="records")

    result_list = [
        GetTagStatisticTransactionSchema(
            tag=data["tag"],
            date=data["date"],
            total_input_tokens=data["total_input_tokens"],
            total_output_tokens=data["total_output_tokens"],
            input_cumulative_total=data["input_cumulative_total"],
            output_cumulative_total=data["output_cumulative_total"],
            total_transactions=data["total_transactions"],
            total_cost=data["total_cumulative_cost"]
            if cumulative_total_cost
            else data["total_cost"],
        )
        for data in data_dicts
    ]

    return result_list


class ProviderPrice:
    def __init__(
        self,
        model_name: str,
        provider: str,
        start_date: datetime | str | None,
        match_pattern: str,
        input_price: int | float,
        output_price: int | float,
        total_price: int | float,
        is_active: bool,
        mode: str,
    ) -> None:
        """
        Initialize a ProviderPrice object.

        :param model_name: The name of the AI model.
        :param start_date: The start date for the price information.
        :param match_pattern: The match pattern for the price information.
        :param input_price: The price for input usage.
        :param output_price: The price for output usage.
        :param total_price: The total price for usage.
        """
        self.model_name = model_name
        self.provider = provider
        self.start_date = (
            datetime.strptime(start_date, "%Y-%m-%d") if start_date != "" else None
        )
        self.match_pattern = match_pattern
        self.input_price = input_price
        self.output_price = output_price
        self.total_price = total_price
        self.is_active = is_active
        self.mode = mode

    def __repr__(self):
        """
        Return a string representation of the ProviderPrice object.

        :return: A string representation of the object.
        """
        return (
            "{"
            + f"model_name: {self.model_name}, provider: {self.provider}, start_date: {self.start_date}, match_pattern: {self.match_pattern}, input_price: {self.input_price}, output_price: {self.output_price}, total_price: {self.total_price}, mode: {self.mode}"
            + "}"
        )


def read_provider_pricelist(
    path: str = "../provider_price_list.json",
) -> list[ProviderPrice]:
    """
    Read the provider price list from a JSON file.

    :param path: The path to the JSON file containing provider prices.
    :return: A list of ProviderPrice objects.
    """
    with open(path, "r") as f:
        data = json.load(f)
    prices = [ProviderPrice(**provider) for provider in data]
    return prices


class ApiURLBuilder:
    @staticmethod
    def build(project, deployment_slug: str, path: str, target_path: str) -> str:
        """
        Build an API URL using the specified project, deployment slug, path, and target path.

        :param project: The project object containing AI providers.
        :param deployment_slug: The deployment slug to identify the AI provider.
        :param path: The base path for the API URL.
        :param target_path: The target path to be appended to the base path.
        :return: The constructed API URL.
        """

        api_base = [
            prov.api_base
            for prov in project.ai_providers
            if prov.slug == deployment_slug
        ][0]
        if path == "":
            path = unquote(unquote(target_path)) if target_path is not None else ""
            if len(path.split("/")[1:]) > 5:
                new_path = path.split("/")[1:]
                new_path = new_path[0:3] + new_path[5:7]
                path = "/" + "/".join(new_path)

        url = api_base + f"/{path}".replace("//", "/")
        print("URL", url)

        if api_base.endswith("/"):
            url = api_base + f"{path}".replace("//", "/")

        print("URL", url)
        return url


class OrderedSet(OrderedDict):
    def __init__(self, iterable=None):
        """
        Create an ordered set, a set that maintains the order of element insertion.

        :param iterable: Optional iterable to initialize the ordered set.
        """
        super().__init__()
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        """
        Add an item to the ordered set.

        :param item: The item to add to the set.
        """
        self[item] = None

    def update(self, iterable):
        """
        Update the ordered set with elements from the provided iterable.

        :param iterable: The iterable containing elements to be added to the ordered set.
        """
        for item in iterable:
            self.add(item)


def pandas_period_from_string(period: str):
    if period == PeriodEnum.week:
        return "W-Mon"
    if period == PeriodEnum.month:
        return "ME"
    if period == PeriodEnum.year:
        return "YE"
    if period == PeriodEnum.hour:
        return "h"
    if period == PeriodEnum.minutes:
        return "5min"
    return "D"


def generate_mock_transactions(n: int, date_from: datetime, date_to: datetime):
    """
    Generate a list of mock transactions.

    This function creates a list of transaction objects for testing purposes.
    The transactions are either successful (status code 200) with randomly
    generated input and output tokens or unsuccessful with no input/output tokens.

    Parameters:
    n (int): The number of transactions to generate.
    date_from (datetime): The start date from which transactions should be added.
    date_to (datetime): The end date till which transactions should be added.

    Returns:
    list: A list of Transaction objects.

    """
    providers = ["Azure", "OpenAI"]
    models = ["gpt-3.5-turbo", "gpt-4", "text-davinci-001"]
    status_codes = [200, 300, 400, 500]

    transactions = []

    for x in range(0, n):
        transaction_id = f"transaction-{x}"
        input_tokens = random.randint(5, 25)
        output_tokens = random.randint(200, 800)

        # Generate random date within date_from and date_to
        time_between_dates = date_to - date_from
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = date_from + timedelta(days=random_number_of_days)
        start_date = random_date
        stop_date = start_date + timedelta(
            seconds=random.randint(1, 6), milliseconds=random.randint(0, 999)
        )

        # Generate random status code according to the distribution, the most common status code is 200, rest is less probable
        status = random.choices(status_codes, [0.75, 0.15, 0.05, 0.05])[0]

        # If status is not 200, set input/output tokens to 0 and error message to "Error"
        error_message = None if status == 200 else "Error"
        generation_speed = (
            output_tokens / (stop_date - start_date).total_seconds()
            if status == 200
            else 0
        )
        output_tokens = output_tokens if status == 200 else 0
        input_cost, output_cost = random.uniform(0.00005, 0.05), random.uniform(
            0.00005, 0.05
        )
        transactions.append(
            Transaction(
                id=transaction_id,
                project_id="project-test",
                tags=["tag1", "tag2", "tag3"],
                provider=random.choice(providers),
                model=random.choice(models),
                type="chat",
                os=None,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                library="PostmanRuntime/7.36.3",
                status_code=status,
                messages=None,
                prompt="",
                last_message="",
                error_message=error_message,
                request_time=start_date,
                response_time=stop_date,
                generation_speed=generation_speed,
                input_cost=input_cost,
                output_cost=output_cost,
                total_cost=input_cost + output_cost,
            )
        )

    return transactions


def check_dates_for_statistics(
    date_from: datetime | str | None, date_to: datetime | str | None
) -> tuple[datetime | None, datetime | None]:
    if isinstance(date_from, str):
        if len(date_from) == 10:
            date_from = datetime.fromisoformat(str(date_from) + "T00:00:00")
        elif date_from.endswith("Z"):
            date_from = datetime.fromisoformat(str(date_from)[:-1])
        else:
            date_from = datetime.fromisoformat(date_from)
    if isinstance(date_to, str):
        if len(date_to) == 10:
            date_to = datetime.fromisoformat(date_to + "T23:59:59")
        elif date_to.endswith("Z"):
            date_to = datetime.fromisoformat(str(date_to)[:-1])
        else:
            date_to = datetime.fromisoformat(date_to)

    if date_from is not None and date_to is not None and date_from == date_to:
        date_to = date_to + timedelta(days=1) - timedelta(seconds=1)

    return date_from, date_to


def read_transactions_from_csv(
    path: str = "../test_transactions.csv",
) -> list[Transaction]:
    df = pd.read_csv(path, sep=";")
    data = df.to_dict(orient="records")
    transactions = []
    pricelist = read_provider_pricelist()
    for idx, obj in enumerate(data):
        transaction_id = f"test-transaction-{idx}"
        request_time = datetime.fromisoformat(
            obj["request_time"].replace("Z", "+00:00")
        )
        response_time = datetime.fromisoformat(
            obj["response_time"].replace("Z", "+00:00")
        )
        latency = response_time - request_time
        price = [
            item
            for item in pricelist
            if item.provider == obj["provider"]
            and re.match(item.match_pattern, obj["model"])
        ]
        if obj["status_code"] == 200:
            if len(price) > 0:
                price = price[0]
                if price.input_price == 0:
                    input_cost, output_cost = 0, 0
                    total_cost = (
                        (obj["input_tokens"] + obj["output_tokens"])
                        / 1000
                        * price.total_price
                    )
                else:
                    input_cost = price.input_price * (obj["input_tokens"] / 1000)
                    output_cost = price.output_price * (obj["output_tokens"] / 1000)
                    total_cost = input_cost + output_cost
            else:
                input_cost, output_cost, total_cost = None, None, None
            transactions.append(
                Transaction(
                    id=transaction_id,
                    project_id="project-test",
                    request={},
                    response={},
                    tags=["tag"],
                    provider=obj["provider"],
                    model=obj["model"],
                    type="chat",
                    os=None,
                    input_tokens=obj["input_tokens"],
                    output_tokens=obj["output_tokens"],
                    library="PostmanRuntime/7.36.3",
                    status_code=obj["status_code"],
                    messages=None,
                    prompt="",
                    last_message="",
                    error_message=None,
                    request_time=request_time,
                    response_time=response_time,
                    generation_speed=obj["output_tokens"] / latency.total_seconds()
                    if latency.total_seconds() > 0
                    else 0,
                    input_cost=input_cost,
                    output_cost=output_cost,
                    total_cost=total_cost,
                )
            )
        else:
            transactions.append(
                Transaction(
                    id=transaction_id,
                    project_id="project-test",
                    request={},
                    response={},
                    tags=["tag"],
                    provider=obj["provider"],
                    model=obj["model"],
                    type="chat",
                    os=None,
                    input_tokens=0,
                    output_tokens=0,
                    library="PostmanRuntime/7.36.3",
                    status_code=obj["status_code"],
                    messages=None,
                    prompt="",
                    last_message="",
                    error_message="Error",
                    request_time=request_time,
                    response_time=response_time,
                    generation_speed=0,
                    input_cost=0,
                    output_cost=0,
                    total_cost=0,
                )
            )
    return transactions


def count_tokens_for_streaming_response(messages: list | str, model: str) -> int:
    encoder = tiktoken.encoding_for_model(model)
    if isinstance(messages, str):
        tokens = encoder.encode(messages)
    else:
        full_prompt = "\n".join(
            [f"{message['role']}: {message['content']}" for message in messages]
        )
        tokens = encoder.encode(full_prompt)
    return len(tokens)


class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def json(self):
        return self.content


def truncate_float(number, decimals):
    if isinstance(number, float):
        str_number = str(number)
        integer_part, decimal_part = str_number.split(".")
        truncated_decimal_part = decimal_part[:decimals]
        return float(f"{integer_part}.{truncated_decimal_part}")
    return number


def resize_b64_image(b64_image: str | str, new_size: tuple[int, int]) -> str:
    image_data = base64.b64decode(b64_image)
    image = Image.open(BytesIO(image_data))
    resized_image = image.resize(new_size)
    buffered = BytesIO()
    resized_image.save(buffered, format=image.format)
    resized_image_bytes = buffered.getvalue()
    resized_b64_string = base64.b64encode(resized_image_bytes).decode("utf-8")
    return resized_b64_string


def preprocess_buffer(request, response, buffer) -> dict:
    decoder = response._get_content_decoder()
    buf = b"".join(buffer)
    if "localhost" in str(request.__dict__["url"]) or "host.docker.internal" in str(
        request.__dict__["url"]
    ):
        content = buf.decode("utf-8").split("\n")
        rest, content = content[-2], content[:-2]
        response_content = {
            pair.split(":")[0]: pair.split(":")[1]
            for pair in rest.split(',"context"')[0][1:].replace('"', "").split(",")
        }
        content = "".join(
            list(
                map(
                    lambda msg: [
                        text
                        for text in [text for text in msg[1:-1].split('response":"')][
                            1
                        ].split('"')
                    ][0],
                    content,
                )
            )
        )
        response_content["response"] = content
    else:
        try:
            response_content = decoder.decode(buf)
            response_content = json.loads(response_content)
        except json.JSONDecodeError:
            content = []
            for i in (
                chunks := buf.decode()
                .replace("data: ", "")
                .split("\n\n")[::-1][3:][::-1]
            ):
                content.append(
                    json.loads(i)["choices"][0]["delta"]["content"].replace("\n", " ")
                )
            content = "".join(content)
            example = json.loads(chunks[0])
            messages = [
                message
                for message in json.loads(request.__dict__["_content"].decode("utf8"))[
                    "messages"
                ]
            ]
            input_tokens = count_tokens_for_streaming_response(
                messages, example["model"]
            )
            output_tokens = count_tokens_for_streaming_response(
                content, example["model"]
            )
            response_content = dict(
                id=example["id"],
                object="chat.completion",
                created=example["created"],
                model=example["model"],
                choices=[
                    dict(
                        index=0,
                        message=dict(role="assistant", content=content),
                        logprobs=None,
                        finish_reason="stop",
                    )
                ],
                system_fingerprint=example["system_fingerprint"],
                usage=dict(
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                ),
            )
    if isinstance(response_content, list):
        response_content = response_content[0]
    if "usage" not in response_content:
        response_content["usage"] = dict(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
    return response_content


class PeriodEnum(str, Enum):
    week = "week"
    year = "year"
    month = "month"
    day = "day"
    hour = "hour"
    minutes = "5minutes"


known_ai_providers = [
    {"provider_name": "OpenAI", "api_base_placeholder": "https://api.openai.com/v1"},
    {
        "provider_name": "Azure OpenAI",
        "api_base_placeholder": "https://<your-deployment-name>.openai.azure.com",
    },
    {
        "provider_name": "Anthropic",
        "api_base_placeholder": "https://api.anthropic.com",
    },
    {
        "provider_name": "Google VertexAI",
        "api_base_placeholder": "https://<location>-aiplatform.googleapis.com/v1",
    },
    {
        "provider_name": "Ollama",
        "api_base_placeholder": "http://localhost:11434/api/generate",
    },
    {
        "provider_name": "Groq",
        "api_base_placeholder": "https://api.groq.com",
    },
    {
        "provider_name": "Huggingface",
        "api_base_placeholder": "https://<your-deployment-name>.us-east-1.aws.endpoints.huggingface.cloud",
    },
    {
        "provider_name": "Other",
        "api_base_placeholder": "https://llmapi.provider.com/v1",
    },
]
