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
from id_mapper import logger

from .middleware import raven_middleware


class IdMapping(Service):
    logger.info('connect to graph-db at {}'.format(os.environ['ID_MAPPER_API']))
    graph = Graph(os.environ['ID_MAPPER_API'],
                  http_port=int(os.environ['ID_MAPPER_PORT']),
                  user=os.environ['ID_MAPPER_USER'],
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


venom = Venom(version='0.2.0', title='ID Mapper')
venom.add(IdMapping)
venom.add(ReflectService)

app = create_app(venom, web.Application(middlewares=[raven_middleware]))

if __name__ == '__main__':
    web.run_app(app)
