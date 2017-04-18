import os
import argparse

from collections import namedtuple
from py2neo import Graph
from id_mapper.graph import insert_pairs
from multiprocessing import Pool


N_PROCESSES = 4
N_LINES = 50

graph = Graph("{}:{}".format(os.environ['ID_MAPPER_API'], os.environ['ID_MAPPER_PORT']),
              password=os.environ['ID_MAPPER_PASSWORD'])


def make_pairs(line):
    x, y = line.strip().split(',')
    db_x, id_x = x.split(':')
    db_y, id_y = y.split(':')
    return Pair(id_x, db_x.lower()), Pair(id_y, db_y.lower())


def process_piece(chunk):
    for line in chunk:
        a, b = make_pairs(line)
        if a.metabolite != b.metabolite:
            insert_pairs(graph, 'Metabolite', a, b)


parser = argparse.ArgumentParser(description='Load a csv with triples')
parser.add_argument('file', type=str, help='the input csv file, 2 columns left and right identifier '
                                           'connected with is-a relationship')
parser.add_argument('type', type=str, choices=['metabolite', 'gene', 'reaction'])
args = parser.parse_args()

Pair = namedtuple('Pair', [args.type, 'database'])

with open(args.file) as csv:
    lines = list(csv.readlines())


with Pool(processes=N_PROCESSES) as pool:
    pool.map(process_piece, [lines[i:i + N_LINES] for i in range(0, len(lines), N_LINES)])
