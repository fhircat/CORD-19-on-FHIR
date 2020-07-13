Co-occurrence Network


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
