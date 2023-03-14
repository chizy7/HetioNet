import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Add the path to the "utils" module to the Python path
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(utils_path)

from utils.data_import import load_nodes, load_edges

load_dotenv()  # Load environment variables from .env file

class Neo4jModel:
    def __init__(self):
        # Initialize the Neo4j driver with the URI and credentials from environment variables
        self.driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))

    def import_data(self):
        with self.driver.session() as session:
            # Load nodes and edges from TSV files
            nodes = load_nodes(os.path.join("data", "nodes.tsv"), "\t")
            edges = load_edges(os.path.join("data", "edges.tsv"), "\t")

            # Create indexes on label properties for faster querying
            session.run("CREATE INDEX ON :Gene(id)")
            session.run("CREATE INDEX ON :Compound(id)")
            session.run("CREATE INDEX ON :Disease(id)")

            # Create nodes
            for node_type in nodes:
                for node in nodes[node_type]:
                    # Create a node with a label equal to the node_type and properties id and name
                    session.run(f"CREATE (: {node_type} {{id: '{node[0]}', name: '{node[1]}'}})")

            # Create edges
            for edge_type in edges:
                for edge in edges[edge_type]:
                    # Create an edge of type edge[1] between the nodes with ids edge[0] and edge[2]
                    session.run(f"MATCH (source: {edge[0].split('::')[0]} {{id: '{edge[0]}'}}), (target: {edge[2].split('::')[0]} {{id: '{edge[2]}'}}) CREATE (source)-[:{edge[1]}]->(target)")

    def query1(self, disease_id):
        with self.driver.session() as session:
            # Find all genes and compounds associated with a given disease, and return their names and the location of the compounds
            result = session.run(f"MATCH (disease: Disease {{id: '{disease_id}'}})-[:DaG]-(gene: Gene), (gene)-[:GiG]-(compound: Compound) RETURN disease.name, collect(DISTINCT compound.name), collect(DISTINCT gene.name), collect(DISTINCT compound.location)")

            return result.single()

    def query2(self):
        with self.driver.session() as session:
            # Find all compounds that are either upregulated or downregulated in at least one disease, and return their names
            result = session.run("MATCH (disease: Disease)-[:DaG]-(gene: Gene), (compound: Compound)-[up: CuG]-(gene), (compound)-[down: CdG]-(location: AnatomicalEntity)<-[:PaD]-(disease) WHERE (up.upregulation AND NOT down.downregulation) OR (down.downregulation AND NOT up.upregulation) RETURN DISTINCT compound.name")

            return [record["compound.name"] for record in result]
