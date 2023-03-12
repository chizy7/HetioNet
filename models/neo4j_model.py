from neo4j import GraphDatabase
from utils.data_import import load_nodes, load_edges

class Neo4jModel:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    def import_data(self):
        with self.driver.session() as session:
            nodes = load_nodes()
            edges = load_edges()

            # Create indexes on label properties for faster querying
            session.run("CREATE INDEX ON :Gene(id)")
            session.run("CREATE INDEX ON :Compound(id)")
            session.run("CREATE INDEX ON :Disease(id)")

            # Create nodes
            for node_type in nodes:
                for node in nodes[node_type]:
                    session.run(f"CREATE (: {node_type} {{id: '{node[0]}', name: '{node[1]}'}})")

            # Create edges
            for edge_type in edges:
                for edge in edges[edge_type]:
                    session.run(f"MATCH (source: {edge[0].split('::')[0]} {{id: '{edge[0]}'}}), (target: {edge[2].split('::')[0]} {{id: '{edge[2]}'}}) CREATE (source)-[:{edge[1]}]->(target)")

    def query1(self, disease_id):
        with self.driver.session() as session:
            result = session.run(f"MATCH (disease: Disease {{id: '{disease_id}'}})-[:DaG]-(gene: Gene), (gene)-[:GiG]-(compound: Compound) RETURN disease.name, collect(DISTINCT compound.name), collect(DISTINCT gene.name), collect(DISTINCT compound.location)")

            return result.single()

    def query2(self):
        with self.driver.session() as session:
            result = session.run("MATCH (disease: Disease)-[:DaG]-(gene: Gene), (compound: Compound)-[up: CuG]-(gene), (compound)-[down: CdG]-(location: AnatomicalEntity)<-[:PaD]-(disease) WHERE (up.upregulation AND NOT down.downregulation) OR (down.downregulation AND NOT up.upregulation) RETURN DISTINCT compound.name")

            return [record["compound.name"] for record in result]

    def clear_data(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
