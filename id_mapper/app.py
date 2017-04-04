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


from id_mapper.stubs import IdMapperQueryRequest, IdMapperQueryResponse
from id_mapper.graph import query_identifiers


class IdMapping(Service):
    graph = Graph("{}:{}".format(os.environ['ID_MAPPER_API'], os.environ['ID_MAPPER_PORT']),
                  password=os.environ['ID_MAPPER_PASSWORD'])

    @http.POST(
        './query',
        description='Query entity by list of identifiers and a database name to get '
                    'all the matching identifiers from another database'
    )
    def query(self, request: IdMapperQueryRequest) -> IdMapperQueryResponse:
        return IdMapperQueryResponse(ids=query_identifiers(
            self.graph, object_type=request.type, object_ids=list(request.ids),
            db_from=request.db_from, db_to=request.db_to
        ))


venom = Venom()
venom.add(IdMapping)
venom.add(ReflectService)

app = create_app(venom)

if __name__ == '__main__':
    web.run_app(app)
