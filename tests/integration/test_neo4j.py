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

from id_mapper.graph import GRAPH, query_identifiers

from py2neo import Node, Relationship


elements = [
    (Node("Metabolite", id="A", db_name="x"), Node("Metabolite", id="B", db_name="y")),
    (Node("Metabolite", id="C", db_name="z"), Node("Metabolite", id="B", db_name="y")),
    (Node("Metabolite", id="B", db_name="z"), Node("Metabolite", id="C", db_name="z")),
]


def _insert_pairs(node1, node2):
    GRAPH.merge(node1)
    GRAPH.merge(node2)
    GRAPH.merge(Relationship(node1, "IS", node2))
    GRAPH.merge(Relationship(node2, "IS", node1))


def test_insert_pairs(app):
    _insert_pairs(*elements[0])
    assert GRAPH.dbms.primitive_counts["NumberOfNodeIdsInUse"] == 2
    assert GRAPH.dbms.primitive_counts["NumberOfRelationshipIdsInUse"] == 2
    _insert_pairs(*elements[1])
    assert GRAPH.dbms.primitive_counts["NumberOfNodeIdsInUse"] == 3
    assert GRAPH.dbms.primitive_counts["NumberOfRelationshipIdsInUse"] == 4
    _insert_pairs(*elements[2])
    assert GRAPH.dbms.primitive_counts["NumberOfNodeIdsInUse"] == 4
    assert GRAPH.dbms.primitive_counts["NumberOfRelationshipIdsInUse"] == 6
    assert query_identifiers("Metabolite", "C", "z", "y")["C"] == ["B"]
    assert "B" not in query_identifiers("Metabolite", "N", "z", "y")
    GRAPH.delete_all()
