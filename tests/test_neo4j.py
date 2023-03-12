import pytest
from models.neo4j_model import Neo4jDatabase

@pytest.fixture(scope="module")
def neo4j_db():
    db = Neo4jDatabase("bolt://localhost:7687", "neo4j", "password")
    yield db
    db.close()

def test_neo4j_query1(neo4j_db):
    disease_id = "DOID:684"
    result = neo4j_db.query1(disease_id)
    assert len(result) > 0

def test_neo4j_query2(neo4j_db):
    disease_id = "DOID:1227"
    result = neo4j_db.query2(disease_id)
    assert len(result) > 0
