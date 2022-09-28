import os
import lxml.etree as ET
import subprocess

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

def _check_for_model(path, model):
    dir = os.path.dirname(path.replace("/op-fused", ""))
    return os.path.isfile(os.path.join(dir, model))

def _find_scaled_model(base_dir: str, ext: str, substr: str) -> str:
    print( base_dir )
    print( ext )
    print( substr )
    for root, dirs, files in os.walk(base_dir):
            for file in files:
                if substr in root and file.endswith(ext):
                    return os.path.join(root, file)
    
    raise FileNotFoundError(f"[Error] - Could not locate: {ext} under {base_dir}")

def generate_ik_settings(path: str, config: object) -> str:

    # generate paths for xml file
    marker_file = path
    output_motion_file = os.path.join(path.replace(".trc", ".mot"))
    
    # We need to find the scaled osim model that is associtated with this
    # motion trial. However, there could be several if a number of static
    # trials have been collected.
    if config.IS_MARKERLESS:
        # To find a markerless model we'll assume that the static and scaled osim
        # files are stored in the same parent dir as this trial.
        # we assume that markerless files are in a subdir of the trial dir.
        subDir    = os.path.dirname(path)
        trialDir  = os.path.dirname(subDir)
        sessDir   = os.path.dirname(trialDir)
        model_file = _find_scaled_model(sessDir, "biocv_fullbody_markerless_scaled.osim", config.STATIC_NAME)
        
    else:
        # if we are dealing with marker based data i.e. from QTM
        # we'll assume (for now) that there is a static model in the
        # dir as the one that out current file resides in.
        model_file = _find_scaled_model(os.path.dirname(os.path.dirname(path)), "biocv_fullbody_markers_scaled.osim", config.STATIC_NAME)
        
    # load generic ik setting
    if config.IS_MARKERLESS:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "ik_markerless.xml")
        xml_savepath = marker_file.replace(".trc", "_ik_markerless.xml")
    else:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "ik_markers.xml")
        xml_savepath = marker_file.replace(".trc", "_ik_markers.xml")
        
    tree = ET.parse(xml_path)
    
    # update xml settings for the current trial
    xml_root = tree.getroot()
    for elem in xml_root.iter('marker_file'):
        elem.text = marker_file
    for elem in xml_root.iter('output_motion_file'):
        elem.text = output_motion_file
    for elem in xml_root.iter('model_file'):
        elem.text = model_file
    for elem in xml_root.iter('time_range'):
        elem.text = str(config.IK_TIME_RANGE[0]) + " " + str(config.IK_TIME_RANGE[1])
    # write updated xml to disk
    tree.write(xml_savepath)
    
    return xml_savepath

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
        xml_savepath = trc_file.replace(".trc", "_scale_op.xml")
    else:
        xml_path = os.path.join(config.DEFAULT_MODELS_PATH, "scale_markers.xml")
        xml_savepath = trc_file.replace(".trc", "_scale_markers.xml")

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
    for elem in xml_root.iter('time_range'):
        elem.text = str(config.SCALE_TIME_RANGE[0]) + " " + str(config.SCALE_TIME_RANGE[1])

    # write updated xml to disk
    tree.write(xml_savepath)
    
    return xml_savepath

def run_osim_tools(path: str, config: object, job="ik") -> None:
    if job == "ik":
        # generate xml ik settings file for this trial
        setup_file_path = generate_ik_settings(path, config)
    elif job == "scale":
        # generate xml scaling settings file for this trial
        setup_file_path = generate_scale_settings(path, config)

    # run solver using settings file
    oscmd = 'opensim-cmd'
    if config.OPENSIM_BINARY_PATH != None:
        print( config.OPENSIM_BINARY_PATH )
        oscmd = config.OPENSIM_BINARY_PATH + oscmd
    
    x = subprocess.run([oscmd,
                    'run-tool',
                    setup_file_path,
                    '-o debug'])
    print(x)
