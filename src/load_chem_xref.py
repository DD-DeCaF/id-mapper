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

"""
Load chemical xrefs into the graph db.

The data source `chem_xref.tsv` should be downloaded from
https://www.metanetx.org/mnxdoc/mnxref.html and placed in the data/ subdir.
"""

import os
import time
from collections import namedtuple

from py2neo import Graph, Node, Relationship
from py2neo.packages.httpstream.http import SocketError
from tqdm import tqdm


print("Connecting to graph database")
connected = False
while not connected:
    try:
        graph = Graph(
            os.environ['ID_MAPPER_API'],
            http_port=int(os.environ['ID_MAPPER_PORT']),
            user=os.environ['ID_MAPPER_USER'],
            password=os.environ['ID_MAPPER_PASSWORD'],
        )
        connected = True
    except SocketError:
        print(f"Could not connect to database, retrying in 2 seconds...")
        time.sleep(2)

print("Reading and parsing 'data/chem_xref.tsv'")
Ref = namedtuple("Ref", ["id", "db", "mnx_id"])
references = []
with open("data/chem_xref.tsv") as file_:
    lines = file_.readlines()

for line in tqdm(lines, mininterval=0.2):
    if line.startswith("#"):
        continue
    line = line.rstrip("\n")
    xref, mnx_id, evidence, description = line.split("\t")

    if ":" not in xref:
        continue

    xref_db, xref_id = xref.split(':', maxsplit=1)

    if xref_id == mnx_id:
        continue

    references.append((
        Node("Metabolite", id=xref_id, db_name=xref_db),
        Node("Metabolite", id=mnx_id, db_name="mnx"),
    ))

print(f"Loaded {len(references)} cross-references")
print(f"Starting database inserts. This may take several hours.")

for ref in tqdm(references, mininterval=0.2):
    xref_node, mnx_node = ref
    graph.merge(xref_node)
    graph.merge(mnx_node)
    graph.merge(Relationship(xref_node, "IS", mnx_node))
    graph.merge(Relationship(mnx_node, "IS", xref_node))
