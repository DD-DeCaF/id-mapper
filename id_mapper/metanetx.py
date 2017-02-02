import requests
from collections import namedtuple
from id_mapper.settings import METANETX_URL


Pair = namedtuple('Pair', ['metabolite', 'database'])


def make_pairs(line):
    """Parse the Metanetx file string and return the pair of metabolites
    ready to be uploaded to the graph database
    """
    xref, metanetx_id = line.split()[:2]
    xref_db, xref_id = xref.split(':')
    return Pair(xref_id, xref_db), Pair(metanetx_id, 'mnx')


def load_xrefs(filename):
    """
    Download Metanetx cross-references files and generate references iterables
    """
    response = requests.get((METANETX_URL + '/{}.tsv').format(filename))
    response.raise_for_status()
    for line in response.iter_lines(decode_unicode=response.encoding):
        if line.startswith('#'):
            continue
        x, y = make_pairs(line)
        if x.metabolite != y.metabolite:
            yield x, y
