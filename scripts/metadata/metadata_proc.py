from csv import DictReader

from jsonasobj import as_json, JsonObj

# This loads the metadata file as a Python dictionary and then emits the first row in JSON
with open('../../datasets/all_sources_metadata_2020-03-13.csv') as f:
    reader = DictReader(f)
    known_sources = dict()
    printed = False
    for row in reader:
        row_j = JsonObj(**row)
        if not printed:
            row_j = JsonObj(**row)
            row_j.id = row_j.source_x + '/' + row_j.sha
            print(as_json(row_j))
            printed = True
        known_sources.setdefault(row_j.source_x, 0)
        known_sources[row_j.source_x] += 1

    print(known_sources)
