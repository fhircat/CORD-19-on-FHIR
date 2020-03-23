import os
import tarfile
from typing import List, Tuple

import requests

from scripts.metadata import SOURCE_DIR

CORD19_RELEASE = "2020-03-20"
CORD19_BASE = f"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/{CORD19_RELEASE}/"
CORD19_FILES: List[Tuple[str, bool]] = [
    ("comm_use_subset.tar.gz", False),
    ("biorxiv_medrxiv.tar.gz", False),
    ("noncomm_use_subset.tar.gz", False),
    ("custom_license.tar.gz", False),
    (f"metadata.csv", False)]


# Borrowed from https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
def download_file(fname: str) -> None:
    with requests.get(CORD19_BASE + fname, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(SOURCE_DIR, fname), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


for file, download in CORD19_FILES:
    if download:
        print(f"Downloading: {file}")
        download_file(file)
    else:
        print(f"Skipped: {file}")


for file, _ in CORD19_FILES:
    if file.endswith(".tar.gz"):
        tarfile = tarfile.open(os.path.join(SOURCE_DIR, file), "r:gz")
        tarfile.extractall(SOURCE_DIR)
