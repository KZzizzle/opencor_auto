#!/bin/bash

# first argument is the cellML or sedML path, second argument is the name of the project. 

/home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script get_num_inputs.py $1 $2

python3 -m venv .venv
source .venv/bin/activate
pip install cookiecutter
pip install PyYAML

python3 create_cookie.py $2

# in the new directory, make the virtual environment and build the cookie
make -C $2 .venv
make -C $2 devenv
source "$2/.venv/bin/activate"
make -C $2 build

cp $1 "$2/src/$2/"
cp run_model.py "$2/src/$2/"
python3 customize_cookie.py "${1##*/}" $2
chmod +x "$2/service.cli/execute.sh"

make -C $2 build
make -C $2 up
cp "$2/.tmp/output/outputs.csv" "$2/validation/output/"
rm "$2/validation/output/outputs.json"

make -C $2 tests

deactivate
# # /home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script run_model.py demo/validation/input/inputs.json demo/src/demo/guyton_antidiuretic_hormone_2008.cellml demo/src/demo/input_keymap.json



