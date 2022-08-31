"""loader_utils.py

Fucntions for loading v3d and openSim data

"""

import os
import numpy as np
import pandas as pd


def _load_v3d_events(path: str) -> pd.DataFrame:

    # set event data path
    events_path = os.path.dirname(path)
    events_path = os.path.join(events_path, "EVENTS.txt")
    # load csv file into dataframe
    events = pd.read_csv(events_path, sep="\t", header=1)
    # drop unwanted row info from v3d
    events.drop([0, 1, 2], inplace=True)
    # reset the index
    events.reset_index(inplace=True)
    # convert values to numpy (float64) for ease of use
    # later on with np.nan
    events = events.astype(float)
    return events


def _extract_events(path: str, act: str, fs=200) -> tuple:

    # load events data from file
    events = _load_v3d_events(path)

    # if we are working with jumping (CMJ) data we can
    # simply specifty start and end using first_movement to
    # stable
    if act == "JUMP":
        start = int(events["First_Movement"][0] / (1 / fs))
        end = int(events["Stable"].to_numpy()[0] / (1 / fs))
        L_R = "r"

    # else if we are working with a running trial we will use
    # the last non-FP contact as start or for walking the first
    # FP contact
    else:
        L_ON = events["LON"].to_numpy()[0]
        R_ON = events["RON"].to_numpy()[0]

        # work out which foot hit the force plates first
        if ~np.isnan(L_ON) and ~np.isnan(R_ON):
            if L_ON < R_ON:
                L_R = "l"
            else:
                L_R = "r"
        elif np.isnan(L_ON):
            L_R = "r"
        else:
            L_R = "l"

        if act == "RUN":
            # once we know which foot hit the plate first we can extract
            # the TD frame from the previous contact to the next contact on
            # same foot

            if L_R == "r":
                start = int(events["LTO"][events["LTO"] < R_ON].max() / (1 / fs))
                end = int(events["LTO"][events["LTO"] > R_ON].min() / (1 / fs))
            else:
                start = int(events["RTO"][events["RTO"] < L_ON].max() / (1 / fs))
                end = int(events["RTO"][events["RTO"] > L_ON].min() / (1 / fs))

        elif act == "WALK":
            if L_R == "r":
                start = int(events["RON"].to_numpy()[0] / (1 / fs))
                end = int(events["RHS"][events["RHS"] > R_ON].min() / (1 / fs))
            else:
                start = int(events["LON"].to_numpy()[0] / (1 / fs))
                end = int(events["LHS"][events["LHS"] > R_ON].min() / (1 / fs))

    return start, end, L_R


def _interp(y: np.array, Q=101) -> np.array:
    """linear interpolation to *Q* values

    Args:
        y (np.array): input array to be interpolated
        Q (int, optional): Desired output array length. Defaults to 101.

    Returns:
        np.array: Interpolated array of length Q
    """
    x0 = range(y.size)
    x1 = np.linspace(0, y.size, Q)
    return np.interp(x1, x0, y, left=None, right=None)


def _time_norm(data: pd.DataFrame, start: int, end: int, Q=101) -> pd.DataFrame:
    """Wrapper for time normalising dataframe columns to *Q* points between two frame (start and end)

    Args:
        data (pd.DataFrame): DataFrame where each column represents a signal and rows
        start (int): start frame
        end (int): end frame
        Q (int, optional): Desired output array length.. Defaults to 101.

    Returns:
        pd.DataFrame: DataFrame with same columns and data interpolated to *Q* points
    """
    data_out = pd.DataFrame(0, index=np.arange(Q), columns=data.columns)
    for col in data.columns:
        if pd.isnull(data[col]).all():
            data_out[col] = np.zeros(Q)
        else:
            data_in = data[col].to_numpy()[start:end]
            data_out[col] = _interp(data_in)
    return data_out


def _from_mot(
    path: str, start_frame: int, end_frame: int, L_R: str, interp=True
) -> pd.DataFrame:
    """Load .mot and extract vars of interest

    Args:
        path (str): path to file
        start_frame (int): start frame
        end_frame (int): end frame
        L_R (str): left or right side
        interp (bool, optional): Time normalise data to 101 points?. Defaults to True.

    Returns:
        pd.DataFrame: Contents of .mot file loaded into a pd.DataFrame
    """
    # load file from disk
    data = pd.read_csv(path, sep="\t", header=8)
    # drop unwanted headers
    data.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], inplace=True)
    # retain only columns that we want
    data.reset_index(inplace=True)
    data = data[
        [
            f"hip_flexion_{L_R}",
            f"hip_adduction_{L_R}",
            f"hip_rotation_{L_R}",
            f"knee_angle_{L_R}",
            f"ankle_angle_{L_R}",
            f"subtalar_angle_{L_R}",
            "lumbar_extension",
            "lumbar_bending",
            "lumbar_rotation",
        ]
    ]

    # normalise each column to 101 points using the start
    # and end frame idicies
    if interp:
        data = _time_norm(data, start_frame, end_frame)

    return data


def _from_csv(
    path: str, start_frame: int, end_frame: int, L_R: str, interp=True
) -> pd.DataFrame:
    """Load .csv and extract vars of interest

    Args:
        path (str): path to file
        start_frame (int): start frame
        end_frame (int): end frame
        L_R (str): left or right side
        interp (bool, optional): Time normalise data to 101 points?. Defaults to True.

    Returns:
        pd.DataFrame: Contents of .csv file loaded into a pd.DataFrame
    """

    data = pd.read_csv(path)
    data.reset_index(inplace=True)
    data = data[
        [
            "torso_x",
            "torso_y",
            "torso_z",
            "pelvis_x",
            "pelvis_y",
            "pelvis_z",
            f"femur_{L_R}_x",
            f"femur_{L_R}_y",
            f"femur_{L_R}_z",
            f"tibia_{L_R}_x",
            f"tibia_{L_R}_y",
            f"tibia_{L_R}_z",
            f"calcn_{L_R}_x",
            f"calcn_{L_R}_y",
            f"calcn_{L_R}_z",
            f"humerus_{L_R}_x",
            f"humerus_{L_R}_y",
            f"humerus_{L_R}_z",
            f"ulna_{L_R}_x",
            f"ulna_{L_R}_y",
            f"ulna_{L_R}_z",
        ]
    ]

    # normalise each column to 101 points using the start
    # and end frame idicies
    if interp:
        data = _time_norm(data, start_frame, end_frame)

    return data


def data_loader(path: str, m_ml: str, act: str) -> pd.DataFrame:

    # load and extract start and end event based on activity type.
    # for jumping this will be start and end, for walking
    # and running, this be the last TD before the FP to the
    # next TD in that stride cycle.
    start_frame, end_frame, L_R = _extract_events(path, act)

    # a quick fix for some gappy marker-based trials
    if "P27_RUN" in path:
        end_frame -= 10
    # load data, extract columns of interest and
    # normalise to 101 data points
    if path.endswith(".mot"):
        data = _from_mot(path, start_frame, end_frame, L_R, m_ml)
    elif path.endswith(".csv"):
        data = _from_csv(path, start_frame, end_frame, L_R, m_ml)

    return data


def update_data(temp, data, m_ml, trial_name):
    # update each item in the main data dict
    for key, col in zip(data[m_ml].keys(), temp.columns):
        data[m_ml][key][trial_name] = temp[col]
    return data
