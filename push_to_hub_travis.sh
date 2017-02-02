#!/bin/bash
set -ev
REPO="dddecaf/id-mapper"
GIT_MASTER_HEAD_SHA=$(git rev-parse --short=12 --verify HEAD)
BRANCH=$TRAVIS_BRANCH
docker build -f Dockerfile -t $REPO:$BRANCH .
docker tag $REPO:$BRANCH $REPO:$GIT_MASTER_HEAD_SHA
docker push $REPO:$BRANCH
docker push $REPO:$GIT_MASTER_HEAD_SHA
if [ $BRANCH = "master" ]; then
   docker tag $REPO:$BRANCH $REPO:latest
   docker push $REPO:latest
fi