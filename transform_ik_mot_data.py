"""
transform_ik_mot_data.py

Transform IK solver mot output data (parent-child Euler rotations) into global 
coordinate system as a orientation angles and 4x4 trans/rot matrix.

NOTE - Orientation angles describe the Euler rotations of a segements LCS 
        resolved in the global coordinate system.
     - 4x4 represents the rotation matrix and translation vector describing a segment
        in the global coordinate system.

"""

import os
import pandas as pd
import numpy as np
import opensim


def mot_loader(path: str) -> np.array:

    # load .mot
    data = pd.read_csv(path, sep="\t", header=8)
    data.drop(columns=["time"], inplace=True)
    data.reset_index(inplace=True)
    data = data.to_numpy()

    return data[:, 1:]


# set some paths
model_path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/2020-02-10-P06/biocv_fullbody_markerless_scaled.osim"
mot_path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/2020-02-10-P06/P06_RUN_01/markers.mot"

# Load model
osim_model = opensim.Model(model_path)

# init model
current_state = osim_model.initSystem()

# load mot
mot_data = mot_loader(mot_path)

# iterate over each time point
for row in mot_data:

    # generate state vector - OpenSim expects the parent-child Euler
    # rotations for each bodyset and then in this case an array of zeros
    # which I think would normally be velocities if we were using muscles
    # in the model
    pad = np.full_like(row, 0)
    state = np.hstack([row, pad])
    new_state = opensim.Vector(state.tolist())

    # set model's state for this time point
    osim_model.setStateVariableValues(current_state, new_state)
    osim_model.realizePosition(current_state)

    # for t in osim_model.getStateVariableValues:
    #     print(t)

    # iterate over each segment
    for body in osim_model.getBodyList():

        print(body.getName())

        # transform stuff and store somewhere useful
        trans = body.getTransformInGround(current_state)
        pos = trans.T
        rot = trans.R
        tran_4x4 = trans.toMat44()
        print(tran_4x4[0])
        xyz_in_ground = trans.convertRotationToBodyFixedXYZ()
