import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

DATASETS_DIR = os.path.join(ROOT_DIR, 'datasets')
METADATA_DIR = os.path.join(DATASETS_DIR, 'metadata')
CONTEXT_DIR = os.path.join(ROOT_DIR, 'contexts')