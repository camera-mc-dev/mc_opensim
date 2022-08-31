from distutils.util import strtobool
import os
import subprocess


def copy_rename(src: str, dst: str) -> None:

    # build dst path from src path
    file_parts = src.split("/")

    dst_path = os.path.join(
        dst,
        "*" + file_parts[-2],
        file_parts[-1].replace("_markers.c3d", ""),
        "markers.c3d",
    )
    print(f"[INFO] - Copied {src}\n to\n {dst_path}")

    # copy and move to dst
    # shutil.copy(src, dst_path)
    cmd = ["cp", src, dst]
    subprocess.run(cmd)


def main(src: str, dst: str) -> None:
    # walk through data_path sub dirs
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith("_markers.c3d"):
                temp = os.path.join(root, file)
                copy_rename(temp, dst)


if __name__ == "__main__":
    src = "/media/ln424/Laurie Needham HD/BioCV/Data/Round2/"
    dst = "/home/ln424/Documents/CAMERA/BioCV_Project/markerless_data/"

    main(src, dst)
