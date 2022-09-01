import os
import lxml.etree as ET
import subprocess
import glob

def _get_root(path):
    return os.path.dirname(os.path.dirname(path.replace("/op-fused", "")))

def _check_dtype(path):
    filename = os.path.basename(path)
    if "op-fused" in path:
        dtype = True
    else:
        dtype = False
    return filename, dtype

def _update_current_part(path):
    idx = path.rfind("P")
    return path[idx:idx+3]

def generate_ik_settings(path: str, config: object) -> str:

    # generate paths for xml file
    marker_file = path
    output_motion_file = os.path.join(path.replace(".trc", ".mot"))
    
    # We need to find the scaled osim model that is associtated with this
    # motion trial. However, there could be several if a number of static
    # trials have been collected.
    if config.IS_MARKERLESS:
        model_file = os.path.join(config.DEFAULT_MODELS_PATH, "biocv_fullbody_markerless_scaled.osim")
    else:
        # if we are dealing with marker based data i.e. from QTM
        # we'll assume (for now) that there is a static model in the
        # dir as the one that out current file resides in.
        model_file = [os.path.join(path, f) for f in os.listdir(os.path.dirname(path)) if config.STATIC_NAME in f and f.endswith("biocv_fullbody_markerless_scaled.osim")][0]
        if not model_file:
            raise FileNotFoundError()
    # load generic ik setting
    if config.IS_MARKERLESS:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "ik_markerless.xml")
    else:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "ik_markers.xml")
    tree = ET.parse(xml_path)
    
    # update xml settings for the current trial
    xml_root = tree.getroot()
    for elem in xml_root.iter('marker_file'):
        elem.text = marker_file
    for elem in xml_root.iter('output_motion_file'):
        elem.text = output_motion_file
    for elem in xml_root.iter('model_file'):
        elem.text = model_file
    
    # write updated xml to disk
    tree.write(xml_path)
    
    return xml_path

def generate_scale_settings(path: str, config: object) -> str:

    # generate paths for xml file
    trc_file = path
    if config.IS_MARKERLESS:
        model_name = f"biocv_fullbody_op_scaled"
        model_file = os.path.join(config.DEFAULT_MODELS_PATH, "biocv_fullbody_op.osim")
        output_model_file = path.replace(".trc", "_biocv_fullbody_markerless_scaled.osim")
    else:
        model_name = f"biocv_fullbody_markers_scaled"
        model_file = os.path.join(config.DEFAULT_MODELS_PATH, "biocv_fullbody_markers.osim")
        output_model_file = path.replace(".trc", "_biocv_fullbody_markers_scaled.osim")

    # load generic scaling settings
    if config.IS_MARKERLESS:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "scale_op.xml")
    else:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "scale_markers.xml")
    tree = ET.parse(xml_path)

    # update xml settings for the current trial
    xml_root = tree.getroot()
    for elem in xml_root.iter('marker_file'):
        elem.text = trc_file
    for elem in xml_root.iter('output_model_file'):
        elem.text = output_model_file
    for elem in xml_root.iter('model_file'):
        elem.text = model_file
    for elem in tree.xpath("//ScaleTool"):
        elem.attrib['name'] = model_name

    # write updated xml to disk
    tree.write(xml_path)
    
    return xml_path

def run_osim_tools(path: str, config: object, job="ik") -> None:
    if job == "ik":
        # generate xml ik settings file for this trial
        setup_file_path = generate_ik_settings(path, config)
    elif job == "scale":
        # generate xml scaling settings file for this trial
        setup_file_path = generate_scale_settings(path, config)

    # run solver using settings file
    subprocess.run(['opensim-cmd',
                    'run-tool',
                    setup_file_path,
                    '-o off'])