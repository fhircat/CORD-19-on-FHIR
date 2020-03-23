#!/bin/bash
ROOT_DIR=../..
FILES=$ROOT_DIR/pm/*
target_uri="https://www.ncbi.nlm.nih.gov/pubmed/"
for f in $FILES
do
  id=$(echo $f | grep -oP "\/\K(PMC)?\d{1,12}")
  cat $f | java -jar $ROOT_DIR/json2rdf-1.0.1-jar-with-dependencies.jar $target_uri | riot --formatted=TURTLE > $ROOT_DIR/out/pm/$id.ttl
  break
done