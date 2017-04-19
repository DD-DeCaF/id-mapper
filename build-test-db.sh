#!/usr/bin/env bash

set -a
source .env
set +a
ID_MAPPER_API=http://localhost

curl http://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_xref.tsv | head -n200 > data/chem_xref.tsv
# curl | head -n200 > data/ecodata.tsv

python load_chem.py
python load_gene.py
