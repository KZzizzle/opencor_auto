# OpenCOR Model Creation with cookiecutter for o2S2PARC

Creates a "cookie" that takes OpenCOR compatible models (.cellML or .sedML) and turns them into o2S2PARC services. 

## Software Requirements
* python3
* make (pip install make)
* docker
* docker-compose
* git (for adding the newly created model into o2S2PARC repositories)

## Code requirements
Must have checked out osparc-services from ITISFoundation: https://github.com/ITISFoundation/osparc-services

## Usage
All you must specify are:
1. The path to your .cellML or .sedML file
2. The name of your future service 

To run, in terminal: ```. create_opencor_service.sh path_to_model name_of_service```

Example: 
```. create_opencor_service.sh /home/username/mymodel.cellml service_example```
