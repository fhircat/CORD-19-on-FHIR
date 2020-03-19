import os
import zipfile

from scripts.metadata import DATASETS

for zipped_file in os.listdir(DATASETS):
    if zipped_file.endswith('.zip'):
        zip_ref = zipfile.ZipFile(os.path.join(DATASETS, zipped_file), 'r')
        zip_ref.extractall(DATASETS)
        zip_ref.close()