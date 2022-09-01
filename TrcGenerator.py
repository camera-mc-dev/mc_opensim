"""TrcGenerator.py

Tool to convert .c3d files to OpenSim .trc. Coordinate system
axes will be rotated if specifed in config.py.

Usage: Specify settings in config file and run:
        python3 TrcGenerator.py
"""

import os
import config
from utils.trc_utils import generate_trc, validate_trc, fix_trc

for root, dirs, files in os.walk(config.PATH):
    for file in files:
        # If we need to generate trc files then we need to search
        # for c3ds
        if file.endswith(".c3d"):
            # construct full file path for this file
            temp_path = os.path.join(root, file)
            print(f"[INFO] - Processing: {temp_path}")

            # generate trc file using config settings
            generate_trc(
                temp_path, rotate=[config.ROTATE_X, config.ROTATE_Y, config.ROTATE_Z]
            )

            if config.VALIDATE_TRC:
                # check that resulting trc file is readable
                try:
                    trc_savepath = temp_path.replace(".c3d", ".trc")
                    validate_trc(trc_savepath)
                except Exception as e:
                    print(
                        f"[WARNING] - {trc_savepath} not readable - attempting to replace nans"
                    )
                    # read file in as csv and replace nans
                    fix_trc(trc_savepath)
                    # check that we have fixed the nan/0 issue
                    try:
                        validate_trc(trc_savepath)
                        print(f"[INFO] - Warning resolved")
                    except Exception as e:
                        print(f"[ERROR] - {trc_savepath} still not readable")
                        print(f"[ERROR] - {e}")

print("[INFO] - Complete!")
