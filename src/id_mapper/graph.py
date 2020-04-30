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

import logging
import os
import time

from py2neo import Graph
from py2neo.packages.httpstream.http import SocketError


logger = logging.getLogger(__name__)

connected = False
while not connected:
    try:
        GRAPH = Graph(
            os.environ["ID_MAPPER_API"],
            http_port=int(os.environ["ID_MAPPER_PORT"]),
            user=os.environ["ID_MAPPER_USER"],
            password=os.environ["ID_MAPPER_PASSWORD"],
        )
        logger.info("Connected to graph db")
        connected = True
    except SocketError as error:
        logger.info(
            f"{str(error)}: Could not connect to database, retrying in "
            "5 seconds..."
        )
        time.sleep(5)


def query_identifiers(
    object_type, object_ids, db_from, db_to, max_separation=3
):
    """Return id for given metabolite from the corresponding database

    :param object_type: The type of the object, e.g. Metabolite, Gene or Reaction.
    :param object_ids: list of identifiers
    :param db_from: database name, f.e "bigg"
    :param db_to: database name, f.e "mnx"
    :param max_separation: max degree of separation to search. Decided by link structure, at time of writing we don't
    expect degree separation more than 3
    :return:
    """
    query = """MATCH (n:{object_type})-[:IS*..{separation}]->(b:{object_type})
             WHERE n.db_name = {{db_from}} AND b.db_name = {{db_to}} AND n.id IN {{identifiers}}
             RETURN n.id AS from, collect(distinct b.id) AS to""".format(
        separation=int(max_separation), object_type=object_type
    )  # possible to parametrize with cypher?

    logger.info(query)
    data = GRAPH.data(
        query,
        parameters={
            "identifiers": object_ids,
            "db_from": db_from,
            "db_to": db_to,
        },
    )
    result = {item["from"]: item["to"] for item in data}
    return result
