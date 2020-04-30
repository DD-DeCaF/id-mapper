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

"""Expose the main Flask-RESTPlus application."""

import logging
import logging.config

from flask import Flask
from flask_cors import CORS
from raven.contrib.flask import Sentry
from werkzeug.middleware.proxy_fix import ProxyFix

from . import errorhandlers


app = Flask(__name__)


def init_app(application):
    """Initialize the main app with config information and routes."""
    from id_mapper.settings import current_config

    application.config.from_object(current_config())

    # Configure logging
    logging.config.dictConfig(application.config["LOGGING"])

    # Configure Sentry
    if application.config["SENTRY_DSN"]:
        sentry = Sentry(
            dsn=application.config["SENTRY_DSN"],
            logging=True,
            level=logging.ERROR,
        )
        sentry.init_app(application)

    # Add routes and resources.
    from id_mapper import resources

    resources.init_app(application)

    # Add CORS information for all resources.
    CORS(application)

    # Register error handlers
    errorhandlers.init_app(application)

    # Please keep in mind that it is a security issue to use such a middleware
    # in a non-proxy setup because it will blindly trust the incoming headers
    # which might be forged by malicious clients.
    # We require this in order to serve the HTML version of the OpenAPI docs
    # via https.
    application.wsgi_app = ProxyFix(application.wsgi_app)
