"""batch_ik.py

Tool for batch processing trc files using OpenSim's IK solver
"""
import os
import config
from utils.osim_utils import run_osim_tools


# First we search for static file that need scaling. We do this first
# as we will need our scaled models to run IK on other motion trials
for root, dirs, files in os.walk(config.PATH):
    for file in files:
        # If we find a static file we can scale it if the config
        # file specifies this
        if config.SCALE_MODEL and config.STATIC_NAME in root and file.endswith(".trc"):
            # construct full file path for this file
            temp_path = os.path.join(root, file)
            
            # if the .trc file is called "markers.trc" we will assume is is a markers file,
            # otherwise, we will assume it was a markerless file.
            if file == "markers.trc":
                config.IS_MARKERLESS = False
            else:
                config.IS_MARKERLESS = True
            
            
            print(f"\n[INFO] - Scaling model: {temp_path}\n")
            run_osim_tools(temp_path, config, job="scale")

# Once we have scaled any statics we can now run the IK solver
# on any motion files that we find
for root, dirs, files in os.walk(config.PATH):
    for file in files:
        # If we find a static file we can scale it if the config
        # file specifies this
        if config.RUN_IK and config.STATIC_NAME not in root and file.endswith(".trc"):
            # construct full file path for this file
            temp_path = os.path.join(root, file)
            
            # if the .trc file is called "markers.trc" we will assume is is a markers file,
            # otherwise, we will assume it was a markerless file.
            if file == "markers.trc":
                config.IS_MARKERLESS = False
            else:
                config.IS_MARKERLESS = True
            
            
            print(f"\n[INFO] - Running IK solver: {temp_path}\n")
            run_osim_tools(temp_path, config, job="ik")
            
            print(f"\n[INFO] - Done (?) IK solver: {temp_path}\n")
