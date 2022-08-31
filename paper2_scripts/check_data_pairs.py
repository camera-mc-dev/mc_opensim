"""check_data_pairs

Tool to visualise pairs of markerless and marker-based data. 
Can be used to check quality of data in each trial.
"""
import os
import numpy as np
import pandas as pd

from ... import data_loader, update_data
# from mc_opensim.utils.loader_utils import data_loader, update_data
from paper2_scripts.plot_utils import plot_temp_data, plot_temp_lumbar_data
from paper2_scripts.data_utils import DataStruct


def check_data_pairs(data):

    reprocessing_list = []

    print(
        "\n\n[INFO] - Press any key for good trial and click mouse for bad trial...\n\n"
    )

    for col in data["markers"]["hip_flex"].columns:
        print(f"Checking: {col}")
        # check = plot_temp_data(data, col)
        check = plot_temp_data(data, col)
        if check is not None:
            reprocessing_list.append(check)

    return reprocessing_list


# set data paths
data_path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/2020-02-10-P06"

# create a data structure to work with each data source
jump_data = DataStruct().joint_ang_template
walk_data = DataStruct().joint_ang_template
run_data = DataStruct().joint_ang_template


# walk through data_path sub dirs and extract data
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith("markers.mot") or file.endswith("markerless.mot"):
            # check we haven't loaded a hop trial and if so skip it
            if "HOP" in root:
                continue

            # construct temp file path matching this file
            temp_path = os.path.join(root, file)
            print(f"[INFO] - Processing {temp_path}")

            # extract file name
            file_name = os.path.basename(temp_path).split(".")[0]

            # extract trial name
            trial_name = os.path.basename(root)

            # determine if this file is marker or markerless
            if "markers" in file:
                m_ml = "markers"
            elif "markerless" in file:
                m_ml = "markerless"

            # determine activity type
            if "RUN" in temp_path:
                act = "RUN"
            elif "CMJ" in temp_path:
                act = "JUMP"
            elif "WALK" in temp_path:
                act = "WALK"

            # load and time normalise the data
            try:
                temp = data_loader(temp_path, m_ml, act)

                # add the newly loaded data to the corresponding data struct
                if act == "JUMP":
                    jump_data = update_data(temp, jump_data, m_ml, trial_name)
                elif act == "WALK":
                    walk_data = update_data(temp, walk_data, m_ml, trial_name)
                elif act == "RUN":
                    run_data = update_data(temp, run_data, m_ml, trial_name)
            except Exception as e:
                print(f"[Warning] - Failed: {e}")


# Check jump data
jump_reprocess = check_data_pairs(jump_data)
print("Jump Data:")
for f in sorted(jump_reprocess):
    print(f"dump - {f}")

# Check walk data
walk_reprocess = check_data_pairs(walk_data)
print("Walk Data:")
for f in sorted(walk_reprocess):
    print(f"dump - {f}")

# Check run data
run_reprocess = check_data_pairs(run_data)
print("Run Data:")
for f in sorted(run_reprocess):
    print(f"dump - {f}")

# final_list = sorted(jump_reprocess + walk_reprocess + run_reprocess)
# final_list = sorted(walk_data             )
# for f in final_list:
#     print(f)
