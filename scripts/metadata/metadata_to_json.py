"""
Process the all_sources_metadata file producing both a JSON and an RDF rendering in the metadata output directory
"""
import os
import string
from csv import DictReader
from pathlib import Path
from typing import Optional, Set, Dict, List, Tuple
from urllib.parse import quote

from jsonasobj import as_json, JsonObj
from rdflib import Namespace

from scripts.metadata import prefixes, SOURCE_DIR, METADATA_DIR

# METADATA_FILE = 'all_sources_metadata_2020-03-13.csv'   # 03-13 drop
METADATA_FILE = 'metadata.csv'                          # 03-20 drop

MISSING_FILE = 'MISSING'

# Root of datasets
data_subdirs = [e for e in os.listdir(SOURCE_DIR) if e != 'metadata' and '.' not in e]
subdir_contents: Dict[str, Set[str]] = dict()

# TODO: Can we find WHO Covidence?
IDENTIFIERS: List[Tuple[str, Namespace]] = [
    ('doi', prefixes.DOI),
    ('pubmed_id', prefixes.PUBMED),
    ('pmcid', prefixes.PMC),
    ('Microsoft Academic Paper Id', prefixes.MS_ACADEMIC)
]

SUBDIR_MAP: Dict[str, str] = {
    "biorxiv_medrxiv": "bioRxiv-medRxiv",
    "comm_use_subset": "Commercial",
    "pmcustom_license": "PMC",          # 03-13 drop
    "custom_license": "PMC",            # 03-20 drop
    "noncomm_use_subset": "Non-comercial"
}


def generate_identifier(entry: JsonObj) -> None:
    """
    Generate an "id" entry for entry
    :param entry: metadata entry
    """
    for identifier, namespace in IDENTIFIERS:
        if hasattr(entry, identifier):
            row_j.id = namespace[entry[identifier].split()[0]]
            break
    else:
        if hasattr(entry, 'sha'):
            row_j.id = row_j.sha
        else:
            assert(True, "Record has no identifier - at a loss")


def generate_pubtator(entry: JsonObj) -> None:
    """
    Generate a puptator link if this has a PMC id
    :param entry: metadata entry
    """
    if hasattr(entry, 'pmcid'):
        entry.pubtator = entry.pmcid

def normalize_namespaces(entry: JsonObj) -> None:
    """ Some of the identifiers are actual multiple occurrences.  Instead of representing this as a list, the
    metadata represents this as space separated values.  Turn them into lists if needed
    """
    for identifier, _ in IDENTIFIERS:
        ids = getattr(entry, identifier, None)
        if ids and ' ' in ids:
            setattr(entry, identifier, ids.split())


# Generate a list of all the files we know about
for subdir in data_subdirs:
    for fname in os.listdir(os.path.join(SOURCE_DIR, subdir)):
        if fname[0] in string.hexdigits and fname.endswith(".json"):
            subdir_contents.setdefault(subdir, set()).add(fname)
subdir_contents[MISSING_FILE] = set()


def which_subdir(sha: str) -> Optional[str]:
    """ Determine which subset (if any) sha is represented in """
    fname = sha + '.json'
    for k, v in subdir_contents.items():
        if fname in v:
            subdir_contents[k].remove(fname)
            return k
    subdir_contents[MISSING_FILE].add(fname)
    return MISSING_FILE


print("*** Starting Content ***")
for subdir in data_subdirs:
    print(f"\t{subdir}: {len(subdir_contents[subdir])}")
print()

# This loads the metadata file as a Python dictionary and then emits the first row in JSON
with open(os.path.join(SOURCE_DIR, METADATA_FILE)) as f:
    reader = DictReader(f)

    known_sources = dict()
    known_subdirs = dict()
    source_x_to_subdir = dict()

    row_num = 0
    for row in reader:
        row_num += 1
        row_j = JsonObj(**{k: v for k, v in row.items() if v != ""})
        if hasattr(row_j, 'doi') and ';' in row_j.doi:
            print(f"Escaping DOI in {row_num}")
            row_j.doi = quote(row_j.doi)
        generate_identifier(row_j)
        normalize_namespaces(row_j)
        generate_pubtator(row_j)

        if hasattr(row_j, "sha"):
            row_j.fhir_link = []
            # Possible to have more than one SHA
            for sha in [e.strip() for e in row_j.sha.split(';')]:
                subdir = which_subdir(sha)
                if subdir in SUBDIR_MAP:
                    row_j.fhir_link.append(f"{SUBDIR_MAP[subdir]}/Composition/{sha}")

        if hasattr(row_j, "authors"):
            row_j.authors = [a.strip() for a in row_j.authors.split(';')]
        Path(METADATA_DIR).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(METADATA_DIR, f'e{row_num}.json'), 'w') as json_file:
            # print(f"***** Writing {row_num}.json")
            json_file.write(as_json(row_j))

        known_sources.setdefault(row_j.source_x, 0)
        known_sources[row_j.source_x] += 1
        known_subdirs.setdefault(subdir, 0)
        known_subdirs[subdir] += 1

    print(f"{row_num} entries written")
    print("\n*** File by source_x ***")
    print(known_sources)
    print("\n*** File by subdirectory ***")
    print(known_subdirs)
    print("\n*** Unreferenced files ***")
    for subdir in data_subdirs:
        rem_ents = len(subdir_contents[subdir])
        if rem_ents:
            print(f"\t{subdir}: {rem_ents}")