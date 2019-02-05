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

"""Implement RESTful API endpoints using resources."""

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.extension import FlaskApiSpec

from .graph import query_identifiers
from .schemas import Query, Response


def init_app(app):
    """Register API resources on the provided Flask application."""
    docs = FlaskApiSpec(app)
    app.add_url_rule('/healthz', view_func=healthz)
    app.add_url_rule('/query', view_func=query, methods=['POST'])
    docs.register(query, endpoint=query.__name__)


def healthz():
    """
    Return an empty, successful response for readiness checks.

    A successful response signals that the app is initialized and ready to
    receive traffic. The main use case is for apps with slow initialization, but
    external dependencies like database connections can also be tested here.
    """
    return ""


@doc(description="Query entity by list of identifiers and a database name to "
                 "get all the matching identifiers from another database")
@use_kwargs(Query)
@marshal_with(Response, code=200)
def query(ids, type, db_from, db_to):
    return {'ids': query_identifiers(
        object_type=type,
        object_ids=list(ids),
        db_from=db_from,
        db_to=db_to,
    )}
