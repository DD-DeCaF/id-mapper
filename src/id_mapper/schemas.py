# Copyright (c) 2017, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Marshmallow schemas for marshalling the API endpoints."""

from marshmallow import Schema, fields


class Query(Schema):
    # Identifiers to query
    ids = fields.List(fields.String(), required=True)
    # The type of the entity, i.e., Metabolite, Gene or Reaction
    type = fields.String(required=True)
    # Database name for the entity ID
    db_from = fields.String(required=True)
    # Database name to map against
    db_to = fields.String(required=True)

    class Meta:
        strict = True


class Response(Schema):
    # Mapping between each query identifier and the found matches
    # E.g., {'atp': ['C00002', 'D08646']}
    ids = fields.Raw()

    class Meta:
        strict = True
