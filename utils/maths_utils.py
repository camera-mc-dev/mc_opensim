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