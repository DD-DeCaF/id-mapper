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

from venom.fields import String, Repeat
from venom.message import Message
from venom.rpc import Stub, http


class QueryRequest(Message):
    id = String(description='Entity ID')
    db_from = String(description='Database name for the entity ID')
    db_to = String(description='Database name to map against')


class QueryResponse(Message):
    ids = Repeat(String(), description='List of matching IDs')


class IDMappingStub(Stub):
    @http.GET('./query')
    def query(self, request: QueryRequest) -> QueryResponse:
        raise NotImplementedError
