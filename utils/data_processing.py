def process_nodes(nodes):
    processed_nodes = {}
    for node in nodes:
        node_id, name, kind = node
        if kind not in processed_nodes:
            processed_nodes[kind] = {}
        processed_nodes[kind][node_id] = {"name": name}
    return processed_nodes

def process_edges(edges):
    processed_edges = {}
    for edge in edges:
        source, metaedge, target = edge
        edge_type = metaedge.split("->")[1]
        if edge_type not in processed_edges:
            processed_edges[edge_type] = []
        processed_edges[edge_type].append((source, target))
    return processed_edges
