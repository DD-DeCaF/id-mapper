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
import re
from collections import namedtuple
from multiprocessing import Pool

from py2neo import Graph

from id_mapper.graph import insert_pairs


N_PROCESSES = 4
N_LINES = 50

with open("data/ecodata.txt") as f:
    lines = list(f.readlines())

DATABASES = [
    "ecogene",
    "eck",
    "name",
    "syn",
    "genbank",
    "sp",
    "blattner",
    "asap",
    "genobase",
    "cg",
]
Pair = namedtuple("Pair", ["metabolite", "database"])


def process_piece(chunk):
    for line in chunk:
        info = dict(zip(DATABASES, line.split("\t")))
        to_delete = []
        for key, value in info.items():
            if value in ("None", "Null", "Null\n", "null", "null\n"):
                to_delete.append(key)
            else:
                info[key] = info[key].strip("'; ").strip()
                info[key] = re.sub("\(\w\.\w\.\)", "", info[key])
        for key in to_delete:
            info.pop(key)
        info["name"] = [info["name"]]
        if "syn" in info:
            info["name"].extend(info["syn"].split(", "))
            info.pop("syn")
            info["name"] = [i.strip() for i in info["name"]]
        pair_1 = Pair(info["blattner"], "blattner")
        for key, value in info.items():
            if key != "blattner":
                if key != "name":
                    insert_pairs(
                        graph,
                        "Gene",
                        pair_1,
                        Pair(value, key),
                        organism="ecoli",
                    )
                else:
                    for n in value:
                        insert_pairs(
                            graph,
                            "Gene",
                            pair_1,
                            Pair(n, key),
                            organism="ecoli",
                        )


graph = Graph(
    "{}:{}".format(os.environ["ID_MAPPER_API"], os.environ["ID_MAPPER_PORT"]),
    password=os.environ["ID_MAPPER_PASSWORD"],
)

with Pool(processes=N_PROCESSES) as pool:
    pool.map(
        process_piece,
        [lines[i : i + N_LINES] for i in range(0, len(lines), N_LINES)],
    )
