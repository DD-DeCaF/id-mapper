#!/usr/bin/env bash

export ID_MAPPER_API=http://localhost
export ID_MAPPER_PORT=7474
export ID_MAPPER_PASSWORD=1

curl http://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_xref.tsv | head -n200 > data/chem_xref.tsv
# curl | head -n200 > data/ecodata.tsv



python load_chem.py
python load_gene.py
