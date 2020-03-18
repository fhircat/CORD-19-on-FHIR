# CORD-19-on-FHIR -- Semantics for COVID-19 Discovery

CORD-19-on-FHIR is a superset of the 
COVID-19 Open Research Dataset [(CORD-19)](https://pages.semanticscholar.org/coronavirus-research) data, provided by the [Allen Institute](https://alleninstitute.org/) to support research on COVID-19 / SARS-CoV-2 / Novel Coronavirus.  It is represented 
in [FHIR RDF](https://www.hl7.org/fhir/rdf.html)
and was produced by data mining the CORD-19 dataset and adding semantic annotations.  The purpose is to facilitate linkage with other biomedical datasets and enable answering research questions. 

## Wiki
https://github.com/fhircat/CORD-19-on-FHIR/wiki

## Semantic annotations

So far, CORD-19-on-FHIR adds the following semantic annotations to the CORD-19 dataset, based only on parsing the titles and abstracts:

- Conditions - 103,968 instances 
- Medications - 16,406 instances
- Procedures - 54,720 instances

We plan to parse the full text articles soon, for those that we can access.  

If you can generate other semantic linkages, please let us know.  Collaboration is invited.  Please issue a pull request or contact Guoqian Jiang <jiang.guoqian@mayo.edu> and Harold Solbrig <solbrig@jhu.edu>.


## License

This dataset was derived from the CORD-19 dataset, and therefore consists of two subsets, having different licenses, that are intermingled in the CORD-19-on-FHIR dataset:

- the CORD-19 dataset, subject to the CORD-19 license; and

- semantic annotations that were added by CORD-19-on-FHIR data mining, subject to a CC0 license.
 
See [LICENSE](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).  By downloading this dataset you are agreeing to the [dataset licenses](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).

Specific licensing information for individual articles in the dataset is available in the [metadata file](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.csv).  See also the [readme for the metadata file[(https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.readme).

