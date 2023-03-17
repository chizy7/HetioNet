import os
import sys
from dotenv import load_dotenv
from py2neo import Graph

# Add the path to the "utils" module to the Python path
if "__file__" in  globals():
    utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils'))
else:
    # if copying/pasting into repl, make a best effort
    utils_path = os.path.abspath(os.path.join(os.path.dirname('.'), 'utils'))

sys.path.append(utils_path)


from utils.data_import import load_nodes_by_type, load_edges, get_node_types, get_edge_types

load_dotenv()  # Load environment variables from .env file

class Neo4jModel:
    def __init__(self):
        # Initialize the Neo4j driver with the URI and credentials from environment variables
        sess_string = f"""
        Graph(
            { os.getenv("NEO4J_URI") },
                auth=(
                    {os.getenv("NEO4J_USER")},
                    {os.getenv("NEO4J_PASSWORD")}
                )
        )
        """
        #print(sess_string)
        self.session = Graph(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))

    def import_data(self):
        # Load nodes and edges from TSV files
        #nodes = load_nodes_by_type(os.path.join("data", "nodes.tsv"))

        #nodes = []
        #edges = load_edges(os.path.join("data", "edges.tsv"))

        #print(f"# node types: {len(nodes)}, # edge types: {len(edges)}")

        node_types = get_node_types()

        # clear everything
        for node_type in node_types:
            print(f"Deleting {node_type} nodes")
            index_str = f"""DROP INDEX {node_type}_idx IF EXISTS"""
            res = self.session.run(index_str)
            delete_str = f"match (n:{node_type}) detach delete n"
            r = self.session.run(delete_str)
            print(f"Result from clearing {node_type} nodes: {r.summary()}")

        # Create nodes
        for node_type in node_types:
            # Create indexes on label properties for faster querying
            index_str = f"""CREATE INDEX {node_type}_idx IF NOT EXISTS
                FOR (n:{node_type}) ON (n.id)
                """
            res = self.session.run(index_str)
            print(f"Added Index to %s: %s" % (node_type, res.summary()))
            data_file = os.path.abspath(os.path.join("data", "nodes", f"{node_type.lower()}.tsv"))
            print(f"Importing {node_type} nodes")
            s = """
            LOAD CSV FROM 'file:///%s'
            AS line FIELDTERMINATOR '\t'
            CREATE
            (:%s { id: line[0], name: line[1] })
            """ % (data_file, node_type)
            print(s)
            res = self.session.run(s)
            print(f"Added nodes: %s" % res.summary())
            #self.session.commit()


        # Create edges
        edge_types = get_edge_types()
        print(edge_types)
        for edge_type in edge_types:
            edge_source = edge_types[edge_type]['source']
            edge_target = edge_types[edge_type]['target']
            edge_relationship = edge_types[edge_type]['relationship']
            edge_name = edge_types[edge_type]['name']

            data_file = os.path.abspath(os.path.join("data", "edges", f"{edge_name}.tsv"))
            print(f"Importing {edge_type} edges from {data_file}")
            # py2neo.errors.ClientError: [Statement.SyntaxError]
            # The PERIODIC COMMIT query hint is no longer supported.
            # Please use CALL { ... } IN TRANSACTIONS instead.
            #USING PERIODIC COMMIT 1000
            s = """
            LOAD CSV FROM 'file:///%s'
            AS line
            FIELDTERMINATOR '\t'
            MATCH
                (source:%s {id: line[0]}), 
                (target:%s {id: line[1]})
            CREATE
            (source)-[:%s]->(target)
            """ % (data_file, edge_source, edge_target, edge_relationship.upper())
            print(s)
            res = self.session.run(s)
            print(f"Added edges: %s" % res.summary())
            #self.session.commit()

    def query1(self, disease_id):
        # Given a disease id, what is its name,
        # hat are drug names that can treat or
        # palliate this disease, what are gene
        # names that cause this disease, and
        # where this disease occurs? Obtain and
        # output this information in a single query.
        q = f"""
        match (d:Disease) where d.id = '{disease_id}'
        merge (c1:Compound)-[t:TREATS]-(d)
        merge (c2:Compound)-[p:PALLIATES]-(d)
        merge (g:Gene)-[assoc:ASSOCIATES]-(d)
        merge (a:Anatomy)-[l:LOCALIZES]-(d)
        return d,c1,c2,g,a
        """
        #print(q)
        result = self.session.run(q)
        res_nodes =  list(result.next())
        #print(f"Number of nodes returned: {len(res_nodes)}")
        #print(f"Nodes: {res_nodes}")
        disease_node = [n for n in res_nodes if str(n.labels) == ':Disease' ][0]
        compound_nodes = [n for n in res_nodes if str(n.labels) == ':Compound' ]
        gene_nodes = [n for n in res_nodes if str(n.labels) == ':Gene' ]
        anatomy_nodes = [n for n in res_nodes if str(n.labels) == ':Anatomy' ]
        disease_name = disease_node['name']
        print(f"Your disease is {disease_name}")
        print(f"Drugs which treat or palliate this disease:")
        for n in compound_nodes:
            print(f"\t{n['name']}")
        print(f"Genes which cause this disease:")
        for n in gene_nodes:
            print(f"\t{n['name']}")
        print(f"Body parts where this disease can be found:")
        for n in anatomy_nodes:
            print(f"\t{n['name']}")
        print()

    def query2(self):
        # Find all compounds that are either upregulated or downregulated in at least one disease, and return their names
        result = session.run("MATCH (disease: Disease)-[:DaG]-(gene: Gene), (compound: Compound)-[up: CuG]-(gene), (compound)-[down: CdG]-(location: AnatomicalEntity)<-[:PaD]-(disease) WHERE (up.upregulation AND NOT down.downregulation) OR (down.downregulation AND NOT up.upregulation) RETURN DISTINCT compound.name")

        return [record["compound.name"] for record in result]
