#!/bin/bash

/home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script get_num_inputs.py $1 $2

# COOKIE_FILE_PATH="/home/zhuang/osparc/services/$2"
# mkdir $COOKIE_FILE_PATH
# cd $COOKIE_FILE_PATH

touch num_params.txt

python3 -m venv .venv
source .venv/bin/activate
pip install cookiecutter
pip install PyYAML

python3 create_cookie.py $2
python3 customize_cookie.py $2
/home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script run_model.py $1 $2



