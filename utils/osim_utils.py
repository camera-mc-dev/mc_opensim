"""osim_utils.py

Tools for working with OpenSim in Python
"""

import os
import math
import numpy as np
import lxml.etree as ET
import subprocess
import opensim


def isRotationMatrix(R: np.array) -> float:
    """Checks input
     matrix is a valid rotation matrix.

    Args:
        R (np.array): 3x3 rotation matrix

    Returns:
        bool: Returns true if input is a valid rotation matrix
    """
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    # Had to *3 to reduce the tolerance. Some
    # precision lost when original data was
    # written to input file
    return n < (1e-6 * 3)


def rotationMatrixToEulerAngles(R: np.array, degrees=True) -> np.array:
    """Calculates rotation matrix to euler angles
    The result is the same as MATLAB except the order
    of the euler angles ( x and z are swapped ).

    Args:
        R (np.array): 3x3 rotation matrix
        degrees (bool, optional): Returns output in degrees is True, radians if False. Defaults to True.

    Returns:
        np.array: Euler angle
    """

    assert isRotationMatrix(R)

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    if degrees:
        x *= 180 / math.pi
        y *= 180 / math.pi
        z *= 180 / math.pi

    return np.array([x, y, z])

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
    
def rotate_data_table(table: opensim.TimeSeriesTableVec3, axis: list, deg: int) -> None:
    """Rotate OpenSim::TimeSeriesTableVec3 entries using an axis and angle.
    Parameters
    ----------
    table: OpenSim.common.TimeSeriesTableVec3
    axis: 3x1 vector
    deg: angle in degrees
    """
    R = opensim.Rotation(np.deg2rad(deg), opensim.Vec3(axis[0], axis[1], axis[2]))
    for i in range(table.getNumRows()):
        vec = table.getRowAtIndex(i)
        vec_rotated = R.multiply(vec)
        table.setRowAtIndex(i, vec_rotated)


def mm_to_m(table: opensim.TimeSeriesTableVec3, label: str) -> None:
    """Scale from units in mm for units in m.
    Parameters
    ----------
    label: string containing the name of the column you want to convert
    """
    c = table.updDependentColumn(label)
    for i in range(c.size()):
        c[i] = opensim.Vec3(c[i][0] * 0.001, c[i][1] * 0.001, c[i][2] * 0.001)