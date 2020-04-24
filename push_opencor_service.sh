#!/bin/bash

# echo "What name should this folder have?"
# read FOLDER_NAME

export FOLDER_NAME="oc-guytonmodel"

# cp "$1/.github/workflows/github-ci.yml" "$1/.github/workflows/github-ci_copy.yml" 
python3 edit_ciyaml.py $1 ${FOLDER_NAME}

cp -R "$1/." "../osparc-services/services/$FOLDER_NAME"
# cd "../osparc-services/services/$FOLDER_NAME"