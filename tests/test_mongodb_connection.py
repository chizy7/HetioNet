from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient()

# Access the test database
db = client.test

# Print the names of all collections in the test database
print(db.list_collection_names())

# Close the connection to the MongoDB server
client.close()
