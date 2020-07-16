Co-occurrence Network

## Data Extraction
```sparql

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX pmc: <https://www.ncbi.nlm.nih.gov/pmc/articles#>

SELECT DISTINCT ?pmc_id0 ?text0 ?pmc_id1 ?text1 (COUNT(?pmc_id1) as ?count) WHERE {
    ?pmc pmc:annotations[ 
        pmc:id ?id0 ; pmc:text ?text0 ; pmc:infons[ 
        pmc:type ?type0 ; pmc:identifier ?pmc_id0 ] ] .    

    FILTER (?type0 = 'Disease' && ?pmc_id0 != "-" && ?pmc_id0 != ?pmc_id1).     
    {             
    SELECT * WHERE {
    	?pmc pmc:annotations [ 
                pmc:id ?id1 ; pmc:text ?text1 ; pmc:infons[ 
                pmc:type ?type1 ; pmc:identifier ?pmc_id1 ] ] .             

        FILTER (?type1= 'Disease' && ?pmc_id1 != "-" )   
 	    }    
    }
} GROUP BY ?pmc_id0 ?text0 ?pmc_id1 ?text1  ORDER BY DESC(?count)


PREFIX mesh: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?id ?name where { 
	?s a mesh:SCR_Chemical .
    ?s mesh:identifier ?id0 .
    ?s rdfs:label ?label .
    BIND(CONCAT("MESH_", str(?id0)) as ?id)
    BIND(str(?label) as ?name)
   ## FILTER (contains (lcase(str(?label)), "covid"))
} 

PREFIX mesh: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select DISTINCT ?id ?name where { 
	?d a mesh:SCR_Disease .
    ?d mesh:preferredMappedTo ?s .
    ?s a mesh:Descriptor .
    ?s mesh:identifier ?id0 .
    ?s rdfs:label ?label .
    BIND(CONCAT("MESH_", str(?id0)) as ?id)
    BIND(str(?label) as ?name)
   ## FILTER (contains (lcase(str(?label)), "covid"))
} 


```
## Data Loading

```sparql
//load test disease nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-disease.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (d:Disease {id:row.pmc_id0})
SET d.name = row.text0;

//load test gene nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-gene.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (g:Gene {id:row.pmc_id0})
SET g.name = row.text0;

//load gene nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "gene_id_names.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (g:Gene {id:row.id})
SET g.name = row.name;

//load mutation nodes
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "gene_id_names.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (m:Mutation {id:row.id})
SET m.name = row.name;

WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "mesh-scr-chemical-01.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (g:Chemical {id:row.id})
SET g.name = row.name;



//load test cooccurence relationships
WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "test-count.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (origin:Disease {id: row.pmc_id0})
MATCH (destination:Gene {id: row.pmc_id1})
MERGE (origin)-[:COOCCURRENCE {count: toInteger(row.count)}]-(destination);


WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "query-result-disease-drug-count.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (origin:Disease {id: row.stardId})
MATCH (destination:Chemical {id: row.endId})
MERGE (origin)-[:COOCCURRENCE {count: toInteger(row.count)}]-(destination);

WITH "https://raw.githubusercontent.com/fhircat/CORD-19-on-FHIR/master/cooccurrence/" AS base
WITH base + "query-result-disease-gene-count.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (origin:Disease {id: row.stardId})
MATCH (destination:Gene {id: row.endId})
MERGE (origin)-[:COOCCURRENCE {count: toInteger(row.count)}]-(destination);




```


## Cypher Queries

```sparql
//query
MATCH((d:Disease)-[c:COOCCURRENCE]-(g:Gene)) WHERE c.count>0  RETURN d, g;

MATCH((d:Disease{name:'COVID-19'})-[c:COOCCURRENCE]-(g:Gene)) WHERE c.count>1000  RETURN d, g;



```


## Data Analytics Using Graph Algorithms

### Betweeness Centrality

```sparql
CALL gds.betweenness.stream({
nodeProjection: "Disease",
relationshipProjection: "COOCCURRENCE"
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, gds.util.asNode(nodeId).name AS name,score
ORDER BY score DESC;


```

### PageRank

```sparql
CALL gds.pageRank.stream({
nodeProjection: "Disease",
relationshipProjection: "COOCCURRENCE",
maxIterations: 20,
dampingFactor: 0.85
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, gds.util.asNode(nodeId).name AS name,score
ORDER BY score DESC;

```
### Triangle Algorithm

```json
CALL gds.alpha.triangles({
nodeProjection: "Disease",
relationshipProjection: {
DEPENDS_ON: {
type: "COOCCURRENCE",
orientation: "UNDIRECTED"
}
}
})
YIELD nodeA, nodeB, nodeC
RETURN gds.util.asNode(nodeA).name AS nodeA,
gds.util.asNode(nodeB).name AS nodeB,
gds.util.asNode(nodeC).name AS nodeC;



```
## Local Clustering Coefficient

```sql

CALL gds.localClusteringCoefficient.stream({
nodeProjection: "Disease",
relationshipProjection: {
DEPENDS_ON: {
type: "COOCCURRENCE",
orientation: "UNDIRECTED"
}
}
})
YIELD nodeId, localClusteringCoefficient
WHERE localClusteringCoefficient > 0
RETURN gds.util.asNode(nodeId).name AS disease, localClusteringCoefficient
ORDER BY localClusteringCoefficient DESC;

```
