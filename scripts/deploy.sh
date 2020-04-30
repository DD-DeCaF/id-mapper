#!/usr/bin/env bash

# Copyright 2018-2020 Novo Nordisk Foundation Center for Biosustainability, DTU.
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

set -xeu

if [ "${TRAVIS_BRANCH}" = "master" ]; then
  DEPLOYMENT=id-mapper-production
else
  echo "Skipping deployment for branch ${TRAVIS_BRANCH}"
  exit 0
fi

kubectl set image deployment/${DEPLOYMENT} web=${IMAGE}:${BUILD_TAG}
