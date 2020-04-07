import pickle
import yaml
import sys

from pathlib import Path


with open('model_inputs.txt', 'rb') as handle:
    model_inputs = pickle.loads(handle.read())

metadata_file = Path("demo/metadata/metadata.yml")

with metadata_file.open("r") as fp:
    metadata_dict = yaml.safe_load(fp)


metadata_dict["inputs"] = {}
for key in model_inputs:    
    print(key)
    metadata_dict["inputs"][key] = {
        "displayOrder": list(model_inputs.keys()).index(key),
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

print(metadata_dict)
metadata_file_copy = Path("demo/metadata/metadata_copy.yml")
with metadata_file_copy.open("w") as fp:
    yaml.safe_dump(metadata_dict, fp)
