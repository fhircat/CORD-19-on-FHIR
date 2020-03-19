import os
import string
from csv import DictReader
from typing import Optional, Set, Dict

from jsonasobj import as_json, JsonObj

from scripts.metadata import prefixes, DATASETS

MISSING_FILE = 'MISSING'


# Root of datasets
data_subdirs = [e for e in os.listdir(DATASETS) if e.startswith('cord-19-') and '.' not in e]
subdir_contents: Dict[str, Set[str]] = dict()


def generate_identifier(entry: JsonObj) -> None:
    """
    Generate an "id" entry for entry
    :param entry: metadata entry
    """
    if hasattr(entry, 'sha'):
        subdir = which_subdir(row_j.sha)
        row_j.id = subdir + '/' + row_j.sha
    elif hasattr(entry, 'pubmed_id'):
        row_j.id = prefixes.PUBMED[entry.pubmed_id]
    elif hasattr(entry, 'pmcid'):
        row_j.id = prefixes.PMC[entry.pmcid]
    elif hasattr(entry, 'doi'):
        row_j.id = prefixes.DOI[entry.doi]
    elif hasattr(entry, 'Microsoft Academic Paper ID'):
        row_j.id = prefixes.MS_ACADEMIC[entry["Microsoft Academic Paper ID"]]


for subdir in data_subdirs:
    for fname in os.listdir(os.path.join(DATASETS, subdir)):
        if fname[0] in string.hexdigits and fname.endswith(".json"):
            subdir_contents.setdefault(subdir, set()).add(fname)
subdir_contents[MISSING_FILE] = set()


def which_subdir(sha: str) -> Optional[str]:
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
with open('../../datasets/all_sources_metadata_2020-03-13.csv') as f:
    reader = DictReader(f)

    known_sources = dict()
    known_subdirs = dict()
    source_x_to_subdir = dict()

    row_num = 0
    for row in reader:
        row_num += 1
        row_j = JsonObj(**{k: v for k, v in row.items() if v != ""})
        generate_identifier(row_j)
        if hasattr(row_j, "sha"):
            subdir = which_subdir(row_j.sha)
        with open(f'../../datasets/metadata/e{row_num}.json', 'w') as json_file:
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