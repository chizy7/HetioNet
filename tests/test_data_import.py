import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(cwd, os.pardir)))

from utils.data_import import load_nodes, load_edges

def test_load_nodes():
    expected_data = [
        ['1', 'anatomy', 'Anatomy'],
        ['2', 'anatomy', 'Organ'],
        ['3', 'anatomy', 'Organism Subdivision'],
        # ...
    ]
    data = load_nodes('data/nodes.tsv')
    assert data == expected_data


def test_load_edges():
    edges = load_edges('data/edges.tsv')
    assert len(edges) == 355676, "Failed to load all edges"
    assert edges[0] == ('Compound', 'PC2', 'Gene', 'LOC728014', 'DECREASES', ''), "Failed to load first edge"
