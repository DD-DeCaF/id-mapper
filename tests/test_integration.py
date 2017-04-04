# coding=utf-8
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

import os
from py2neo import Graph
from id_mapper.graph import insert_pairs, query_identifiers
from id_mapper.metanetx import Pair


graph = Graph(host=os.environ['DB_PORT_7687_TCP_ADDR'], password='1')


elements = [
    (Pair('A', 'x'), Pair('B', 'y')),
    (Pair('C', 'z'), Pair('B', 'y')),
    (Pair('B', 'z'), Pair('C', 'z')),
]


def test_insert_pairs():
    insert_pairs(graph, 'Metabolite', *elements[0])
    assert graph.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 2
    assert graph.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 2
    insert_pairs(graph, 'Metabolite', *elements[1])
    assert graph.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 3
    assert graph.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 4
    insert_pairs(graph, 'Metabolite', *elements[2])
    assert graph.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 4
    assert graph.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 6
    assert query_identifiers(graph, 'Metabolite', 'C', 'z', 'y')['C'] == ['B']
    assert 'B' not in query_identifiers(graph, 'Metabolite', 'N', 'z', 'y')
    graph.delete_all()
