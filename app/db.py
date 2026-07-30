"""
MongoDB Atlas connection (shared client)
"""
import os
from pymongo import MongoClient

_client = None
_db = None


def get_db():
    """Get the MongoDB database handle, connecting lazily on first use"""
    global _client, _db

    if _db is None:
        uri = os.environ.get("MONGODB_URI")
        if not uri:
            raise RuntimeError("MONGODB_URI environment variable is not set")

        db_name = os.environ.get("MONGODB_DB_NAME", "bcv_scrape")
        _client = MongoClient(uri)
        _db = _client[db_name]
        _db["rates_history"].create_index("date", unique=True)

    return _db
