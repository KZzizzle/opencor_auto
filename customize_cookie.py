import pickle
import yaml
import sys
import json

from pathlib import Path


project_name = str(sys.argv[2])
model_file = str(sys.argv[1])

#=======================================================================
# Edit metadata file
#=======================================================================

# read constants and state fields for the particular model 
with open('model_inputs.txt', 'rb') as handle:
    model_inputs = pickle.loads(handle.read())

metadata_file = Path(project_name+"/metadata/metadata_copy.yml")

with metadata_file.open("r") as fp:
    metadata_dict = yaml.safe_load(fp)


# replace default input fields in metadata.yml with model constants and states
metadata_dict["inputs"] = {}

metadata_dict["inputs"].update({
    "starttime": {
        "displayOrder": 1,
        "label": "simulation start time",
        "description": "starting time of simulation (s)",
        "type": "float",
        "defaultValue":0
        }
        })
metadata_dict["inputs"].update({
    "endtime": {
        "displayOrder":2,
        "label":"simulation ending time",
        "description": "ending time of simulation (s)",
        "type": "float",
        "defaultValue": 1000
        }
        })
metadata_dict["inputs"].update({
    "timeincr": {
        "displayOrder":3,
        "label":"simulation time increment",
        "description": "time step for running simulation (s)",
        "type": "float",
        "defaultValue": 1
        }
        })


for key in model_inputs:    
    # print(key)
    metadata_dict["inputs"][key] = {
        "displayOrder": list(model_inputs.keys()).index(key)+4,
        "label":key.split("/")[-1],
        "description": key,
        "type": "float",
        "defaultValue": model_inputs[key]
    }

metadata_dict["outputs"] = {}
metadata_dict["outputs"].update({
    "model_output": {
            "displayOrder": 1,
            "label": "Simulation result (CSV-format)",
            "description": "The time-series output of the simulation in comma-delimited .csv format",
            "type": "data:application/csv",
            "fileToKeyMap": {
                "outputs.csv":"model_output"
                }
            }
            })

# write to metadata file
metadata_file_copy = Path(project_name+"/metadata/metadata.yml")
with metadata_file_copy.open("w") as fp:
    yaml.safe_dump(metadata_dict, fp, default_flow_style=False)

#=======================================================================
# write validation input file for constants and states
#=======================================================================

input_dict={}
for key in metadata_dict["inputs"]:    
    input_dict.update({key: metadata_dict["inputs"][key]["defaultValue"]})

inputvalidation_file = Path(project_name+"/validation/input/inputs.json")
with inputvalidation_file.open("w") as fpin:
    json.dump(input_dict, fpin, indent=4)

#=======================================================================
# edit the Dockerfile
#=======================================================================

Docker_file = Path(project_name+"/docker/ubuntu/Dockerfile_copy")
Docker_fileout = Path(project_name+"/docker/ubuntu/Dockerfile")

# additional text to install dependencies
addtext = """
RUN apt-get -qq update && apt-get install -y \\
 libpulse-mainloop-glib0 \\
 libfontconfig1 \\
 libfreetype6 \\
 libx11-6 \\
 libx11-xcb1 \\
 libxext6 \\
 libxslt1.1 \\
 sqlite3

RUN apt-get -qq update && \\
    apt-get install -y \\
      jq    &&\\
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/opencor

# Taking the OpenCOR binary from the web, this binary is Python enabled.  This method fails to complete for me so enabling the alternative method.
ADD https://github.com/dbrnz/opencor/releases/download/snapshot-2019-06-11/OpenCOR-2019-06-11-Linux.tar.gz /home/opencor/
RUN tar -xvzf OpenCOR-2019-06-11-Linux.tar.gz && \\
    rm OpenCOR-2019-06-11-Linux.tar.gz

"""
# text to add environment variables for project name and model file
envtext = "ENV PROJECT_NAME=\"" + project_name + "\"\nENV MODEL_FILE=\"" + model_file + "\"\n"

# make the changes in the Docker file
with Docker_file.open("r") as d_file:
    buf = d_file.readlines()

with Docker_fileout.open("w") as dout_file:
    for line in buf:
        if line == "#     docker run demo:prod\n":
            line = line + addtext + envtext
        dummyvar = dout_file.write(line)


# copy code and model into the source directory
with Docker_fileout.open("r") as d_file:
    buf = d_file.readlines()

with Docker_fileout.open("w") as dout_file:
    for line in buf:
        if line .__contains__("RUN adduser "):
            line = line + "\nCOPY --chown=scu:scu ./src/"+ project_name + "/run_model.py /home/" + project_name + "/\n"
            line = line + "COPY --chown=scu:scu ./src/" + project_name + "/" + model_file + " /home/" + project_name + "/\n"
        placeholder = dout_file.write(line)

#=======================================================================
# edit execute.sh
#=======================================================================

execute_file = Path(project_name+"/service.cli/execute_copy.sh")
execute_fileout = Path(project_name+"/service.cli/execute.sh")

executetext = ("\n/home/opencor/OpenCOR-2019-06-11-Linux/bin/OpenCOR -c PythonRunScript::script run_model.py "
+ "${INPUT_FOLDER}/inputs.json /home/" + project_name + "/" + model_file 
+ "\n\ncp outputs.csv ${OUTPUT_FOLDER}/outputs.csv\n\nenv | grep INPUT")


with execute_file.open("r") as e_file:
    ebuf = e_file.readlines()

lastline = len(ebuf)
with execute_fileout.open("w") as eout_file:
    for index, line in enumerate(ebuf):
        if line .__contains__("# For example: input_1 -> $INPUT_1"):
            line = line + executetext
            lastline = index
        if index <= lastline:
            dummyvar = eout_file.write(line)


# infile = open('input.txt','r').readlines()
# with open('output.txt','w') as outfile:
#     for index,line in enumerate(infile):
#         if index != 7:
#             outfile.write(line)