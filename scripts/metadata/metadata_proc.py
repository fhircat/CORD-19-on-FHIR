import os
import string
from csv import DictReader
from typing import List, Optional, Set, Dict

from jsonasobj import as_json, JsonObj

MISSING_FILE = 'MISSING'

subdir_base = "/Users/solbrig/data/CORD Dataset"
data_subdirs = ["biorxiv_medrxiv", "comm_use_subset", "noncomm_use_subset", "pmc_custom_license"]
subdir_contents: Dict[str, Set[str]] = dict()

for subdir in data_subdirs:
    for fname in os.listdir(os.path.join(subdir_base, subdir)):
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
    printed = False
    for row in reader:
        row_j = JsonObj(**row)
        subdir = which_subdir(row_j.sha)
        row_j.id = subdir + '/' + row_j.sha
        if not printed:
            print(as_json(row_j))
            printed = True
        known_sources.setdefault(row_j.source_x, 0)
        known_sources[row_j.source_x] += 1
        known_subdirs.setdefault(subdir, 0)
        known_subdirs[subdir] += 1

    print("\n*** File by source_x ***")
    print(known_sources)
    print("\n*** File by subdirectory ***")
    print(known_subdirs)
    print("\n*** Unreferenced files ***")
    for subdir in data_subdirs:
        rem_ents = len(subdir_contents[subdir])
        if rem_ents:
            print(f"\t{subdir}: {rem_ents}")