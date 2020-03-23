Modify download_bioc.py to set which annotations to pull.

Run download_bioc.py script to pull PMC and PM annotations from Pubtator API:
https://www.ncbi.nlm.nih.gov/research/pubtator/api.html

Run shell scripts to convert the downloaded JSON to RDF turtle.

Conversion script requirements:
https://github.com/AtomGraph/JSON2RDF
https://jena.apache.org/

Notes:
Compile JSON2RDF package and put jar in Project Directory
Add Jena bin to path