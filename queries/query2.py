import os
from pymongo import MongoClient

def query2(disease_id):
    client = MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['DB_NAME']]

    disease = db.nodes.find_one({'_id': disease_id, 'kind': 'Disease'})
    if not disease:
        return 'Disease not found'

    # Get all genes associated with the disease
    genes = db.edges.find({'source': disease_id, 'metaedge': 'DaG'}, {'target': 1})
    gene_ids = [gene['target'] for gene in genes]

    # Get all compounds that regulate these genes in opposite direction
    compounds = db.edges.aggregate([
        {'$match': {'metaedge': 'CrC', 'source': {'$in': gene_ids}}},
        {'$lookup': {
            'from': 'nodes',
            'localField': 'target',
            'foreignField': '_id',
            'as': 'target_node'
        }},
        {'$unwind': '$target_node'},
        {'$match': {
            'target_node.kind': 'Compound',
            '$or': [
                {'$and': [{'direction': 'up'}, {'location': 'cytoplasm'}]},
                {'$and': [{'direction': 'down'}, {'location': 'nucleus'}]}
            ]
        }},
        {'$group': {'_id': '$target', 'name': {'$first': '$target_node.name'}}},
        {'$sort': [('name', 1)]}
    ])

    compound_names = [compound['name'] for compound in compounds]
    return compound_names
