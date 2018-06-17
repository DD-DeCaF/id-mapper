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

METANETX_URL = 'http://www.metanetx.org/cgi-bin/mnxget/mnxref'
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(asctime)s [%(levelname)s] [%(name)s] %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
        },
    },
    'loggers': {
        # All loggers will by default use the root logger below (and
        # hence be very verbose). To silence spammy/uninteresting log
        # output, add the loggers here and increase the loglevel.
        'asyncio': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'sentry'],
    },
}
