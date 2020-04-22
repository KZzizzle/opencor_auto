#!/bin/bash

# first argument is the cellML or sedML path, second argument is the name of the project. 

# /home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script get_num_inputs.py $1 $2

# python3 -m venv .venv
# source .venv/bin/activate
# pip install cookiecutter
# pip install PyYAML

# python3 create_cookie.py $2
# cp "$2/docker/ubuntu/Dockerfile" "$2/docker/ubuntu/Dockerfile_copy"
# cp "$2/service.cli/execute.sh" "$2/service.cli/execute_copy.sh"
# cp "$2/metadata/metadata.yml" "$2/metadata/metadata_copy.yml"

pushd $2
make .venv
source .venv/bin/activate
# make build
popd

cp $1 "$2/src/$2/"
cp run_model.py "$2/src/$2/"
python3 customize_cookie.py "${1##*/}" $2
pushd $2
make build
make up
popd

# /home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script run_model.py $1 $2



