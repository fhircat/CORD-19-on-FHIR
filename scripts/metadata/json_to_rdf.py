import os

import jsonasobj
from rdflib import Graph

from scripts.metadata import METADATA_DIR, CONTEXT_DIR

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
