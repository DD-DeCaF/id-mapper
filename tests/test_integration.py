import os
import pytest
from py2neo import Graph, NodeSelector
from id_mapper.graph import insert_pairs, find_match, collect_matches, \
    NoSuchNode
from id_mapper.metanetx import Pair


graph = Graph(host=os.environ['DB_PORT_7687_TCP_ADDR'],
              password='1')


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
    assert find_match(graph, 'C', 'z', 'y') == ['B']
    with pytest.raises(NoSuchNode):
        find_match(graph, 'N', 'z', 'y')
    selector = NodeSelector(graph)
    A = list(selector.select('Metabolite', id='A', db_name='x'))[0]
    assert set(collect_matches(graph, A, 'z')) == {'B', 'C'}
    graph.delete_all()
