# HetioNet
This project implements a database system to model HetioNet using two types of NoSQL stores: Neo4j and MongoDB. The database can answer queries about drugs that can treat or palliate a given disease and the compounds that can treat a new disease. The project includes a Python command-line client interface for database creation and queries.

## Project Requirement

Build a database system to model HetioNet. The database should at least answer the following questions in the quickest response time.
1. Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease and where this disease occurs? Obtain and output this information in a single query.
2. We assume that a compound can treat a disease if the compound `up-regulates/down-regulates` a gene, but the location `down-regulates/up-regulates` the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease(i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.

* Python 3
* pip
* Neo4j
* MongoDB

## Installation
1. Clone the repository: 
```git clone https://github.com/chizy7/HetioNet.git
cd <repository-name>
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Download the HetioNet data files and place them in the `data/` directory.
Default datafiles will already be there

## Usage
### Data Import
In order to import data, run the following command:
```
python3 main.py -i
```
This script will create the necessary database models and import the data from the HetioNet data files.

## Running Queries
To run a query - without importing data - run the following command:
```
python main.py
```
and follow the prompts.

You will be prompted to enter a disease ID. The script will then output the name of the disease, the drug names that can treat or palliate the disease, the gene names that cause the disease, and the locations where the disease occurs.

To run query 2, run the following command:
```cd queries/
python query2.py
```
You will be prompted to enter a new disease name. The script will then output the names of the compounds that can treat the new disease, based on the up-regulation/down-regulation of genes and the location of the disease.

## Running Tests
To run the tests, navigate to the tests/ directory and run the corresponding Python script. For example, to run the Neo4j database model tests, run the following command:
```cd tests/
python test_neo4j.py
```

## Authors and acknowledgment

- Chizaram Chibueze
- Guy Matz

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
