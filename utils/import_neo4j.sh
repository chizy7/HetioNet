#!/bin/bash
set -e

# I *think* the import process has issues if it's working with datafiles
# in a different dirctory
cd ../data

neo4j-admin database import full \
     hetionet \
     --verbose \
     --trim-strings=true \
     --delimiter='TAB' \
     --nodes=Gene=nodes/gene.tsv \
     --nodes=Anatomy=nodes/anatomy.tsv \
     --nodes=Disease=nodes/disease.tsv \
     --nodes=Compound=nodes/compound.tsv \
     --relationships=Downregulates=edges/Anatomy_Downregulates_Gene.tsv \
     --relationships=Expresses=edges/Anatomy_Expresses_Gene.tsv \
     --relationships=Upregulates=edges/Anatomy_Upregulates_Gene.tsv \
     --relationships=Binds=edges/Compound_Binds_Gene.tsv \
     --relationships=Downregulates=edges/Compound_Downregulates_Gene.tsv \
     --relationships=Palliates=edges/Compound_Palliates_Disease.tsv \
     --relationships=Resembles=edges/Compound_Resembles_Compund.tsv \
     --relationships=Treats=edges/Compound_Treats_Disease.tsv \
     --relationships=Upregulates=edges/Compound_Upregulates_Gene.tsv \
     --relationships=Associates=edges/Disease_Associates_Gene.tsv \
     --relationships=Downregulates=edges/Disease_Downregulates_Gene.tsv \
     --relationships=Localizes=edges/Disease_Localizes_Anatomy.tsv \
     --relationships=Resembles=edges/Disease_Resembles_Disease.tsv \
     --relationships=Upregulates=edges/Disease_Upregulates_Gene.tsv \
     --relationships=Covaries=edges/Gene_Covaries_Gene.tsv \
     --relationships=Interacts=edges/Gene_Interacts_Gene.tsv \
     --relationships=Regulates=edges/Gene_Regulates_Gene.tsv

# cd back to where we came from
cd -
