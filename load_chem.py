import os
from id_mapper.metanetx import make_pairs
from id_mapper.graph import insert_pairs
from py2neo import Graph

from multiprocessing import Pool

N_PROCESSES = 20
N_LINES = 100

with open('chem_xref_mini_1.tsv') as f:
    lines = list(f.readlines())


def process_piece(chunk):
    for line in chunk:
        x, y = make_pairs(line)
        if x.metabolite != y.metabolite:
            insert_pairs(graph, 'Metabolite', x, y)

graph = Graph(host=os.environ['DB_PORT_7687_TCP_ADDR'], password=os.environ['NEO4J_PASSWORD'])

with Pool(processes=N_PROCESSES) as pool:
    pool.map(process_piece, [lines[i:i+N_LINES] for i in range(0, len(lines), N_LINES)])

