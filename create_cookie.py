
from cookiecutter.main import cookiecutter
import sys


def main(servicename):
    file = open("num_params.txt", "r")
    num_inputs = int(file.read())+3

    cookiecutter('https://github.com/ITISFoundation/cookiecutter-osparc-service', extra_context={
        'docker_base':"ubuntu:18.04",
        'number_of_inputs': num_inputs, 
        'affiliation': 'ITIS Foundation'
        'project_name': servicename,
        'author_name': "Katie Zhuang",
        'author_email': "zhuang@itis.swiss",
        'project_type': "computational",
        'number_of_outputs': 1,
        'git_username': "KZzizzle"
    })
    return 0

def usage():
    print("Usage: docker run KZzizzle/opencor-load <str> ")
    print("  where <str> is the name of the model that you want to run. It must be on the input folder.")


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)  # Script name.
    modelpath = "simulation-experiment.sedml"

    try:
        servicename = str(args.pop(0))
    except ValueError:
        print('ValueError in inputs')
        usage()
        sys.exit(2)
    except IndexError:
        print('indexError in inputs')
        usage()
        sys.exit(2)

    rc = main(servicename)