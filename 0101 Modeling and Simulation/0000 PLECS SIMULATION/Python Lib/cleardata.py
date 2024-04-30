
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                           ________                       __      __       
#?                                          / ____/ /__  ____ ______   ____/ /___ _/ /_____ _
#?                                         / /   / / _ \/ __ `/ ___/  / __  / __ `/ __/ __ `/
#?                                        / /___/ /  __/ /_/ / /     / /_/ / /_/ / /_/ /_/ / 
#?                                        \____/_/\___/\__,_/_/      \__,_/\__,_/\__/\__,_/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------                                       
import os
#?----------------------------------------------------------------------------------------------------------------------------------------
folder_paths = [
                (os.path.join(os.getcwd(), "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV")).replace("\\", "/") ,
                (os.path.join(os.getcwd(), "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html")).replace("\\", "/") ,
                (os.path.join(os.getcwd(), "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log")).replace("\\", "/") ,
                (os.path.join(os.getcwd(), "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces")).replace("\\", "/") 
                ]
#?----------------------------------------------------------------------------------------------------------------------------------------
def delete_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Error: The provided path is not a directory.")
        return
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def clear_data_folders():
    for folder_path in folder_paths:
        delete_files_in_folder(folder_path)
#?----------------------------------------------------------------------------------------------------------------------------------------