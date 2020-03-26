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


## Pubtator annotations

We have also added another set of annotations from [Pubtator](https://www.ncbi.nlm.nih.gov/research/pubtator/).  These are pulled from the Pubtator API via pmcid (PubMed Central id) from metadata file (see below).  Not all PMC ids yielded annotations.  These annotations have been converted from the source JSON into RDF Turtle format.

## License

This dataset was derived from the CORD-19 dataset, and therefore consists of two subsets, having different licenses, that are intermingled in the CORD-19-on-FHIR dataset:

- the CORD-19 dataset, subject to the CORD-19 license; and

- semantic annotations that were added by CORD-19-on-FHIR data mining, subject to a CC0 license.
 
See [LICENSE](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).  By downloading this dataset you are agreeing to the [dataset licenses](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/LICENSE).

Specific licensing information for individual articles in the dataset is available in the [metadata file](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.csv).  See also the [readme for the metadata file[(https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/all_sources_metadata_2020-03-13.readme).

## Files

-**Pipfile, Pipfile.lock** -- Use by pip python installer
- **contexts** -- JSON-LD 1.1 `@context` files used in converting JSON data files into RDF Turtle
- **source** -- Source data from CORD-19 release, EXCEPT for the commercial subset, which was too big to put on github.  It is available here: https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/comm_use_subset.tar.gz
- **datasets** -- CORD-19-on-FHIR releases.  There is one zip for corresponding to each of the CORD-19 source subsets.  And there are zip files that, taken together, correspond to the CORD-19 metadata file.
- **examples** -- A few sample files, illustrating the content of the `datasets` directory.

