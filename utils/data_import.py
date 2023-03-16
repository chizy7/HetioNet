import os
import csv

def import_data_to_csv(filename):
    data = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def load_nodes_by_type(filename, delimiter='\t', skip_header=True):
    # will return a dict of lists by node type
    data = {}
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            node_id   = row[0]
            node_name = row[1]
            node_kind = row[2]
            if node_kind not in data.keys():
                data[node_kind] = []
            data[node_kind].append([node_id, node_name])
    return data

def load_metaedges(filename, delimiter='\t', skip_header=True):
    # will return a dict of lists by node type
    data = {}
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            metaedge_id     = row[0]
            metaedge_source = row[1]
            metaedge_target = row[2]
            metaedge_relationship = row[3]
            metaedge_name = row[4]
            data[metaedge_id] = {'source':metaedge_source, 'target':metaedge_target, 'relationship':metaedge_relationship, 'name':metaedge_name}
    return data

def load_edges(filename, delimiter='\t', skip_header=True):
    relationships = load_metaedges(os.path.join("data", "metaedges.tsv"))

    data = {}
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            source = row[0]
            metaedge = row[1]
            target = row[2]
            relationship = relationships[metaedge]['relationship']
            if metaedge not in data.keys():
                data[metaedge] = []
            data[metaedge].append([source, relationship, target])
    return data

def get_node_types():
    relationships = load_metaedges(os.path.join("data", "metaedges.tsv"))
    return list({ relationships[x]['source'] for x in relationships })

def get_edge_types():
    relationships = load_metaedges(os.path.join("data", "metaedges.tsv"))
    #return list({ relationships[x]['source'] for x in relationships })
    return relationships
