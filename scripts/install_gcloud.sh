#!/usr/bin/env bash

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

set -xeu

if [ ! -d "${HOME}/google-cloud-sdk" ]; then
  curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-200.0.0-linux-x86_64.tar.gz | tar -zx
  ./google-cloud-sdk/install.sh --quiet
fi
source ./google-cloud-sdk/path.bash.inc
echo ${GCLOUD_KEY} | base64 --decode > travis-ci.key.json
gcloud --quiet config set project dd-decaf-cfbf6
gcloud --quiet config set compute/zone europe-west1-b
gcloud --quiet auth activate-service-account ${GCLOUD_EMAIL} --key-file travis-ci.key.json
docker login -u _json_key --password-stdin https://gcr.io < travis-ci.key.json
