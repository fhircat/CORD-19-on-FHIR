import os
from typing import Optional
from zipfile import ZipFile

from scripts.metadata import DATASETS_DIR, METADATA_DIR

print(f"** Zipping metadata directory **")

files_per_zipfile = 20000
zipfile_series = 0
nfiles = 0
zf: ZipFile = None


def new_zipfile(current_zipfile: Optional[ZipFile]) -> ZipFile:
    global zipfile_series

    if current_zipfile:
        current_zipfile.close()
    zipfile_series += 1
    zf_name = f"metadata{zipfile_series}.zip"
    print(f"\tWriting {zf_name}")
    zf = ZipFile(os.path.join(DATASETS_DIR, zf_name), "w")
    return zf


for file in os.listdir(METADATA_DIR):
    _, suffix = os.path.splitext(file)
    if zf is None or nfiles > files_per_zipfile:
        zf = new_zipfile(zf)
        nfiles = 0
    zf.write(os.path.join(METADATA_DIR, file), os.path.join(suffix[1:], file))
    nfiles += 1

zf.close()
print(f"** {nfiles} written **")
