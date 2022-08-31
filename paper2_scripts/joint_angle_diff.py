"""joint_angle_diffs.py

Generates Fig 6 & 7 for second BioCV paper. 
i.e. The Development and Evaluation of a Fully 
Automated Markerless Motion Capture Workflow 
"""

import os

from paper2_scripts.loader_utils import data_loader, update_data
import paper2_scripts.plot_utils as plot_utils
from paper2_scripts.data_utils import DataStruct

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

# plot CMJ angles
plot_utils.hip_joint_plot(jump_data, walk_data, run_data, save_path=data_path)
plot_utils.knee_ank_joint_plot(jump_data, walk_data, run_data, save_path=data_path)
# plot_utils.lumbar_joint_plot(jump_data, "CMJ")

# plot WALK angles
# plot_utils.hip_joint_plot(walk_data, "Walk")
# plot_utils.knee_ank_joint_plot(walk_data, "Walk")
# plot_utils.lumbar_joint_plot(walk_data, "Walk")

# plot RUN angles
# plot_utils.hip_joint_plot(run_data, "Run")
# plot_utils.knee_ank_joint_plot(run_data, "Run")
# plot_utils.lumbar_joint_plot(run_data, "Run")


# bland altmant/LFM
# angles = ["hip_flex",
#         "hip_ad_ab",
#         "hip_rot",
#         "knee_flex",
#         "ank_flex"]

# for angle in angles:
#     blandAltman(np.mean(jump_data["markers"][angle].to_numpy(), axis=0),
#                 np.mean(jump_data["markerless"][angle].to_numpy(), axis=0),
#                 title=f'{angle} - CMJ')

# for angle in angles:
#     blandAltman(np.mean(walk_data["markers"][angle].to_numpy(), axis=0),
#                 np.mean(walk_data["markerless"][angle].to_numpy(), axis=0),
#                 title=f'{angle} - WALK')

# for angle in angles:
#     blandAltman(np.mean(run_data["markers"][angle].to_numpy(), axis=0),
#                 np.mean(run_data["markerless"][angle].to_numpy(), axis=0),
#                 title=f'{angle} - RUN')


# MDC
