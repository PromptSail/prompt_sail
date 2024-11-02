from utils import detect_subdomain

from datetime import datetime, timedelta
import pandas as pd
import re
from transactions.models import Transaction
from pathlib import Path


def test_detect_subdomain():
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com") is None
    )
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com:8000")
        is None
    )
    assert (
        detect_subdomain(host="project1.mydomain.com", base_url="https://mydomain.com")
        == "project1"
    )
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com:8000")
        == None
    )
    assert (
        detect_subdomain(
            host="project2.foo.bar.baz", base_url="https://foo.bar.baz:8000"
        )
        == "project2"
    )


def test_local_domains():
    host = "project1.promptsail.local:8000"
    base_url = "http://promptsail.local:8000"
    assert detect_subdomain(host, base_url) == "project1"





def read_transactions_from_csv(fixture_file_name: str) -> list[Transaction]:
    """Read test transactions from a CSV file. 
    
    The CSV files are located in the fixtures/transactions directory. 
    
    The CSV file should have the following columns:
    provider;model;total_tokens;input_tokens;output_tokens;status_code;request_time;response_time
    
    Example:
        OpenAI;babbage-002;216;200;16;200;2024-04-18T11:11:34.098Z;2024-04-18T11:11:34.490Z
    OpenAI;davinci-002;62;46;16;200;2024-04-18T11:24:05.948Z;2024-04-18T11:24:06.573Z
    
    Args:
        fixture_file_name: Name of the fixture file in the fixtures/transactions directory.

    Returns:
        List of Transaction objects
    """
    # Get path to fixtures directory relative to this file
    fixtures_dir = Path(__file__).parent / "fixtures"
    path = fixtures_dir / "transactions" / fixture_file_name
    
    # check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist. Check if the file exists in the fixtures/transactions directory.")

    df = pd.read_csv(path, sep=";")
    data = df.to_dict(orient="records")
    transactions = []
    
    for idx, obj in enumerate(data):
        transaction_id = f"test-transaction-{idx}"
        request_time = datetime.fromisoformat(obj["request_time"].replace("Z", "+00:00"))
        response_time = datetime.fromisoformat(obj["response_time"].replace("Z", "+00:00"))
        latency = response_time - request_time

        if obj["status_code"] == 200:
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
                    generation_speed=obj["output_tokens"] / latency.total_seconds() if latency.total_seconds() > 0 else 0,
                    input_cost=0,
                    output_cost=0,
                    total_cost=0,
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



# deprecated: moved to tests/utils.py
def read_transactions_from_csv_old(
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