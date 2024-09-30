import os
import importlib.util

module_name = 'basicsr'
spec = importlib.util.find_spec(module_name)

if spec is not None:
    basicsr_path = os.path.dirname(spec.origin)
    
    # path file degradations.py
    file_path = os.path.join(basicsr_path, 'data', 'degradations.py')

    
    if os.path.exists(file_path):
        new_import_statement = "from torchvision.transforms.functional import rgb_to_grayscale\n"

        with open(file_path, 'r') as file:
            lines = file.readlines()

        if len(lines) >= 8:
            lines[7] = new_import_statement  

        with open(file_path, 'w') as file:
            file.writelines(lines)

        print("Replace  successfully!")

        with open(file_path, 'r') as file:
            updated_lines = file.readlines() 
    else:
        print(f"Can't not find: {file_path}")
else:
    print(f"Can't not find module: {module_name}")