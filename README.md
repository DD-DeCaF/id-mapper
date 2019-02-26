# ID Mapper

[![Build Status](https://travis-ci.org/DD-DeCaF/id-mapper.svg?branch=master)]()
[![Codecov](https://codecov.io/gh/DD-DeCaF/id-mapper/branch/master/graph/badge.svg)](https://codecov.io/gh/DD-DeCaF/id-mapper)
[![DOI](https://zenodo.org/badge/80559780.svg)](https://zenodo.org/badge/latestdoi/80559780)

Based on [MetaNetX](http://www.metanetx.org/). Information about metabolites and reactions is provided by [MNXref namespace](http://www.metanetx.org/mnxdoc/mnxref.html).

An online API service endpoint can be found at https://api.dd-decaf.eu/id-mapper/query.

Example on how to find a match for the chemical with [BIGG](http://bigg.ucsd.edu/) id `nh3` in [BioPath](https://webapps.molecular-networks.com/biopath3/biopath3) database:

```{python}
In [1]: import requests
In [2]: query = {"ids": ["atp"], "db_from": "bigg", "db_to": "kegg", "type": "Metabolite"}
In [3]: requests.post("http://localhost:8000/query", json=query).json()
Out[3]: {"ids": {"atp": ["C00002", "D08646"]}}
```

The graph consists of large amount of connected components. A connected component is considered being one object: a metabolite or a reaction. Search is returning all the elements in the component with `db_to` database name.
![graph](graph.png)

## Development

Download and load the chemical references into the graph database (may take several hours):

```{bash}
curl -O https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_xref.tsv
docker-compose run --rm web python src/load_chem_xref.py
```

Start the application:
```{bash}
docker-compose up
```

## License

id-mapper is licensed under the Apache License Version 2.0 (see LICENSE in source directory).
