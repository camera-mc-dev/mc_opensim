import os
import numpy as np
import pandas as pd

from paper2_scripts.loader_utils import data_loader, update_data
from paper2_scripts.plot_utils import orientation_plot
from paper2_scripts.data_utils import DataStruct

# set data paths
data_path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/2020-03-05-P17/"

# create a data structure to work with each data source
jump_data = DataStruct().segment_ang_template
walk_data = DataStruct().segment_ang_template
run_data = DataStruct().segment_ang_template

# walk through data_path sub dirs and extract data
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith("openSimRots_markerless.csv") or file.endswith(
            "openSimRots_markers.csv"
        ):
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

# plot torso
orientation_plot(jump_data, "torso", "CMJ", "Torso")
orientation_plot(walk_data, "torso", "WALK", "Torso")
orientation_plot(run_data, "torso", "RUN", "Torso")

# plot pelvis
orientation_plot(jump_data, "pelvis", "CMJ", "pelvis")
orientation_plot(walk_data, "pelvis", "WALK", "pelvis")
orientation_plot(run_data, "pelvis", "RUN", "pelvis")

# plot femur
orientation_plot(jump_data, "femur", "CMJ", "femur")
orientation_plot(walk_data, "femur", "WALK", "femur")
orientation_plot(run_data, "femur", "RUN", "femur")

# plot tibia
orientation_plot(jump_data, "tibia", "CMJ", "tibia")
orientation_plot(walk_data, "tibia", "WALK", "tibia")
orientation_plot(run_data, "tibia", "RUN", "tibia")

# plot calcn
orientation_plot(jump_data, "calcn", "CMJ", "calcn")
orientation_plot(walk_data, "calcn", "WALK", "calcn")
orientation_plot(run_data, "calcn", "RUN", "calcn")
