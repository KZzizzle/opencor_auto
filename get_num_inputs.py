import OpenCOR
import sys
import pickle

# modelurl = ('LoeweLutzFabbriSeveri.cellml')
# modelurl = input("Enter the model url: ")
# modelurl = 'https://models.physiomeproject.org/workspace/bagci_2008/@@rawfile/ca2dff72d386a14f5540e39363286bf0f40070d3/bagci_2008a.cellml'
# modelurl = 'https://models.physiomeproject.org/workspace/guyton_pulmonary_oxygen_uptake_2008/rawfile/b9a3c89bce95b78d1c3006cb4bbafc90a5222f16/guyton_pulmonary_oxygen_uptake_2008.cellml'


def main(modelpath, servicename):

    return_code = 0
    if modelpath.endswith("cellml") or modelpath.endswith("sedml"):
        model = OpenCOR.openSimulation(modelpath)
    else:
        print('Invalid file type: only .cellml and .sedml accepted')
        return_code=3
    try: 
        print('try getting simulation')
        c = model.data().constants()
        s = model.data().states()
        num_inputs = len(s)+len(c)
        print(num_inputs)
        if num_inputs<1:
            print('this model has no editable input values')
        else:
            numinputs = open("num_params.txt","w") 
            numinputs.write(str(num_inputs))
            numinputs.close()
            
            model_inputs =c.copy()
            for entry in c:
                model_inputs[entry]=c[entry]
            s_copy =s.copy()
            for entry in s:
                s_copy[entry]=s[entry]
            model_inputs.update(s_copy)    

            with open('model_inputs.txt', 'wb') as f:
                pickle.dump(model_inputs, f)

    except:
        print('Error during model loading')
        return_code = 2


    return return_code


def usage():
    print("Usage: docker run KZzizzle/opencor-load <str> ")
    print("  where <str> is the name of the model that you want to run. It must be on the input folder.")


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)  # Script name.
    modelpath = "simulation-experiment.sedml"

    try:
        modelpath = str(args.pop(0))
        servicename = str(args.pop(0))
    except ValueError:
        print('ValueError in inputs')
        usage()
        sys.exit(2)
    except IndexError:
        print('indexError in inputs')
        usage()
        sys.exit(2)

    rc = main(modelpath, servicename)