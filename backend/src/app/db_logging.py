from datetime import datetime
from enum import Enum
import json
from typing import Any, Dict, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from app.logging import logger, logging_context

class Direction(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class MongoDBLogger:
    def __init__(self, mongo_url: str, collection_name: str = "proxy_logs"):
        logger.info(f"Connecting to MongoDB at {mongo_url}")
        self.client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        self.db = self.client.prompt_sail  # Use the known database name
        self.collection: Collection = self.db[collection_name]
        # Test connection and collection
        self.client.server_info()
        logger.info(f"MongoDB connected, using collection: {collection_name}")

    def log_request(
        self,
        direction: Direction,
        method: str,
        url: str,
        headers: Dict[str, str],
        body: Optional[Any] = None,
        status_code: Optional[int] = None
    ) -> None:
        """
        Log a request/response to MongoDB with timestamp and direction.
        
        Args:
            direction: Direction enum indicating if this is an incoming or outgoing request
            method: HTTP method used
            url: Request URL
            headers: Request headers
            body: Request/response body (optional)
            status_code: Response status code (optional, for responses)
        """
        log_entry = {
            "timestamp": datetime.utcnow(),
            "direction": direction,
            "method": method,
            "url": url,
            "headers": headers
        }

        # Handle body if present
        if body:
            try:
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                if isinstance(body, str):
                    body = json.loads(body)
                log_entry["body"] = body
            except (json.JSONDecodeError, UnicodeDecodeError):
                log_entry["body"] = str(body)

        if status_code is not None:
            log_entry["status_code"] = status_code

        result = self.collection.insert_one(log_entry)
        logger.info(f"MongoDB log entry inserted with ID: {result.inserted_id}")
        return result.inserted_id
