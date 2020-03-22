from pathlib2 import Path
import pandas as pd
from time import sleep
import os
import requests
import json

PULL_PMC = True
PULL_PM = True
BATCH_SIZE = 1
SLEEPTIME = BATCH_SIZE * 0.34
PMC_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmcids="
PM_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids="

def write_json_files(lines, sha_lookup1, sha_lookup2, out_dir: Path, pmc=True):
    try:
        lines = str(lines)
        for line in lines.splitlines():
            data = json.loads(line)
            article_id = data["id"]
            data["sha"] = sha_lookup1.get("PMC"* pmc + article_id) or sha_lookup2.get("PMC"* pmc + article_id)
            with open(out_dir / f'{"PMC" * pmc}{article_id}.json', 'w') as fp:
                json.dump(data, fp=fp, indent=4)
    except Exception:
        print("Error:")
        print(lines)
        print('*' * 40)
        sleep(100)

def main():
    proj_dir = Path.cwd().parent.parent
    metafile = proj_dir / 'source' / 'metadata.csv'

    # path to save json annotatons to
    pmc_save_dir = proj_dir / 'data' / 'pmc'
    pm_save_dir = proj_dir / 'data' / 'pm'

    # create path for rdf files for later processing
    pmc_rdf_dir = proj_dir / 'data' / 'ttl' / 'pmc'
    pm_rdf_dir = proj_dir / 'data' / 'ttl' / 'pm'

    # create directories
    for dir in (pmc_save_dir, pm_save_dir, pmc_rdf_dir, pm_rdf_dir):
        os.makedirs(dir, exist_ok=True)

    metadata = pd.read_csv(metafile, keep_default_na=False)

    pmcids = list(set(metadata['pmcid']))
    pmids = list(set(metadata['pubmed_id']))

    pmcids.remove('')
    pmids.remove('')

    pmc_to_sha = {k: v for k,v in zip(metadata['pmcid'], metadata['sha'])}
    pm_to_sha = {k: v for k, v in zip(metadata['pubmed_id'], metadata['sha'])}

    # list of already downloaded article id's
    existing_pmc = [file.stem for file in pmc_save_dir.glob('*.json')]
    existing_pm = [file.stem for file in pm_save_dir.glob('*.json')]

    for i in range(len(pmcids) // BATCH_SIZE):
        pmc_batch = pmcids[i:(i + 1) * BATCH_SIZE]
        pm_batch = pmids[i:(i + 1) * BATCH_SIZE]

        # only get new articles
        pmc_batch = [i for i in pmc_batch if i not in existing_pmc]
        pm_batch = [i for i in pm_batch if i not in existing_pm]

        # Pubmed Central
        if pmc_batch and PULL_PMC:
            pmc_query = PMC_URL + ','.join(pmc_batch)
            r = requests.get(pmc_query)
            write_json_files(r.text, pmc_to_sha, pm_to_sha, pmc_save_dir, pmc=True)
            sleep(SLEEPTIME)

        # Pubmed
        if pm_batch and PULL_PM:
            pm_query = PM_URL + ','.join(pm_batch)
            r = requests.get(pm_query)
            write_json_files(r.text,pmc_to_sha, pm_to_sha, pm_save_dir, pmc=False)
            sleep(SLEEPTIME)


if __name__ == "__main__":
    main()