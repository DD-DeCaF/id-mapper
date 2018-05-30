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

from . import raven_client


async def raven_middleware(app, handler):
    """aiohttp middleware which captures any uncaught exceptions to Sentry before re-raising"""
    async def middleware_handler(request):
        try:
            return await handler(request)
        except Exception:
            raven_client.captureException()
            raise
    return middleware_handler
