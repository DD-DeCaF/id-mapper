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

import logging
import sys

from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

from . import settings


logger = logging.getLogger('service-id-mapper')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(logging.DEBUG)

# Configure Raven to capture warning logs
raven_client = Client(settings.SENTRY_DSN)
handler = SentryHandler(raven_client)
handler.setLevel(logging.WARNING)
setup_logging(handler)
