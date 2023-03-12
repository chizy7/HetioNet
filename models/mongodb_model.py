from pymongo import MongoClient
from utils.data_import import load_nodes, load_edges


class MongoDbModel:
    def __init__(self, host, port, db_name):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def query1(self, disease_id):
        disease_collection = self.db["diseases"]
        drug_collection = self.db["drugs"]
        gene_collection = self.db["genes"]
        location_collection = self.db["locations"]

        # Find disease by id and get its name
        disease = disease_collection.find_one({"id": disease_id}, {"_id": 0, "name": 1})

        # Find drugs that can treat or palliate the disease
        drugs = drug_collection.find({"treats": {"$elemMatch": {"disease_id": disease_id}}}, {"_id": 0, "name": 1})

        # Find genes that cause the disease
        genes = gene_collection.find({"causes": {"$elemMatch": {"disease_id": disease_id}}}, {"_id": 0, "name": 1})

        # Find the locations where the disease occurs
        locations = location_collection.find({"diseases": disease_id}, {"_id": 0, "name": 1})

        # Combine the results into a single dictionary and return it
        result = {
            "disease_name": disease["name"],
            "drug_names": [drug["name"] for drug in drugs],
            "gene_names": [gene["name"] for gene in genes],
            "location_names": [location["name"] for location in locations],
        }
        return result

    def query2(self, new_disease_id):
        drug_collection = self.db["drugs"]
        gene_collection = self.db["genes"]
        location_collection = self.db["locations"]

        # Find genes that are associated with the new disease
        genes = gene_collection.find({"associations": {"$elemMatch": {"disease_id": new_disease_id}}})

        # Find drugs that can target those genes in a way that down-regulates/up-regulates them
        drugs = []
        for gene in genes:
            for association in gene["associations"]:
                if association["disease_id"] != new_disease_id:
                    # Check if the gene is regulated in a way opposite to the new disease location
                    location = location_collection.find_one(
                        {"id": association["location_id"], "regulates": gene["id"]},
                        {"_id": 0, "name": 1, "regulates_direction": 1},
                    )
                    if location and location["regulates_direction"] != association["direction"]:
                        # Find the drugs that target this gene
                        drug_results = drug_collection.find(
                            {"targets": {"$elemMatch": {"gene_id": gene["id"]}}}, {"_id": 0, "name": 1}
                        )
                        for drug in drug_results:
                            drugs.append(drug)

        # Remove duplicate drugs
        unique_drugs = list({drug["name"]: drug for drug in drugs}.values())

        # Return the drug names as a list
        result = {"drug_names": [drug["name"] for drug in unique_drugs]}
        return result
