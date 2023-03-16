import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Add the path to the "utils" module to the Python path
if "__file__" in  globals():
    utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils'))
else:
    # if copying/pasting into repl, make a best effort
    utils_path = os.path.abspath(os.path.join(os.path.dirname('.'), 'utils'))

sys.path.append(utils_path)


from utils.data_import import load_nodes_by_type, load_edges

load_dotenv()  # Load environment variables from .env file

class Neo4jModel:
    def __init__(self):
        # Initialize the Neo4j driver with the URI and credentials from environment variables
        self.driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))

    def import_data(self):
        with self.driver.session() as session:
            # Load nodes and edges from TSV files
            nodes = load_nodes_by_type(os.path.join("data", "nodes.tsv"))
            #nodes = []
            edges = load_edges(os.path.join("data", "edges.tsv"))

            print(f"# node types: {len(nodes)}, # edge types: {len(edges)}")

            # clear everything
            #r = session.run("match (n) detach delete n")
            #print(f"Result from clearning nodes: {r.data()}")
            # Create nodes
            ctr = 0
            for node_type in nodes:
                for node in nodes[node_type]:
                    # Create a node with a label equal to the node_type and properties id and name
                    print(node)
                    s= f'CREATE (: {node_type} {{id: "{node[0].split("::")[1]}", name: "{node[1]}"}})'
                    session.run(s)
                    print(s)
                    ctr = ctr + 1
                    if ctr % 100 == 0:
                        print(f"Added 100 nodes of {node_type}")
            print(f"Added {ctr} nodes")

            # Create edges
            ctr = 0
            for edge_type in edges:
                for edge in edges[edge_type]:
                    # Create an edge of type edge[1] between the nodes with ids edge[0] and edge[2]
                    s = f"MATCH (source: {edge[0].split('::')[0]} {{id: '{edge[0].split('::')[1]}'}}), (target: {edge[2].split('::')[0]} {{id: '{edge[2].split('::')[1]}'}}) CREATE (source)-[:{edge[1]}]->(target)"
                    r = session.run(s)
                    print(f"Result from : {s}\n\t{r.data()}")
                    ctr = ctr + 1
                    if ctr % 100 == 0:
                        print(f"Added 100 edges of {edge_type}")
            print(f"Added {ctr} edges")
            # Create indexes on label properties for faster querying
            # Getting error when in original location
            # Maybe we need to create nodes first?- gmatz TODO
#            session.run("CREATE INDEX ON :Gene(id)")
#            session.run("CREATE INDEX ON :Compound(id)")
#            session.run("CREATE INDEX ON :Disease(id)")

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
