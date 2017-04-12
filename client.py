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

import asyncio

from id_mapper.stubs import IDMappingStub, QueryRequest
from venom.rpc.comms.aiohttp import Client

client = Client(IDMappingStub, 'http://localhost')

async def find_match(met_id, db_from, db_to):
    response = await client.invoke(
        IDMappingStub,
        IDMappingStub.query,
        QueryRequest(id=met_id, db_from=db_from, db_to=db_to))
    print('response:', response.message)

loop = asyncio.get_event_loop()
loop.run_until_complete(find_match('MNXR1', 'mnx', 'bigg'))