from datetime import datetime
from enum import Enum
import json
from typing import Any, Dict, Optional
from pymongo import MongoClient
from pymongo.collection import Collection

class Direction(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class MongoDBLogger:
    def __init__(self, mongo_url: str, collection_name: str = "proxy_logs"):
        self.client = MongoClient(mongo_url)
        self.db = self.client.promptsail
        self.collection: Collection = self.db[collection_name]

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

        self.collection.insert_one(log_entry)
