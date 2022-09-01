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

def generate_ik_settings(path):

    # check if we are processing marker or 
    # markerless data - dtype==True means we 
    # are working with markerless data
    filename, dtype = _check_dtype(path)
    p_no = _update_current_part(path)
    
    # generate paths for xml file
    marker_file = path
    output_motion_file = os.path.join(path.replace(".trc", ".mot"))
    if dtype:
        model_file = os.path.join(_get_root(path), "biocv_fullbody_markerless_scaled.osim")
    else:
        model_file = os.path.join(_get_root(path), "biocv_fullbody_markers_scaled.osim")

    # load generic ik setting
    xml_path = _get_root(os.path.dirname(path))
    if dtype:
        xml_path = os.path.join(xml_path, "ik_markerless.xml")
        tree = ET.parse(xml_path)
    else:
        xml_path = os.path.join(xml_path, "ik_markers.xml")
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

def generate_scale_settings(path):
    
    # check if we are processing marker or 
    # markerless data - dtype==True means we 
    # are working with markerless data
    filename, dtype = _check_dtype(path)
    p_no = _update_current_part(path)

    # generate paths for xml file
    if dtype:
        trc_file = os.path.join(os.path.dirname(path.replace("/op-fused", "")), f"{p_no}_STATIC_01", f"{p_no}_static_op.trc")
        model_name = f"biocv_fullbody_op_{p_no}_scaled"
        model_file = os.path.join(_get_root(path), "biocv_fullbody_op.osim")
        output_model_file = os.path.join(os.path.dirname(path.replace("/op-fused", "")), f"biocv_fullbody_markerless_scaled.osim")
    else:
        trc_file = os.path.join(os.path.dirname(path.replace("/op-fused", "")), f"{p_no}_STATIC_01", "markers.trc")
        model_name = f"biocv_fullbody_markers_{p_no}_scaled"
        model_file = os.path.join(_get_root(path), "biocv_fullbody_markers.osim")
        output_model_file = os.path.join(os.path.dirname(path.replace("/op-fused", "")), "biocv_fullbody_markers_scaled.osim")

    # load generic scaling settings
    if dtype:
        xml_path = os.path.join(_get_root(path), "scale_op.xml")
    else:
        xml_path = os.path.join(_get_root(path), "scale_markers.xml") 
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

def run_osim_tools(path, job="ik"):
    if job == "ik":
        # generate xml ik settings file for this trial
        setup_file_path = generate_ik_settings(path)
    elif job == "scale":
        # generate xml sclaing settings file for this trial
        setup_file_path = generate_scale_settings(path)

    # run solver using settings file
    subprocess.run(['opensim-cmd',
                    'run-tool',
                    setup_file_path,
                    '-o off'])