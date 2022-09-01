"""4x4ToEuler.py

Convert Opensim 44mat to Euler rotations in ground 
and extract segment local coordinate system.
"""

import os
import numpy as np
import pandas as pd

from utils.maths_utils import rotationMatrixToEulerAngles


def process_data(path, markerless=True):

    data_row = []
    vid_frame = []
    rots = {}
    trans = {}
    # open file and read/process one line at a time
    with open(path) as file:
        for line in file:
            if line[0].isdigit():
                # if we are processing the first frame, we populate an empty dict
                # with keys using seg and store the data
                if line[0] == "0":
                    rots["vid_frame"] = [int(line.split()[1])]
                    trans["vid_frame"] = [int(line.split()[1])]
                # if we already have a dict of keys, we can simply append
                else:
                    rots["vid_frame"].append(int(line.split()[1]))
                    trans["vid_frame"].append(int(line.split()[1]))

            elif line.startswith("\t") and not line.strip().split()[0].endswith(
                "_offset"
            ):
                # get segment name and reshape to a 4x4
                temp_line = line.strip().split()
                seg = temp_line.pop(0)
                mat = np.array(temp_line, dtype=np.float).reshape((4, 4))

                # convert 3x3rot to xyz euler angle
                rot = rotationMatrixToEulerAngles(mat[:3, :3])

                # if we are processing the frist frame, we populate an empty dict
                # with keys using seg and store the data
                if len(rots["vid_frame"]) == 1:
                    for i, xyz in enumerate(["_x", "_y", "_z"]):
                        rots[seg + xyz] = [rot[i]]
                        trans[seg + xyz] = [mat[i, -1]]
                # if we already have a dict of keys, we can simply append
                else:
                    for i, xyz in enumerate(["_x", "_y", "_z"]):
                        rots[seg + xyz].append(rot[i])
                        trans[seg + xyz].append(mat[i, -1])

    # Write converted rot and trans dicts to disk in an easy to use tabular format
    trans = pd.DataFrame(trans)
    rots = pd.DataFrame(rots)

    if markerless:
        m_ml = "_markerless"
    else:
        m_ml = "_markers"

    save_path = os.path.dirname(path)
    trans_name = os.path.join(save_path, "openSimTrans" + m_ml + ".csv")
    rots_name = os.path.join(save_path, "openSimRots" + m_ml + ".csv")

    print(f"Saving: {trans_name}")
    print(f"Saving: {rots_name}")
    trans.to_csv(trans_name)
    rots.to_csv(rots_name)


def main(path: str) -> None:

    # walk through data_path sub dirs and extract data
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith("openSimTransformations"):
                data_path = os.path.join(root, file)
                print(f"Processing: {data_path}")

                if file.endswith("-markerBased"):
                    process_data(data_path, markerless=False)
                elif file.endswith("-markerless"):
                    process_data(data_path, markerless=True)


if __name__ == "__main__":
    # set dir path to search for 'openSimTransforms'
    path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/"
    main(path)
