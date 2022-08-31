"""isbs2021.py

Generates results and figures for ISBS 2021 abstract.

"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

font = {"size": 16}
plt.rc("font", **font)


def from_v3d_events(path):

    # set event data path
    events_path = (
        path.replace("markers", "EVENTS")
        .replace("markerless", "EVENTS")
        .replace(".mot", ".txt")
        .replace("_fix_pv", "")
    )
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


def extract_events(events, cycle="step"):

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

    # once we know which foot hit the plate first we can extract
    # the TD frame from the previous contract and the next contact
    if cycle == "stride":
        if L_R == "r":
            start = int(events["LTO"][events["LTO"] < R_ON].max() / (1 / 200))
            end = int(events["LTO"][events["LTO"] > R_ON].min() / (1 / 200))
        else:
            start = int(events["RTO"][events["RTO"] < L_ON].max() / (1 / 200))
            end = int(events["RTO"][events["RTO"] > L_ON].min() / (1 / 200))

    elif cycle == "step":
        if L_R == "r":
            start = int(R_ON / (1 / 200))
            end = int(events["LHS"][events["LHS"] > R_ON].min() / (1 / 200))
        else:
            start = int(L_ON / (1 / 200))
            end = int(events["RHS"][events["RHS"] > L_ON].min() / (1 / 200))

    return start, end, L_R


def interp(y, Q=101):
    x0 = range(y.size)
    x1 = np.linspace(0, y.size, Q)
    return np.interp(x1, x0, y, left=None, right=None)


def time_norm(data, start, end, Q=101):
    """
    linear interpolation to *n* values
    """
    data_out = pd.DataFrame(0, index=np.arange(Q), columns=data.columns)
    for col in data.columns:
        if pd.isnull(data[col]).all():
            data_out[col] = np.zeros(Q)
        else:
            data_in = data[col].to_numpy()[start:end]
            data_out[col] = interp(data_in)
    return data_out


def from_mot(path, start_frame, end_frame, L_R, m_ml):

    # load .mot and extract vars of interest
    data = pd.read_csv(path, sep="\t", header=8)
    data.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], inplace=True)
    data.reset_index(inplace=True)
    data = data[
        [
            f"hip_flexion_{L_R}",
            f"hip_adduction_{L_R}",
            f"hip_rotation_{L_R}",
            f"knee_angle_{L_R}",
            f"ankle_angle_{L_R}",
            f"subtalar_angle_{L_R}",
        ]
    ]

    # normalise each column to 101 points using the start
    # and end frame idicies
    data = time_norm(data, start_frame, end_frame)

    return data


def data_loader(path, m_ml="markers"):

    # load event data
    events = from_v3d_events(path)

    # find TD closest to lab origin and
    # use the previous TD so we can normalise
    # data from TD to TD in the centre of the volume
    start_frame, end_frame, L_R = extract_events(events, cycle="stride")
    if "P27" in path:
        end_frame -= 10
    # load data, extract columns of interest and
    # normalise to 101 data points
    data = from_mot(path, start_frame, end_frame, L_R, m_ml)

    return data


def update_data(temp, data, file_name):
    # remove "markers_" or "markerless_" from file_name
    file_name = file_name.replace("markers_", "").replace("markerless_", "")
    # update each item in the main data dict
    for key, col in zip(data.keys(), temp.columns):
        data[key][file_name] = temp[col]
    return data


# set data paths
data_path = "/home/ln424/Documents/CAMERA/BioCV_Project/ISBS2021_results"

# create a data structure to work with for each data source
markers = {
    "hip_flex": pd.DataFrame(),
    "hip_ad_ab": pd.DataFrame(),
    "hip_rot": pd.DataFrame(),
    "knee_flex": pd.DataFrame(),
    "ank_flex": pd.DataFrame(),
    "ank_ev_inv": pd.DataFrame(),
}

markerless = {
    "hip_flex": pd.DataFrame(),
    "hip_ad_ab": pd.DataFrame(),
    "hip_rot": pd.DataFrame(),
    "knee_flex": pd.DataFrame(),
    "ank_flex": pd.DataFrame(),
    "ank_ev_inv": pd.DataFrame(),
}

# walk through data_path sub dirs and extract data
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".mot"):
            # construct temp file path this matching file
            temp_path = os.path.join(root, file)
            print(f"[INFO] - Processing {temp_path}")
            # extract file name
            file_name = os.path.basename(temp_path).split(".")[0]

            # load and time normalise the data
            if "markers" in file:
                m_ml = "markers"
            elif "markerless" in file:
                m_ml = "markerless"
            temp = data_loader(temp_path, m_ml=m_ml)

            # parse data based on name
            if m_ml == "markers":
                # add the newly loaded data to the dict of dfs
                markers = update_data(temp, markers, file_name)
            else:
                # add the newly loaded data to the dict of dfs
                markerless = update_data(temp, markerless, file_name)

# sort columns in markerless data to match the order of those
# in the marker-based data
for key in markerless.keys():
    markerless[key] = markerless[key].reindex(columns=markers[key].columns)

# plot each waveform and its diff for inspection purposes
joint_axis1 = "hip_flex"
joint_axis2 = "hip_ad_ab"
joint_axis3 = "hip_rot"
# joint_axis1 = "knee_flex"
# joint_axis2 = "ank_flex"
# joint_axis3 = "ank_ev_inv"
# for m, ml in zip(markers[joint_axis1].columns, markerless[joint_axis1].columns):
#     fig1 = plt.figure()

#     ax01 = fig1.add_subplot(3,2,1)
#     ax01.plot(markers[joint_axis1][m], color='r')
#     ax01.plot(markerless[joint_axis1][ml], color='b')
#     ax01.set_title(f"{m} vs {ml}")
#     ax01.set_ylabel("Joint Angle [$^\circ$]")
#     ax01.set_xlim(0, 100)
#     # ax01.set_ylim(-40, 60)

#     ax02 = fig1.add_subplot(3,2,2)
#     ax02.plot(markers[joint_axis1][m].to_numpy() - markerless[joint_axis1][ml].to_numpy(), color='r', linewidth=3)
#     rmse = np.round(np.sqrt((np.mean(markers[joint_axis1][m].to_numpy() - markerless[joint_axis1][ml].to_numpy())**2)), 1)
#     ax02.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax02.transAxes)
#     ax02.set_xlim(0, 100)

#     ax03 = fig1.add_subplot(3,2,3)
#     ax03.plot(markers[joint_axis2][m], color='r')
#     ax03.plot(markerless[joint_axis2][ml], color='b')
#     ax03.set_title(f"{m} vs {ml}")
#     ax03.set_ylabel("Joint Angle [$^\circ$]")
#     ax03.set_xlim(0, 100)
#     # ax03.set_ylim(-40, 60)

#     ax04 = fig1.add_subplot(3,2,4)
#     ax04.plot(markers[joint_axis2][m].to_numpy() - markerless[joint_axis2][ml].to_numpy(), color='r', linewidth=3)
#     rmse = np.round(np.sqrt((np.mean(markers[joint_axis2][m].to_numpy() - markerless[joint_axis2][ml].to_numpy())**2)), 1)
#     ax04.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax04.transAxes)
#     ax04.set_xlim(0, 100)

#     ax05 = fig1.add_subplot(3,2,5)
#     ax05.plot(markers[joint_axis3][m], color='r')
#     ax05.plot(markerless[joint_axis3][ml], color='b')
#     ax05.set_title(f"{m} vs {ml}")
#     ax05.set_ylabel("Joint Angle [$^\circ$]")
#     ax05.set_xlim(0, 100)
#     # ax05.set_ylim(-40, 60)

#     ax06 = fig1.add_subplot(3,2,6)
#     ax06.plot(markers[joint_axis3][m].to_numpy() - markerless[joint_axis3][ml].to_numpy(), color='r', linewidth=3)
#     rmse = np.round(np.sqrt((np.mean(markers[joint_axis3][m].to_numpy() - markerless[joint_axis3][ml].to_numpy())**2)), 1)
#     ax06.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax06.transAxes)
#     ax06.set_xlim(0, 100)
#     plt.show()

# plot joint angle waveforms
fig = plt.figure()

ax1 = fig.add_subplot(3, 3, 1)
ax1.plot(markers["hip_flex"], color="r")
ax1.plot(markerless["hip_flex"], color="b")
ax1.set_title("Hip Flex/Ext")
ax1.set_ylabel("Joint Angle [$^\circ$]")
ax1.set_xlim(0, 100)
ax1.set_ylim(-40, 60)
ax1.grid()

ax2 = fig.add_subplot(3, 3, 2)
ax2.plot(markers["hip_ad_ab"], color="r")
ax2.plot(markerless["hip_ad_ab"], color="b")
ax2.set_title("Hip Ab/Ad")
ax2.set_xlim(0, 100)
ax2.set_ylim(-40, 60)
ax2.grid()

ax3 = fig.add_subplot(3, 3, 3)
ax3.plot(markers["hip_rot"], color="r")
ax3.plot(markerless["hip_rot"], color="b")
ax3.set_title("Hip Int/Ext Rot")
ax3.set_xlim(0, 100)
ax3.set_ylim(-40, 60)
ax3.grid()

ax4 = fig.add_subplot(3, 3, 4)
ax4.plot(markers["knee_flex"], color="r")
ax4.plot(markerless["knee_flex"], color="b")
ax4.set_title("Knee Flex/Ext")
ax4.set_ylabel("Joint Angle [$^\circ$]")
ax4.set_xlim(0, 100)
ax4.grid()

ax5 = fig.add_subplot(3, 3, 7)
ax5.plot(markers["ank_flex"], color="r")
ax5.plot(markerless["ank_flex"], color="b")
ax5.set_title("Ankle Flex/Ext")
ax5.set_xlabel("Step Cycle [%]")
ax5.set_ylabel("Joint Angle [$^\circ$]")
ax5.set_xlim(0, 100)
ax5.set_ylim(-40, 40)
ax5.grid()

ax6 = fig.add_subplot(3, 3, 8)
ax6.plot(markers["ank_ev_inv"], color="r")
ax6.plot(markerless["ank_ev_inv"], color="b")
ax6.set_title("Ankle Ab/Ad")
ax6.set_xlabel("Step Cycle [%]")
ax6.set_xlim(0, 100)
ax6.set_ylim(-40, 40)
ax6.grid()

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()

# plot differnce waveforms
fig = plt.figure()

ax1 = fig.add_subplot(3, 3, 1)
ax1.plot(
    np.mean(markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1
)
std = np.std(markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax1.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax1.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax1.transAxes,
)
ax1.set_title("Hip Flex/Ext")
ax1.set_ylabel("Diff [$^\circ$]")
ax1.set_xlim(0, 100)
ax1.set_ylim(-20, 20)
ax1.grid()

ax2 = fig.add_subplot(3, 3, 2)
ax2.plot(
    np.mean(
        markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
)
std = np.std(
    markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax2.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax2.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax2.transAxes,
)
ax2.set_title("Hip Ab/Ad")
ax2.set_xlim(0, 100)
ax2.set_ylim(-20, 20)
ax2.grid()

ax3 = fig.add_subplot(3, 3, 3)
ax3.plot(
    np.mean(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1)
std = np.std(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax3.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax3.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax3.transAxes,
)
ax3.set_title("Hip Int/Ext Rot")
ax3.set_xlim(0, 100)
ax3.set_ylim(-20, 20)
ax3.grid()

ax4 = fig.add_subplot(3, 3, 4)
ax4.plot(
    np.mean(
        markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
)
std = np.std(
    markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax4.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax4.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax4.transAxes,
)
ax4.set_title("Knee Flex/Ext")
ax4.set_ylabel("Diff [$^\circ$]")
ax4.set_xlim(0, 100)
ax4.set_ylim(-20, 20)
ax4.grid()

ax5 = fig.add_subplot(3, 3, 7)
ax5.plot(
    np.mean(markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1
)
std = np.std(markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax5.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax5.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax5.transAxes,
)
ax5.set_title("Ankle Flex/Ext")
ax5.set_xlabel("Step Cycle [%]")
ax5.set_ylabel("Diff [$^\circ$]")
ax5.set_xlim(0, 100)
ax5.set_ylim(-20, 20)
ax5.grid()

ax6 = fig.add_subplot(3, 3, 8)
ax6.plot(
    np.mean(
        markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
)
std = np.std(
    markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax6.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax6.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax6.transAxes,
)
ax6.set_title("Ankle Ab/Ad")
ax6.set_xlabel("Step Cycle [%]")
ax6.set_xlim(0, 100)
ax6.set_ylim(-20, 20)
ax6.grid()

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()

# combo plot - hip x,y,z
fig = plt.figure()

ax1 = fig.add_subplot(3, 3, 1)
ax1.plot(markers["hip_flex"], color="r")
ax1.plot(markerless["hip_flex"], color="b")
ax1.set_title("Hip Flex/Ext")
ax1.set_ylabel("Joint Angle [$^\circ$]")
ax1.set_xlim(0, 100)
ax1.set_ylim(-40, 60)
ax1.grid()

ax2 = fig.add_subplot(3, 3, 2)
ax2.plot(markers["hip_ad_ab"], color="r")
ax2.plot(markerless["hip_ad_ab"], color="b")
ax2.set_title("Hip Ab/Ad")
ax2.set_xlim(0, 100)
ax2.set_ylim(-40, 60)
ax2.grid()

ax3 = fig.add_subplot(3, 3, 3)
ax3.plot(markers["hip_rot"], color="r")
ax3.plot(markerless["hip_rot"], color="b")
ax3.set_title("Hip Int/Ext Rot")
ax3.set_xlim(0, 100)
ax3.set_ylim(-40, 60)
ax3.grid()

ax1 = fig.add_subplot(3, 3, 4)
ax1.plot(
    np.mean(markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1
)
std = np.std(markers["hip_flex"].to_numpy() - markerless["hip_flex"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax1.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax1.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax1.transAxes,
)
ax1.set_ylabel("Diff [$^\circ$]")
ax1.set_xlim(0, 100)
ax1.set_ylim(-20, 20)
ax1.set_xlabel("Step Cycle [%]")
ax1.grid()

ax2 = fig.add_subplot(3, 3, 5)
ax2.plot(
    np.mean(
        markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
)
std = np.std(
    markers["hip_ad_ab"].to_numpy() - markerless["hip_ad_ab"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax2.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax2.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax2.transAxes,
)
ax2.set_xlim(0, 100)
ax2.set_ylim(-20, 20)
ax2.set_xlabel("Step Cycle [%]")
ax2.grid()

ax3 = fig.add_subplot(3, 3, 6)
ax3.plot(
    np.mean(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1)
std = np.std(markers["hip_rot"].to_numpy() - markerless["hip_rot"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax3.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax3.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax3.transAxes,
)
ax3.set_xlim(0, 100)
ax3.set_ylim(-20, 20)
ax3.set_xlabel("Step Cycle [%]")
ax3.grid()

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()

# combo plot - ankle and knee
fig = plt.figure()

ax4 = fig.add_subplot(3, 3, 1)
ax4.plot(markers["knee_flex"], color="r")
ax4.plot(markerless["knee_flex"], color="b")
ax4.set_title("Knee Flex/Ext")
ax4.set_ylabel("Joint Angle [$^\circ$]")
ax4.set_xlabel("Step Cycle [%]")
ax4.set_xlim(0, 100)
ax4.set_ylim(0, 130)
ax4.grid()

ax5 = fig.add_subplot(3, 3, 2)
ax5.plot(markers["ank_flex"], color="r")
ax5.plot(markerless["ank_flex"], color="b")
ax5.set_title("Ankle Flex/Ext")
ax5.set_xlabel("Step Cycle [%]")
ax5.set_xlim(0, 100)
ax5.set_ylim(-40, 40)
ax5.grid()

ax6 = fig.add_subplot(3, 3, 3)
ax6.plot(markers["ank_ev_inv"], color="r")
ax6.plot(markerless["ank_ev_inv"], color="b")
ax6.set_title("Ankle Ab/Ad")
ax6.set_xlabel("Step Cycle [%]")
ax6.set_xlim(0, 100)
ax6.set_ylim(-40, 40)
ax6.grid()

ax4 = fig.add_subplot(3, 3, 4)
ax4.plot(
    np.mean(
        markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
)
std = np.std(
    markers["knee_flex"].to_numpy() - markerless["knee_flex"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax4.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax4.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax4.transAxes,
)
ax4.set_ylabel("Diff [$^\circ$]")
ax4.set_xlabel("Step Cycle [%]")
ax4.set_xlim(0, 100)
ax4.set_ylim(-20, 20)
ax4.grid()

ax5 = fig.add_subplot(3, 3, 5)
ax5.plot(
    np.mean(markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1
)
std = np.std(markers["ank_flex"].to_numpy() - markerless["ank_flex"].to_numpy(), axis=1)
x = np.arange(0, 101)
ax5.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax5.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax5.transAxes,
)
ax5.set_xlabel("Step Cycle [%]")
ax5.set_xlim(0, 100)
ax5.set_ylim(-20, 20)
ax5.grid()

ax6 = fig.add_subplot(3, 3, 6)
ax6.plot(
    np.mean(
        markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
    ),
    color="r",
    linewidth=3,
)
mean = np.mean(
    markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
)
std = np.std(
    markers["ank_ev_inv"].to_numpy() - markerless["ank_ev_inv"].to_numpy(), axis=1
)
x = np.arange(0, 101)
ax6.fill_between(x, mean - std, mean + std, color="gray", alpha=0.3)
rmse = np.round(np.sqrt((np.mean(mean) ** 2)), 1)
ax6.text(
    0,
    0,
    f"RMSE = {rmse}$^\circ$",
    fontsize=18,
    horizontalalignment="left",
    verticalalignment="bottom",
    transform=ax6.transAxes,
)
ax6.set_xlabel("Step Cycle [%]")
ax6.set_xlim(0, 100)
ax6.set_ylim(-20, 20)
ax6.grid()

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()
