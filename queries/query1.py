import os
from pymongo import MongoClient

def query1(disease_id):
    client = MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['DB_NAME']]

    disease = db.nodes.find_one({'id': disease_id, 'kind': 'Disease'})
    if disease:
        # Get drug names that can treat or palliate this disease
        drug_names = []
        edges = db.edges.find({'metaedge': {'$in': ['CdG', 'CtD']}, 'target': disease_id})
        for edge in edges:
            drug = db.nodes.find_one({'id': edge['source'], 'kind': 'Compound'})
            if drug:
                drug_names.append(drug['name'])

        # Get gene names that cause this disease
        gene_names = []
        edges = db.edges.find({'metaedge': 'DaG', 'target': disease_id})
        for edge in edges:
            gene = db.nodes.find_one({'id': edge['source'], 'kind': 'Gene'})
            if gene:
                gene_names.append(gene['name'])

        # Get locations where this disease occurs
        locations = []
        edges = db.edges.find({'metaedge': 'DaL', 'source': disease_id})
        for edge in edges:
            location = db.nodes.find_one({'id': edge['target'], 'kind': 'Anatomy'})
            if location:
                locations.append(location['name'])

        return {'disease_name': disease['name'], 'drug_names': drug_names, 'gene_names': gene_names, 'locations': locations}
    else:
        return None
