import pickle
import yaml
import sys
import json

from pathlib import Path


project_name = str(sys.argv[1])


# read constants and state fields for the particular model 
with open('model_inputs.txt', 'rb') as handle:
    model_inputs = pickle.loads(handle.read())

metadata_file = Path(project_name+"/metadata/metadata.yml")

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



    # metadata_dict["inputs"][key] = metadata_dict["inputs"].pop(service_input)
    # metadata_dict["inputs"][key]["label"] = labelstr[-1]
    # metadata_dict["inputs"][key]["description"] = key
    # metadata_dict["inputs"][key]["type"] = "float"
    # metadata_dict["inputs"][key]["defaultValue"] = model_inputs[key]

# write to metadata file
metadata_file_copy = Path(project_name+"/metadata/metadata_copy.yml")
with metadata_file_copy.open("w") as fp:
    yaml.safe_dump(metadata_dict, fp, default_flow_style=False)


# write validation input file for constants and states
input_dict={}
for key in metadata_dict["inputs"]:    
    input_dict.update({key: metadata_dict["inputs"][key]["defaultValue"]})


inputvalidation_file = Path(project_name+"/validation/input/inputs_test.json")
with inputvalidation_file.open("w") as fpin:
    json.dump(input_dict, fpin, indent=4)