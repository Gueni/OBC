
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?               _    ____________  _____ ________  _   _______
#?              | |  / / ____/ __ \/ ___//  _/ __ \/ | / / ___/
#?              | | / / __/ / /_/ /\__ \ / // / / /  |/ /\__ \
#?              | |/ / /___/ _, _/___/ // // /_/ / /|  /___/ /
#?              |___/_____/_/ |_|/____/___/\____/_/ |_//____/
#?              
#? Name:        versions.py
#? Purpose:     Get imported libraries,their versions,fill a requirements.txt
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/01/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------  
#? ------------------------------------------------------------------------------- 


import os
import re
import pkg_resources
from typing import List

def extract_imports_from_file(filepath: str) -> List[str]:
    imports = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Find library names in import statements
                match = re.findall(r'(?:import|from)\s+([a-zA-Z_][\w.]+)', line)
                if match:
                    imports.extend(match)
    return imports

def get_installed_version(package_name: str) -> str:

    try:
        distribution = pkg_resources.get_distribution(package_name)
        return distribution.version
    except pkg_resources.DistributionNotFound:
        return 'unknown'

def populate_requirements_txt(project_dir: str, requirements_file: str) -> None:
    imports = set()
    # Walk through all files in the project directory
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                file_imports = extract_imports_from_file(filepath)
                imports.update(file_imports)
    # Get versions and write to requirements.txt
    with open(requirements_file, 'w') as req_file:
        # Determine the maximum length of package names
        max_name_length = max(len(imp) for imp in imports) if imports else 0
        
        for imp in sorted(imports):
            version = get_installed_version(imp)
            # Use ljust to align package names to the right
            line = f'{imp.ljust(max_name_length)} == {version}\n'
            req_file.write(line)

    print(f'Requirements file "{requirements_file}" has been populated.')

project_directory = 'D:/WORKSPACE/OBC/OBC/' 
requirements_txt  = 'D:/WORKSPACE/OBC/OBC/requirements.txt'
populate_requirements_txt(project_directory, requirements_txt)