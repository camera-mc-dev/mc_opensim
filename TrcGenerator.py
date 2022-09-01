"""TrcGenerator.py

Tool to convert .c3d files to OpenSim .trc. Each c3d 
file will be have coordinate systems rotated from z-up 
to y-up and units converted from mm to m.

Usage: Set path to directory containing c3d files. 
"""

import os
import pandas as pd
import numpy as np
import opensim

from utils.maths_utils import rotate_data_table, mm_to_m

def validate_trc(path: str) -> None:
    trcAdapter.read(savename)

def fix_trc(filename: str, find="nan", replace=0, fix_units=True, unit="mm") -> None:
    """Attempt to fix unreadable trc file. This is often caused
       by incorrect unit scaling or having '0' instead of nans

    Args:
        filename (str): _description_
        find (str, optional): _description_. Defaults to "nan".
        replace (int, optional): _description_. Defaults to 0.
        fix_units (bool, optional): _description_. Defaults to True.
        unit (str, optional): _description_. Defaults to "mm".
    """
    # open file and read lines
    infi = open(filename)
    lines = infi.readlines()

    # find and replace
    for i, line in enumerate(lines):
        lines[i] = line.replace("nan", "0")

    # make sure that units are given in meta-data
    if fix_units:
        lines[2] = lines[2].replace("\t\t", f"\t{unit}\t")

    # write back to file
    with open(filename, "w") as f:
        for line in lines:
            f.write(f"{line}")


# set path to data and genate processing list of c3d files
path = "/media/ln424/Laurie Needham HD/New_TRCs"

processing_list = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".c3d"):
            temp = os.path.join(root, file)
            processing_list.append(temp)
# processing_list = sorted([os.path.join(path, f) for f in os.listdir(path) if f.endswith(".c3d")])

for p in processing_list:
    print(f"[INFO] - Converting: {p}")

    # Marker data read from C3D.
    adapter = opensim.C3DFileAdapter()
    tables = adapter.read(p)

    # Get marker data from c3d file
    markers = adapter.getMarkersTable(tables)

    # Rotate marker data assuming that positive z-axis is
    # normal to the floor plane
    rotate_data_table(markers, [0, 0, 1], -90)
    rotate_data_table(markers, [1, 0, 0], -90)

    # Write marker data to .trc file
    trcAdapter = opensim.TRCFileAdapter()
    savename = os.path.join(path, p.replace(".c3d", ".trc"))
    trcAdapter.write(markers, savename)

    # check that resulting trc file is readable
    try:
        validate_trc(savename)
    except Exception as e:
        print(f"[WARNING] - {savename} not readable - attempting to replace nans")
        # read file in as csv and replace nans
        fix_trc(savename)
        # check that we have fixed the nan/0 issue
        try:
            markersDouble = trcAdapter.read(savename)
            print(f"[INFO] - Warning resolved")
        except Exception as e:
            print(f"[WARNING] - {savename} still not readable")
            print(f"[WARNING] - {e}")
print("[INFO] - Complete!")
