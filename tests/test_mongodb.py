import pytest
from models.mongodb_model import MongoDBDatabase

@pytest.fixture(scope="module")
def mongodb_db():
    db = MongoDBDatabase("mongodb://localhost:27017/")
    yield db
    db.close()

def test_mongodb_query1(mongodb_db):
    disease_id = "DOID:684"
    result = mongodb_db.query1(disease_id)
    assert len(result) > 0

def test_mongodb_query2(mongodb_db):
    disease_id = "DOID:1227"
    result = mongodb_db.query2(disease_id)
    assert len(result) > 0
