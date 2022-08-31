    """batch_ik.py

    Tool for batch processing trc files using OpenSim's IK solver
    """
import os
import time

from utils.osim_utils import run_osim_tools, generate_ik_settings, generate_scale_settings

def check_for_model(path, model):
    dir = os.path.dirname(path.replace("/op-fused", ""))
    return os.path.isfile(os.path.join(dir, model))

# Process file older than n days
limit_days = 4

treshold = time.time() - limit_days*86400

# set data paths
data_path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/2020-02-24-P19/P19_RUN_08"

# walk through data_path sub dirs and extract data
old = []
new = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith("markers.trc"):
            # construct full file path for this file
            temp_path = os.path.join(root, file)
            
            # skip unwanted trials such as statics and data from ap and dlc
            if "STATIC" not in temp_path and "ap-fused" not in temp_path and "dlc-fused" not in temp_path:
                # check file was not generated in the last n days
                creation_time = os.stat(temp_path.replace(".trc", ".mot")).st_ctime
                if creation_time > treshold:
                    old.append(root)
                    continue
                else:
                    new.append(root)

                if file.endswith("markers.trc"):
                    # check if we have a scaled marker-based model for this participant
                    if not check_for_model(root, "biocv_fullbody_markers_scaled.osim"):
                        # create a new scaled model for the 
                        # ik solver to use for this participant
                        print(f"\n[INFO] - Scaling markers: {temp_path}\n")
                        run_osim_tools(root, job="scale")

                elif file.endswith("joints_kalman.trc"):
                    # check if we have a scaled markerless model for this participant
                    if not check_for_model(root, "biocv_fullbody_markerless_scaled.osim"):
                        # create a new scaled model for the 
                        # ik solver to use for this participant
                        print(f"\n[INFO] - Scaling markerless: {temp_path}\n")
                        run_osim_tools(root, job="scale")




