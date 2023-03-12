from models.neo4j_model import Neo4jModel
from models.mongodb_model import MongoDBModel
from queries.query1 import query1
from queries.query2 import query2

def main():
    # Initialize database models
    neo4j_model = Neo4jModel()
    mongodb_model = MongoDBModel()

    # Import HetioNet data into database models
    neo4j_model.import_data()
    mongodb_model.import_data()

    # Execute queries and print results
    print("Query 1 results:")
    query1(neo4j_model, mongodb_model)
    print("\nQuery 2 results:")
    query2(neo4j_model, mongodb_model)

if __name__ == "__main__":
    main()
