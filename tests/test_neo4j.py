import os
import pytest
from models.neo4j_model import Neo4jDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Define fixture to create and close Neo4jDatabase object
@pytest.fixture(scope="module")
def neo4j_db():
    db = Neo4jDatabase(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    yield db
    db.close()

# Test queries using neo4j_db fixture
def test_neo4j_query1(neo4j_db):
    disease_id = "DOID:684"
    result = neo4j_db.query1(disease_id)
    assert len(result) > 0

def test_neo4j_query2(neo4j_db):
    disease_id = "DOID:1227"
    result = neo4j_db.query2(disease_id)
    assert len(result) > 0
