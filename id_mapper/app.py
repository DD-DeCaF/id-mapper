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
from aiohttp import web

from venom.rpc import Service, Venom
from venom.rpc.comms.aiohttp import create_app
from venom.rpc.method import http
from venom.rpc.reflect.service import ReflectService
from venom.exceptions import NotFound

from id_mapper.stubs import QueryRequest, QueryResponse
from id_mapper.graph import find_match, NoSuchNode


class IDMapping(Service):
    @http.GET(
        './query',
        description='Query entity by id and database name to get '
                    'all the matching IDs from another database'
    )
    def query(self, request: QueryRequest) -> QueryResponse:
        graph = Graph(
            host=os.environ['DB_PORT_7687_TCP_ADDR'],
            password=os.environ['NEO4J_PASSWORD']
        )
        try:
            return QueryResponse(ids=find_match(
                graph, request.id, request.db_from, request.db_to
            ))
        except NoSuchNode as e:
            raise NotFound(str(e))

venom = Venom()
venom.add(IDMapping)
venom.add(ReflectService)


app = create_app(venom)

if __name__ == '__main__':
    web.run_app(app)
