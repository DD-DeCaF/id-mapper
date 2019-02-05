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

"""Provide settings for different deployment scenarios."""

import os

import werkzeug.exceptions


__all__ = ("Development", "Testing", "Production")


def current_config():
    """Return the appropriate configuration object based on the environment."""
    if os.environ['ENVIRONMENT'] in ['production', 'staging']:
        return Production()
    elif os.environ['ENVIRONMENT'] == 'testing':
        return Testing()
    elif os.environ['ENVIRONMENT'] == 'development':
        return Development()
    else:
        raise KeyError(f"Unknown environment '{os.environ['ENVIRONMENT']}'")


class Default:
    """Set the default configuration for all environments."""

    def __init__(self):
        """
        Initialize the default configuration.

        We chose configuration by instances in order to avoid ``KeyError``s
        from environments that are not active but access
        ``os.environ.__getitem__``.
        """
        self.DEBUG = True
        self.SECRET_KEY = os.urandom(24)
        self.BUNDLE_ERRORS = True
        self.APISPEC_TITLE = "id-mapper"
        self.APISPEC_SWAGGER_UI_URL = "/"
        self.CORS_ORIGINS = os.environ['ALLOWED_ORIGINS'].split(',')
        self.SENTRY_DSN = os.environ.get('SENTRY_DSN')
        self.SENTRY_CONFIG = {
            'ignore_exceptions': [
                werkzeug.exceptions.BadRequest,
                werkzeug.exceptions.Unauthorized,
                werkzeug.exceptions.Forbidden,
                werkzeug.exceptions.NotFound,
                werkzeug.exceptions.MethodNotAllowed,
            ]
        }
        self.LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': "%(asctime)s [%(levelname)s] [%(name)s] "
                              "%(message)s",
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
            },
            'loggers': {
                # All loggers will by default use the root logger below (and
                # hence be very verbose). To silence spammy/uninteresting log
                # output, add the loggers here and increase the loglevel.
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        }
        self.METANETX_URL = 'http://www.metanetx.org/cgi-bin/mnxget/mnxref'


class Development(Default):
    """Development environment configuration."""

    pass


class Testing(Default):
    """Testing environment configuration."""

    def __init__(self):
        """Initialize the testing environment configuration."""
        super().__init__()
        self.TESTING = True


class Production(Default):
    """Production environment configuration."""

    def __init__(self):
        """
        Initialize the production environment configuration.

        Require a secret key to be defined and make logging slightly less
        verbose.
        """
        super().__init__()
        self.DEBUG = False
        self.SECRET_KEY = os.environ['SECRET_KEY']
        self.LOGGING['root']['level'] = 'INFO'
