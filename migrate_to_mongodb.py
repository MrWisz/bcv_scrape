"""
One-off migration: import rates_history.json into the MongoDB rates_history collection.

Usage:
    python migrate_to_mongodb.py

Requires MONGODB_URI (and optionally MONGODB_DB_NAME) to be set, e.g. via .env.
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

from app.db import get_db

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rates_history.json')


def main():
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)

    collection = get_db()['rates_history']

    imported = 0
    for date, entry in history.items():
        collection.update_one(
            {'date': date},
            {'$set': {
                'USD': entry['USD'],
                'EUR': entry['EUR'],
                'timestamp': entry['timestamp']
            }},
            upsert=True
        )
        imported += 1

    print(f"Imported {imported} entries from {HISTORY_FILE} into MongoDB.")


if __name__ == '__main__':
    main()
