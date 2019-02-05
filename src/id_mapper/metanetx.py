# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple

import requests

from .app import app


Pair = namedtuple('Pair', ['metabolite', 'database'])


def make_pairs(line):
    """Parse the Metanetx file string and return the pair of metabolites
    ready to be uploaded to the graph database
    """
    xref, metanetx_id = line.split()[:2]
    xref_db, xref_id = xref.split(':', maxsplit=1)
    return Pair(xref_id, xref_db), Pair(metanetx_id, 'mnx')


def load_xrefs(filename):
    """
    Download Metanetx cross-references files and generate references iterables
    """
    response = requests.get((app.config['METANETX_URL'] + '/{}.tsv').format(filename))
    response.raise_for_status()
    for line in response.iter_lines(decode_unicode=response.encoding):
        if line.startswith('#'):
            continue
        x, y = make_pairs(line)
        if x.metabolite != y.metabolite:
            yield x, y
