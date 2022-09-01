import os
import numpy as np
import opensim

def _rotate_data_table(table: opensim.TimeSeriesTableVec3, axis: list, deg: int) -> None:
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


def _mm_to_m(table: opensim.TimeSeriesTableVec3, label: str) -> None:
    """Scale from units in mm for units in m.
    Parameters
    ----------
    label: string containing the name of the column you want to convert
    """
    c = table.updDependentColumn(label)
    for i in range(c.size()):
        c[i] = opensim.Vec3(c[i][0] * 0.001, c[i][1] * 0.001, c[i][2] * 0.001)


def generate_trc(c3d_path: str, rotate=None) -> None:
    """Given a path to a c3d file, will read c3d data and 
    convert to OpenSim's trc format. Rotation can be applied
    if required by passing list of ints containing rotation around
    each axis in degrees.

    Args:
        c3d_path (str): path to c3d file
        rotate (list, optional): Axis rotations to be applied in an 
        x, y, z sequence e.g. [90, 90, 90] will apply a 90 deg rotation
        to all axes. Defaults to None.
    """
    # Marker data read from C3D.
    adapter = opensim.C3DFileAdapter()
    tables = adapter.read(c3d_path)

    # Get marker data from c3d file
    markers = adapter.getMarkersTable(tables)

    # Rotate marker data assuming that positive z-axis is
    # normal to the floor plane
    if rotate is not None:
        _rotate_data_table(markers, [1, 0, 0], rotate[0])
        _rotate_data_table(markers, [0, 1, 0], rotate[1])
        _rotate_data_table(markers, [0, 0, 1], rotate[2])

    # Write marker data to .trc file
    trcAdapter = opensim.TRCFileAdapter()
    savename = c3d_path.replace(".c3d", ".trc")
    trcAdapter.write(markers, savename)

def validate_trc(trc_path: str) -> None:
    trcAdapter = opensim.TRCFileAdapter()
    trcAdapter.read(trc_path)
    print(f"[INFO] - Validated: {trc_path}")

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