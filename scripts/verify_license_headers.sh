#!/usr/bin/env bash

# Copyright (c) 2017, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
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

set -eu

PATTERN="Novo Nordisk Foundation Center for Biosustainability"
RET=0

for file in $(find $@ -name '*.py')
do
  grep "${PATTERN}" ${file} >/dev/null
  if [[ $? != 0 ]]
  then
    echo "Source code file ${file} seems to be missing a license header"
    RET=1
  fi
done
exit ${RET}
