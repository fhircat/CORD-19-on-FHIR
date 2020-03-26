import os
from typing import Optional
from zipfile import ZipFile, ZIP_DEFLATED

from scripts.metadata import DATASETS_DIR, METADATA_DIR


class Zipper:
    FILES_PER_ZIPFILE = 60000

    def __init__(self, base_dir: str, suffix: str) -> None:
        self.base_dir = base_dir
        self.suffix = suffix
        self.zipfile_series = 0
        self.nfiles_in_zipfile = 0
        self.total_files = 0
        self.zipfile: Optional[ZipFile] = None

    def addfile(self, fname: str) -> None:
        if self.zipfile is None or self.nfiles_in_zipfile >= Zipper.FILES_PER_ZIPFILE:
            self.rollover_zipfile()
        self.zipfile.write(fname, os.path.basename(fname))
        self.nfiles_in_zipfile += 1
        self.total_files += 1

    def rollover_zipfile(self) -> None:
        self.close()
        self.zipfile_series += 1
        zf_name = f"metadata_{self.suffix}_{self.zipfile_series}.zip"
        print(f"Writing {zf_name}")
        self.zipfile = ZipFile(os.path.join(self.base_dir, zf_name), "w", ZIP_DEFLATED)
        self.nfiles_in_zipfile = 0

    def close(self) -> None:
        if self.zipfile is not None:
            self.zipfile.close()

    def summary(self) -> str:
        return f"{self.total_files} {self.suffix} files written"


json_zipper = Zipper(DATASETS_DIR, "json")
ttl_zipper = Zipper(DATASETS_DIR, "ttl")

print(f"** Zipping {METADATA_DIR} **")
for file in os.listdir(METADATA_DIR):
    _, suffix = os.path.splitext(file)
    fname = os.path.join(METADATA_DIR, file)
    if suffix == '.json':
        json_zipper.addfile(fname)
    elif suffix == ".ttl":
        ttl_zipper.addfile(fname)
    else:
        print(f"Skipping {file}")

json_zipper.close()
print(json_zipper.summary())
ttl_zipper.close()
print(ttl_zipper.summary())

