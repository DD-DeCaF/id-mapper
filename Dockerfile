# Copyright (c) 2018-2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG BASE_TAG=alpine

FROM dddecaf/wsgi-base:${BASE_TAG}

ARG BASE_TAG=alpine
ARG BUILD_COMMIT

LABEL dk.dtu.biosustain.id-mapper.alpine.vendor="Novo Nordisk Foundation \
Center for Biosustainability, Technical University of Denmark"
LABEL maintainer="niso@biosustain.dtu.dk"
LABEL dk.dtu.biosustain.id-mapper.alpine.build.base-tag="${BASE_TAG}"
LABEL dk.dtu.biosustain.id-mapper.alpine.build.commit="${BUILD_COMMIT}"

ARG CWD="/app"

ENV PYTHONPATH="${CWD}/src"

WORKDIR "${CWD}"

COPY requirements ./requirements/

RUN set -eux \
    # Add py2neo build dependencies.
    && apk add --no-cache --virtual .build-deps build-base libffi-dev openssl-dev \
    && pip install -r requirements/requirements.txt \
    # Remove build dependencies to reduce layer size.
    && rm -rf /root/.cache/pip \
    && apk del .build-deps

COPY . ./

RUN chown -R "${APP_USER}:${APP_USER}" .

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.py", "id_mapper.wsgi:app"]
