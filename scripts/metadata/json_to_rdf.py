import os
from zipfile import ZipFile

import jsonasobj
from rdflib import Graph

from scripts.metadata import METADATA_DIR, CONTEXT_DIR, DATASETS_DIR

CONTEXT = os.path.join(CONTEXT_DIR, 'metadata.context.json')
context_j = jsonasobj.load(CONTEXT)
BASE = context_j['@context']['@base']

n_converted = 0
for fname in os.listdir(METADATA_DIR):
    basename, ext = os.path.splitext(fname)
    if ext == '.json':
        g = Graph()
        g.parse(os.path.join(METADATA_DIR, fname), format="json-ld", context=CONTEXT, base=BASE)
        g.serialize(os.path.join(METADATA_DIR, basename + '.ttl'), format='ttl')
        n_converted += 1

print(f"*** {n_converted} files converted ***")

print(f"** Zipping metadata directory **")

files_per_zipfile = 20000
zipfile_series = 0
nfiles = 0
zf = None

def new_zipfile(current_zipfile: ZipFile) -> ZipFile:
    global zipfile_series

    if current_zipfile:
        current_zipfile.close()
    zipfile_series += 1
    zf_name = f"metadata{zipfile_series}.zip"
    print(f"\tWriting {zf_name}")
    zf = ZipFile(os.path.join(DATASETS_DIR, zf_name), "w")
    zf.write(METADATA_DIR)
    return zf


for file in os.listdir(METADATA_DIR):
    if zf is None or nfiles > files_per_zipfile:
        zf = new_zipfile(zf)
        nfiles = 0
    zf.write(os.path.join(METADATA_DIR, file))
    nfiles += 1

zf.close()
