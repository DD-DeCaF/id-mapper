import os
from py2neo import Graph, NodeSelector, Node, Relationship


class Is(Relationship): pass


class NoSuchNode(Exception):
    """
    Raised if no node for the object exists
    """
    def __init__(self, node_id, database):
        self.node = node_id
        self.database = database

    def __str__(self):
        return 'No node for object {} from database {}'.format(
            self.node,
            self.database,
        )


def insert_pairs(label, pair1, pair2):
    """Merge nodes to database and create mutual IS relationships between

    :param label: "Metabolite" or "Reaction"
    :param pair1: node 1
    :param pair2: node 2
    :return:
    """
    graph = Graph(host=os.environ['DB_PORT_7687_TCP_ADDR'], password='1')
    nodes = [
        Node(
            label,
            id=pair.metabolite,
            db_name=pair.database
        )
        for pair in (pair1, pair2)
        ]
    for n in nodes:
        graph.merge(n)
    graph.merge(Is(nodes[0], nodes[1]))
    graph.merge(Is(nodes[1], nodes[0]))


def find_match(object_id, db_from, db_to):
    """Return id for given metabolite from the corresponding database

    :param met_id: metabolite id
    :param db_from: database name, f.e "bigg"
    :param db_to: database name, f.e "mnx"
    :return:
    """
    graph = Graph(host=os.environ['DB_PORT_7687_TCP_ADDR'], password='1')
    selector = NodeSelector(graph)
    selected = list(selector.select('Metabolite', id=object_id, db_name=db_from))
    assert len(selected) <= 1
    if not selected:
        raise NoSuchNode(object_id, db_from)
    result = []
    for rel in graph.match(start_node=selected[0], rel_type="IS"):
        if rel.end_node()["db_name"] == db_to:
            result.append(rel.end_node()["id"])
    return result
