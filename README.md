# CORD-19-on-FHIR -- Semantics for COVID-19 Discovery

CORD-19-on-FHIR is a superset of the 
COVID-19 Open Research Dataset [(CORD-19)](https://pages.semanticscholar.org/coronavirus-research) data, provided by the [Allen Institute](https://alleninstitute.org/) to support research on COVID-19 / SARS-CoV-2 / Novel Coronavirus.  It is represented 
in [FHIR RDF](https://www.hl7.org/fhir/rdf.html)
and was produced by data mining the CORD-19 dataset and adding semantic annotations.  The purpose is to facilitate linkage with other biomedical datasets and enable answering research questions. 

## Wiki
https://github.com/fhircat/CORD-19-on-FHIR/wiki

## Semantic annotations

So far, CORD-19-on-FHIR adds the following semantic annotations to the CORD-19 dataset, based only on parsing the titles and abstracts.See an **RDF turtle** example [here](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/examples/sample_0036b28fddf7e93da0970303672934ea2f9944e7.json.ttl). A number of **sparql queries** to identify the instances of different data types are aviable at [here](https://github.com/fhircat/CORD-19-on-FHIR/wiki/SPARQL-Queries). 

- Condition: 182,231 instances
- Medication: 32,069 instances
- Procedure: 100,260 instances

We plan to parse the full text articles soon, for those that we can access.  

If you can generate other semantic linkages, please let us know.  Collaboration is invited.  Please issue a pull request or contact Guoqian Jiang <jiang.guoqian@mayo.edu> and Harold Solbrig <solbrig@jhu.edu>.


## Pubtator annotations

We have also added another set of annotations from [Pubtator](https://www.ncbi.nlm.nih.gov/research/pubtator/).  These are pulled from the Pubtator API via pmcid (PubMed Central id) from metadata file (see below).  Not all PMC ids yielded annotations.  These annotations have been converted from the source JSON into RDF Turtle format. See an **RDF turtle** example [here](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/examples/PMC212558_t.ttl). A number of **sparql queries** to identify the instances of different data types are aviable at [here](https://github.com/fhircat/CORD-19-on-FHIR/wiki/PubTator-Dataset).

- Species:       2,030,458 instances
- Gene:          1,235,829 instances
- Disease:       1,036,954 instances
- Chemical:      778,872 instances
- CellLine:      76,816 instances
- Mutation:      33,413 instances
- Strain:        26,573 instances

## Collaborators

- [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research)
- [COVID-19 Knowledge Accelerator](https://www.gps.health/covid19_knowledge_accelerator.html)
- [EBMonFHIR](https://confluence.hl7.org/display/CDS/EBMonFHIR)
- [Coronavirus Infectious Disease Ontology](http://bioportal.bioontology.org/ontologies/CIDO)
- [Pubtator](https://www.ncbi.nlm.nih.gov/research/pubtator/)
- [OntoText and GraphDB](https://www.ontotext.com/)

## License

This dataset was derived from the CORD-19 dataset, and therefore consists of two subsets, having different licenses, that are intermingled in the CORD-19-on-FHIR dataset:

- the CORD-19 dataset, subject to the CORD-19 license; and

- semantic annotations that were added by CORD-19-on-FHIR data mining, subject to a CC0 license.
 
See [LICENSE](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).  By downloading this dataset you are agreeing to the [dataset licenses](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).

Specific licensing information for individual articles in the dataset is available in the [metadata file](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.csv).  See also the [readme for the metadata file](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.readme).

- semantic annotations that were added by Pubtator from public domain, using the following public domain notice


```text
# ===========================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
#  This software/database is a "United States Government Work" under the
#  terms of the United States Copyright Act.  It was written as part of
#  the author's official duties as a United States Government employee and
#  thus cannot be copyrighted.  This software/database is freely available
#  to the public for use. The National Library of Medicine and the U.S.
#  Government have not placed any restriction on its use or reproduction.
#
#  Although all reasonable efforts have been taken to ensure the accuracy
#  and reliability of the software and data, the NLM and the U.S.
#  Government do not and cannot warrant the performance or results that
#  may be obtained by using this software or data. The NLM and the U.S.
#  Government disclaim all warranties, express or implied, including
#  warranties of performance, merchantability or fitness for any particular
#  purpose.
===============================================================================
 
 
```

## Files

-**Pipfile, Pipfile.lock** -- Use by pip python installer
- **contexts** -- JSON-LD 1.1 `@context` files used in converting JSON data files into RDF Turtle
- **source** -- Source data from CORD-19 release, EXCEPT for the commercial subset, which was too big to put on github.  It is available here: https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/comm_use_subset.tar.gz
- **datasets** -- CORD-19-on-FHIR releases.  There is one zip for corresponding to each of the CORD-19 source subsets.  And there are zip files that, taken together, correspond to the CORD-19 metadata file. Pubtator annotatio release is under the folder Pubtator_RDF.
- **examples** -- A few sample files, illustrating the content of the `datasets` directory.

