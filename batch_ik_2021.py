import os
import lxml.etree as ET
import subprocess


def generate_ik_settings(path, save_path):

    # determine if we are using markers or markerless
    filename = os.path.basename(path)
    if "markerless" in filename:
        dtype = True
    else:
        dtype = False

    # generate paths for xml file
    marker_file = path
    save_path = "/home/ln424/Documents/CAMERA/BioCV_Project/ISBS2021_results"
    output_motion_file = os.path.join(save_path, filename.replace(".trc", ".mot"))
    if dtype:
        model_file = path.replace(filename[4:], "markerless_scaled.osim")
    else:
        model_file = path.replace(filename[4:], "markers_scaled.osim")

    # load generic ik setting
    xml_path = os.path.dirname(os.path.dirname(path))
    if dtype:
        xml_path = os.path.join(xml_path, "ik_markerless.xml")
        tree = ET.parse(xml_path)
    else:
        xml_path = os.path.join(xml_path, "ik_markers.xml")
        tree = ET.parse(xml_path)

    # update for the current trial
    xml_root = tree.getroot()
    for elem in xml_root.iter("marker_file"):
        elem.text = marker_file
    for elem in xml_root.iter("output_motion_file"):
        elem.text = output_motion_file
    for elem in xml_root.iter("model_file"):
        elem.text = model_file

    # write updated xml to disk
    xml_savepath = path.replace(".trc", "_ik_settings.xml")
    tree.write(xml_savepath)

    return xml_savepath


def generate_scale_settings(path, save_path):
    pass


def solve_ik(path, job="ik"):
    if job == "ik":
        # generate xml ik settings file for this trial
        setup_file_path = generate_ik_settings(path)
    elif job == "scale":
        # generate xml sclaing settings file for this trial
        setup_file_path = generate_scale_settings(path)

    # run solver using settings file
    subprocess.run(["opensim-cmd", "run-tool", setup_file_path])


# set data paths
data_path = "/media/ln424/OS/Users/lauri/Documents/ISBS2021_BioCV_OpenSim/P09"

# walk through data_path sub dirs and extract data
processing_list = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".trc"):
            # construct temp file path this matching file
            temp_path = os.path.join(root, file)
            # generate settings file and run solver
            if "markerless" in temp_path and "P09" in temp_path:
                print(f"[INFO] - Processing {temp_path}")
                solve_ik(temp_path)
                processing_list.append(temp_path)
