import os
import pytest
from models.mongodb_model import MongoDBDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="module")
def mongodb_db():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    db = MongoDBDatabase(mongo_uri, db_name)
    yield db
    db.close()
