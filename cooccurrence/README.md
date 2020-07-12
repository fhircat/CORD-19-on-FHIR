Co-occurrence Network


```cypher
//load disease nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-disease.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (d:Disease {id:row.pmc_id0})
SET d.name = row.text0;

//load gene nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-gene.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (g:Gene {id:row.pmc_id0})
SET g.name = row.text0;


//load cooccurence relationships
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-count.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (origin:Disease {id: row.pmc_id0})
MATCH (destination:Gene {id: row.pmc_id1})
MERGE (origin)-[:COOCCURRENCE {count: toInteger(row.count)}]-(destination);


//query
MATCH((d:Disease)-[c:COOCCURRENCE]-(g:Gene)) WHERE c.count>0  RETURN d, g;

```
