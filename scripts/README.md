# Scripts directory
The scripts in the script directory perform the following transformations

## [download_cord19_resources.py](metadata/download_cord_19.py)
This script downloads the source files from the semantic scholar site and then un-tars them
into their corresponding directories.  The header of this file
needs to be adjusted to match the release and file names.

```python
CORD19_RELEASE = "2020-03-20"
CORD19_BASE = f"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/{CORD19_RELEASE}/"
CORD19_FILES: List[Tuple[str, bool]] = [
    ("comm_use_subset.tar.gz", True),
    ("biorxiv_medrxiv.tar.gz", True),
    ("noncomm_use_subset.tar.gz", True),
    ("custom_license.tar.gz", True),
    (f"metadata.csv", True)]
```

Note: there is an issue request in to remove the un-tar step and use the tar files directly, as the sole
purpose of this step at the moment is to create lists of files to determine the correct links into the
FHIR RDF rendering.

## [metadata_to_json.py](metadata/metadata_to_json.py)
This creates a json file in the [datasets/metadata] directory for each row in the metadata file.

## [json_to_rdf.py](metadata/json_to_rdf.py)
This uses the [metadata context](contexts/metadata.context.json) to convert the metadata json files to
their RDF equivalent

## [metadata_zipper.py](metadata/metadata_zipper.py) 
This creates zip files out of the metadata directory, separating the json and ttl into separate directories
in the process