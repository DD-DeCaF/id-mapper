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

from id_mapper.graph import GRAPH, insert_pairs, query_identifiers
from id_mapper.metanetx import Pair


elements = [
    (Pair('A', 'x'), Pair('B', 'y')),
    (Pair('C', 'z'), Pair('B', 'y')),
    (Pair('B', 'z'), Pair('C', 'z')),
]


def test_insert_pairs(app):
    insert_pairs('Metabolite', *elements[0])
    assert GRAPH.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 2
    assert GRAPH.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 2
    insert_pairs('Metabolite', *elements[1])
    assert GRAPH.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 3
    assert GRAPH.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 4
    insert_pairs('Metabolite', *elements[2])
    assert GRAPH.dbms.primitive_counts['NumberOfNodeIdsInUse'] == 4
    assert GRAPH.dbms.primitive_counts['NumberOfRelationshipIdsInUse'] == 6
    assert query_identifiers('Metabolite', 'C', 'z', 'y')['C'] == ['B']
    assert 'B' not in query_identifiers('Metabolite', 'N', 'z', 'y')
    GRAPH.delete_all()
