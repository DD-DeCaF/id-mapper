# Copyright 2018 Novo Nordisk Foundation Center for Biosustainability, DTU.
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

FROM dddecaf/wsgi-base:alpine

ENV APP_USER=giraffe

ARG UID=1000
ARG GID=1000

ARG CWD="/app"

ENV PYTHONPATH="${CWD}/src"

RUN addgroup -S -g "${GID}" "${APP_USER}" && \
    adduser -S -H -u "${UID}" -G "${APP_USER}" "${APP_USER}"

WORKDIR "${CWD}"

# py2neo dependencies
RUN apk add --no-cache g++ libffi-dev openssl-dev

COPY requirements ./requirements

RUN pip-sync requirements/requirements.txt

COPY . "${CWD}/"

RUN chown -R "${APP_USER}:${APP_USER}" "${CWD}"
