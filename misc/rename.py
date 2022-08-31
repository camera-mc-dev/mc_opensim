import os
import shutil
from pathlib import Path


def mv_rename(path: str) -> None:

    # get one dir up from path (i.e. parent dir)
    # parent_dir = Path(path).parents[1]
    # # create new file name
    # new = os.path.join(parent_dir, "markerless.mot")

    new = path.replace("_EVENTS.txt", "/markers.events")

    # move and rename file
    print(f"Move and rename: {path} as: \n\t {new}")
    shutil.copy(path, new)


def main(path: str) -> None:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("_EVENTS.txt"):
                temp = os.path.join(root, file)

                mv_rename(temp)


if __name__ == "__main__":
    path = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data"
    main(path)
