import sys
from models.neo4j_model import Neo4jModel
#from models.mongodb_model import MongoDBModel
from queries.query1 import query1
from queries.query2 import query2

def main():
    # Initialize database models
    neo4j_model = Neo4jModel()
#    mongodb_model = MongoDBModel()

# For testing
#    neo4j_model.query2('DOID:11476')
    while True:
        disease_id = input("Which disease ID would you like to know about? [q to quit]: ")
        if disease_id in ['q', '']:
            print("Bye!")
            sys.exit()

        db = input("Which DB would you like to use? (1 = neo4j, 2 = mongo): ")
        if db not in ['1','2']:
            print("Pick a valid DB")
            continue
        #print(f"{disease_id} {db}")

        if (db == '2'):
            print("How about we just do this in neo4j for now . . .")
        #if (db == '1'):
        if (db):
            # Execute queries and print results
            print("Query 1 results:")
            neo4j_model.query1(disease_id)
            #    print("\nQuery 2 results:")
            #    query2(neo4j_model, mongodb_model)

def import_data():
    resp = input("Are you sure you want to import? (Current data will be deleted): [y|Y] ")

    if resp in ['y','Y']:
        # Import HetioNet data into database models
        neo4j_model.import_data()
        #    mongodb_model.import_data()
    else:
        print("Ij think you said no . . .")


if __name__ == "__main__":
    if "-i" in sys.argv:
        import_data()
    main()
