"""plot_utils.py

Plotting functions for bioCV data papers
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

font = {"size": 16}
plt.rc("font", **font)
plt.rcParams["figure.figsize"] = 10, 20


def hip_joint_plot(jump_data, walk_data, run_data, dpi=600, save_path=None):

    # for i in range(len(jump_data["markers"])):
    #     fig = plt.figure()
    #     ax3 = fig.add_subplot(6,3,3)
    #     ax3.plot(run_data["markers"]["hip_flex"].iloc[:,i], color='r')
    #     ax3.plot(run_data["markerless"]["hip_flex"].iloc[:,i], color='b')
    #     a = run_data["markers"]["hip_flex"].columns[i]
    #     ax3.set_title(f"{a}")
    #     ax3.set_xlim(0, 100)
    #     ax3.set_ylim(-30, 70)
    #     ax3.grid()
    #     blue_line = mlines.Line2D([], [], color='blue',label='Markerless')
    #     red_line = mlines.Line2D([], [], color='red',label='Markers')
    #     ax3.legend(handles=[blue_line, red_line], prop={"size":10,}, frameon=False)

    # combo plot - lumbar x,y,z
    fig = plt.figure()

    ax1 = fig.add_subplot(6, 3, 1)
    ax1.plot(jump_data["markers"]["hip_flex"], color="r")
    ax1.plot(jump_data["markerless"]["hip_flex"], color="b")
    ax1.set_title(f"Jumping")
    ax1.set_ylabel("Hip Flex/Ext [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(-30, 70)
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 2)
    ax2.plot(walk_data["markers"]["hip_flex"], color="r")
    ax2.plot(walk_data["markerless"]["hip_flex"], color="b")
    ax2.set_title(f"Walking")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-30, 70)
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 3)
    ax3.plot(run_data["markers"]["hip_flex"], color="r")
    ax3.plot(run_data["markerless"]["hip_flex"], color="b")
    ax3.set_title(f"Running")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(-30, 70)
    ax3.grid()
    blue_line = mlines.Line2D([], [], color="blue", label="Markerless")
    red_line = mlines.Line2D([], [], color="red", label="Markers")
    ax3.legend(
        handles=[blue_line, red_line],
        prop={
            "size": 10,
        },
        frameon=False,
        loc="upper left",
    )

    ax1 = fig.add_subplot(6, 3, 4)
    ax1.plot(
        np.mean(
            jump_data["markers"]["hip_flex"].to_numpy()
            - jump_data["markerless"]["hip_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        jump_data["markers"]["hip_flex"].to_numpy()
        - jump_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        jump_data["markers"]["hip_flex"].to_numpy()
        - jump_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
    )
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
    # ax1.set_xlabel("Jump Cycle [%]")
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 5)
    ax2.plot(
        np.mean(
            walk_data["markers"]["hip_flex"].to_numpy()
            - walk_data["markerless"]["hip_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        walk_data["markers"]["hip_flex"].to_numpy()
        - walk_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        walk_data["markers"]["hip_flex"].to_numpy()
        - walk_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
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
    # ax2.set_xlabel("Gait Cycle [%]")
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 6)
    ax3.plot(
        np.mean(
            run_data["markers"]["hip_flex"].to_numpy()
            - run_data["markerless"]["hip_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        run_data["markers"]["hip_flex"].to_numpy()
        - run_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        run_data["markers"]["hip_flex"].to_numpy()
        - run_data["markerless"]["hip_flex"].to_numpy(),
        axis=1,
    )
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
    # ax3.set_xlabel("Step Cycle [%]")
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 7)
    ax1.plot(jump_data["markers"]["hip_ad_ab"], color="r")
    ax1.plot(jump_data["markerless"]["hip_ad_ab"], color="b")
    # ax1.set_title(f"Jumping")
    ax1.set_ylabel("Hip Ad/Abduction [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(-40, 40)
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 8)
    ax2.plot(walk_data["markers"]["hip_ad_ab"], color="r")
    ax2.plot(walk_data["markerless"]["hip_ad_ab"], color="b")
    # ax2.set_title(f"Walking")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-40, 40)
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 9)
    ax3.plot(run_data["markers"]["hip_ad_ab"], color="r")
    ax3.plot(run_data["markerless"]["hip_ad_ab"], color="b")
    # ax3.set_title(f"Running")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(-40, 40)
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 10)
    ax1.plot(
        np.mean(
            jump_data["markers"]["hip_ad_ab"].to_numpy()
            - jump_data["markerless"]["hip_ad_ab"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        jump_data["markers"]["hip_ad_ab"].to_numpy()
        - jump_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
    )
    std = np.std(
        jump_data["markers"]["hip_ad_ab"].to_numpy()
        - jump_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
    )
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
    # ax1.set_xlabel("Jump Cycle [%]")
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 11)
    ax2.plot(
        np.mean(
            walk_data["markers"]["hip_ad_ab"].to_numpy()
            - walk_data["markerless"]["hip_ad_ab"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        walk_data["markers"]["hip_ad_ab"].to_numpy()
        - walk_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
    )
    std = np.std(
        walk_data["markers"]["hip_ad_ab"].to_numpy()
        - walk_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
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
    # ax2.set_xlabel("Gait Cycle [%]")
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 12)
    ax3.plot(
        np.mean(
            run_data["markers"]["hip_ad_ab"].to_numpy()
            - run_data["markerless"]["hip_ad_ab"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        run_data["markers"]["hip_ad_ab"].to_numpy()
        - run_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
    )
    std = np.std(
        run_data["markers"]["hip_ad_ab"].to_numpy()
        - run_data["markerless"]["hip_ad_ab"].to_numpy(),
        axis=1,
    )
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
    # ax3.set_xlabel("Step Cycle [%]")
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 13)
    ax1.plot(jump_data["markers"]["hip_rot"], color="r")
    ax1.plot(jump_data["markerless"]["hip_rot"], color="b")
    # ax1.set_title(f"Jumping")
    ax1.set_ylabel("Int/Ext Rotation [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(-40, 40)
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 14)
    ax2.plot(walk_data["markers"]["hip_rot"], color="r")
    ax2.plot(walk_data["markerless"]["hip_rot"], color="b")
    # ax2.set_title(f"Walking")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-40, 40)
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 15)
    ax3.plot(run_data["markers"]["hip_rot"], color="r")
    ax3.plot(run_data["markerless"]["hip_rot"], color="b")
    # ax3.set_title(f"Running")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(-40, 40)
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 16)
    ax1.plot(
        np.mean(
            jump_data["markers"]["hip_rot"].to_numpy()
            - jump_data["markerless"]["hip_rot"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        jump_data["markers"]["hip_rot"].to_numpy()
        - jump_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
    )
    std = np.std(
        jump_data["markers"]["hip_rot"].to_numpy()
        - jump_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
    )
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
    ax1.set_xlabel("Jump Cycle [%]")
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 17)
    ax2.plot(
        np.mean(
            walk_data["markers"]["hip_rot"].to_numpy()
            - walk_data["markerless"]["hip_rot"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        walk_data["markers"]["hip_rot"].to_numpy()
        - walk_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
    )
    std = np.std(
        walk_data["markers"]["hip_rot"].to_numpy()
        - walk_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
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
    ax2.set_xlabel("Gait Cycle [%]")
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 18)
    ax3.plot(
        np.mean(
            run_data["markers"]["hip_rot"].to_numpy()
            - run_data["markerless"]["hip_rot"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        run_data["markers"]["hip_rot"].to_numpy()
        - run_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
    )
    std = np.std(
        run_data["markers"]["hip_rot"].to_numpy()
        - run_data["markerless"]["hip_rot"].to_numpy(),
        axis=1,
    )
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
    ax3.set_xlabel("Gait Cycle [%]")
    ax3.grid()

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    if save_path is not None:
        path = os.path.join(save_path, "hip_joint_plot.png")
        plt.savefig(path, dpi=dpi)
        print(f"INFO - Saved figure: {path}")
    plt.show()


# def hip_joint_plot(data, act):
#     # combo plot - hip x,y,z
#     fig = plt.figure()

#     ax1 = fig.add_subplot(3,3,1)
#     ax1.plot(data["markers"]["hip_flex"], color='r')
#     ax1.plot(data["markerless"]["hip_flex"], color='b')
#     ax1.set_title(f"Hip Flex/Ext - {act}")
#     ax1.set_ylabel("Joint Angle [$^\circ$]")
#     ax1.set_xlim(0, 100)
#     ax1.set_ylim(-40, 60)
#     ax1.grid()

#     ax2 = fig.add_subplot(3,3,2)
#     ax2.plot(data["markers"]["hip_ad_ab"], color='r')
#     ax2.plot(data["markerless"]["hip_ad_ab"], color='b')
#     ax2.set_title(f"Hip Ab/Ad - {act}")
#     ax2.set_xlim(0, 100)
#     ax2.set_ylim(-40, 60)
#     ax2.grid()

#     ax3 = fig.add_subplot(3,3,3)
#     ax3.plot(data["markers"]["hip_rot"], color='r')
#     ax3.plot(data["markerless"]["hip_rot"], color='b')
#     ax3.set_title(f"Hip Int/Ext Rot - {act}")
#     ax3.set_xlim(0, 100)
#     ax3.set_ylim(-40, 60)
#     ax3.grid()

#     ax1 = fig.add_subplot(3,3,4)
#     ax1.plot(np.mean(data["markers"]["hip_flex"].to_numpy() - data["markerless"]["hip_flex"].to_numpy(), axis=1), color='r', linewidth=3)
#     mean = np.mean(data["markers"]["hip_flex"].to_numpy() - data["markerless"]["hip_flex"].to_numpy(), axis=1)
#     std = np.std(data["markers"]["hip_flex"].to_numpy() - data["markerless"]["hip_flex"].to_numpy(), axis=1)
#     x = np.arange(0,101)
#     ax1.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     ax1.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax1.transAxes)
#     ax1.set_ylabel("Diff [$^\circ$]")
#     ax1.set_xlim(0, 100)
#     ax1.set_ylim(-20, 20)
#     ax1.set_xlabel("Step Cycle [%]")
#     ax1.grid()

#     ax2 = fig.add_subplot(3,3,5)
#     ax2.plot(np.mean(data["markers"]["hip_ad_ab"].to_numpy() - data["markerless"]["hip_ad_ab"].to_numpy(), axis=1), color='r', linewidth=3)
#     mean = np.mean(data["markers"]["hip_ad_ab"].to_numpy() - data["markerless"]["hip_ad_ab"].to_numpy(), axis=1)
#     std = np.std(data["markers"]["hip_ad_ab"].to_numpy() - data["markerless"]["hip_ad_ab"].to_numpy(), axis=1)
#     x = np.arange(0,101)
#     ax2.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     ax2.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax2.transAxes)
#     ax2.set_xlim(0, 100)
#     ax2.set_ylim(-20, 20)
#     ax2.set_xlabel("Step Cycle [%]")
#     ax2.grid()

#     ax3 = fig.add_subplot(3,3,6)
#     ax3.plot(np.mean(data["markers"]["hip_rot"].to_numpy() - data["markerless"]["hip_rot"].to_numpy(), axis=1), color='r', linewidth=3)
#     mean = np.mean(data["markers"]["hip_rot"].to_numpy() - data["markerless"]["hip_rot"].to_numpy(), axis=1)
#     std = np.std(data["markers"]["hip_rot"].to_numpy() - data["markerless"]["hip_rot"].to_numpy(), axis=1)
#     x = np.arange(0,101)
#     ax3.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     ax3.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax3.transAxes)
#     ax3.set_xlim(0, 100)
#     ax3.set_ylim(-20, 20)
#     ax3.set_xlabel("Step Cycle [%]")
#     ax3.grid()

#     plt.subplots_adjust(wspace=0.3, hspace=0.3)
#     plt.show()


def knee_ank_joint_plot(jump_data, walk_data, run_data, dpi=600, save_path=None):
    # combo plot - lumbar x,y,z

    # for i in range(len(jump_data["markers"])):
    #     fig = plt.figure()
    #     ax3 = fig.add_subplot(6,3,3)
    #     ax3.plot(run_data["markers"]["knee_flex"].iloc[:,i], color='r')
    #     ax3.plot(run_data["markerless"]["knee_flex"].iloc[:,i], color='b')
    #     a = run_data["markers"]["knee_flex"].columns[i]
    #     ax3.set_title(f"{a}")
    #     ax3.set_xlim(0, 100)
    #     ax3.set_ylim(0, 140)
    #     ax3.grid()
    #     blue_line = mlines.Line2D([], [], color='blue',label='Markerless')
    #     red_line = mlines.Line2D([], [], color='red',label='Markers')
    #     ax3.legend(handles=[blue_line, red_line], prop={"size":10,}, frameon=False)

    fig = plt.figure()

    ax1 = fig.add_subplot(6, 3, 1)
    ax1.plot(jump_data["markers"]["knee_flex"], color="r")
    ax1.plot(jump_data["markerless"]["knee_flex"], color="b")
    ax1.set_title(f"Jumping")
    ax1.set_ylabel("Knee Flex/Ext [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 140)
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 2)
    ax2.plot(walk_data["markers"]["knee_flex"], color="r")
    ax2.plot(walk_data["markerless"]["knee_flex"], color="b")
    ax2.set_title(f"Walking")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 140)
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 3)
    ax3.plot(run_data["markers"]["knee_flex"], color="r")
    ax3.plot(run_data["markerless"]["knee_flex"], color="b")
    ax3.set_title(f"Running")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 140)
    ax3.grid()
    blue_line = mlines.Line2D([], [], color="blue", label="Markerless")
    red_line = mlines.Line2D([], [], color="red", label="Markers")
    ax3.legend(
        handles=[blue_line, red_line],
        prop={"size": 10},
        frameon=False,
        loc="upper left",
    )

    ax1 = fig.add_subplot(6, 3, 4)
    ax1.plot(
        np.mean(
            jump_data["markers"]["knee_flex"].to_numpy()
            - jump_data["markerless"]["knee_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        jump_data["markers"]["knee_flex"].to_numpy()
        - jump_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        jump_data["markers"]["knee_flex"].to_numpy()
        - jump_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
    )
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
    # ax1.set_xlabel("Jump Cycle [%]")
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 5)
    ax2.plot(
        np.mean(
            walk_data["markers"]["knee_flex"].to_numpy()
            - walk_data["markerless"]["knee_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        walk_data["markers"]["knee_flex"].to_numpy()
        - walk_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        walk_data["markers"]["knee_flex"].to_numpy()
        - walk_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
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
    # ax2.set_xlabel("Gait Cycle [%]")
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 6)
    ax3.plot(
        np.mean(
            run_data["markers"]["knee_flex"].to_numpy()
            - run_data["markerless"]["knee_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        run_data["markers"]["knee_flex"].to_numpy()
        - run_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        run_data["markers"]["knee_flex"].to_numpy()
        - run_data["markerless"]["knee_flex"].to_numpy(),
        axis=1,
    )
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
    # ax3.set_xlabel("Step Cycle [%]")
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 7)
    ax1.plot(jump_data["markers"]["ank_flex"], color="r")
    ax1.plot(jump_data["markerless"]["ank_flex"], color="b")
    # ax1.set_title(f"Jumping")
    ax1.set_ylabel("Dorsi/Plantar Flexion [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(-50, 50)
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 8)
    ax2.plot(walk_data["markers"]["ank_flex"], color="r")
    ax2.plot(walk_data["markerless"]["ank_flex"], color="b")
    # ax2.set_title(f"Walking")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-50, 50)
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 9)
    ax3.plot(run_data["markers"]["ank_flex"], color="r")
    ax3.plot(run_data["markerless"]["ank_flex"], color="b")
    # ax3.set_title(f"Running")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(-50, 50)
    ax3.grid()

    ax1 = fig.add_subplot(6, 3, 10)
    ax1.plot(
        np.mean(
            jump_data["markers"]["ank_flex"].to_numpy()
            - jump_data["markerless"]["ank_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        jump_data["markers"]["ank_flex"].to_numpy()
        - jump_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        jump_data["markers"]["ank_flex"].to_numpy()
        - jump_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
    )
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
    ax1.set_xlabel("Jump Cycle [%]")
    ax1.grid()

    ax2 = fig.add_subplot(6, 3, 11)
    ax2.plot(
        np.mean(
            walk_data["markers"]["ank_flex"].to_numpy()
            - walk_data["markerless"]["ank_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        walk_data["markers"]["ank_flex"].to_numpy()
        - walk_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        walk_data["markers"]["ank_flex"].to_numpy()
        - walk_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
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
    ax2.set_xlabel("Gait Cycle [%]")
    ax2.grid()

    ax3 = fig.add_subplot(6, 3, 12)
    ax3.plot(
        np.mean(
            run_data["markers"]["ank_flex"].to_numpy()
            - run_data["markerless"]["ank_flex"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        run_data["markers"]["ank_flex"].to_numpy()
        - run_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
    )
    std = np.std(
        run_data["markers"]["ank_flex"].to_numpy()
        - run_data["markerless"]["ank_flex"].to_numpy(),
        axis=1,
    )
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
    ax3.set_xlabel("Gait Cycle [%]")
    ax3.grid()

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    if save_path is not None:
        path = os.path.join(save_path, "knee_ankle_joint_plot.png")
        plt.savefig(path, dpi=dpi)
        print(f"INFO - Saved figure: {path}")
    plt.show()


# def knee_ank_joint_plot(data, act):
#     # combo plot - ankle and knee
#     fig = plt.figure()

#     ax4 = fig.add_subplot(3,3,1)
#     ax4.plot(data["markers"]["knee_flex"], color='r')
#     ax4.plot(data["markerless"]["knee_flex"], color='b')
#     ax4.set_title(f"Knee Flex/Ext - {act}")
#     ax4.set_ylabel("Joint Angle [$^\circ$]")
#     ax4.set_xlabel("Step Cycle [%]")
#     ax4.set_xlim(0, 100)
#     ax4.set_ylim(0, 130)
#     ax4.grid()

#     ax5 = fig.add_subplot(3,3,2)
#     ax5.plot(data["markers"]["ank_flex"], color='r')
#     ax5.plot(data["markerless"]["ank_flex"], color='b')
#     ax5.set_title(f"Ankle Flex/Ext - {act}")
#     ax5.set_xlabel("Step Cycle [%]")
#     ax5.set_xlim(0, 100)
#     ax5.set_ylim(-40, 40)
#     ax5.grid()

#     # ax6 = fig.add_subplot(3,3,3)
#     # ax6.plot(data["markers"]["ank_ev_inv"], color='r')
#     # ax6.plot(data["markerless"]["ank_ev_inv"], color='b')
#     # ax6.set_title(f"Ankle Ab/Ad - {act}")
#     # ax6.set_xlabel("Step Cycle [%]")
#     # ax6.set_xlim(0, 100)
#     # ax6.set_ylim(-40, 40)
#     # ax6.grid()

#     ax4 = fig.add_subplot(3,3,4)
#     ax4.plot(np.mean(data["markers"]["knee_flex"].to_numpy() - data["markerless"]["knee_flex"].to_numpy(), axis=1), color='r', linewidth=3)
#     mean = np.mean(data["markers"]["knee_flex"].to_numpy() - data["markerless"]["knee_flex"].to_numpy(), axis=1)
#     std = np.std(data["markers"]["knee_flex"].to_numpy() - data["markerless"]["knee_flex"].to_numpy(), axis=1)
#     x = np.arange(0,101)
#     ax4.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     ax4.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax4.transAxes)
#     ax4.set_ylabel("Diff [$^\circ$]")
#     ax4.set_xlabel("Step Cycle [%]")
#     ax4.set_xlim(0, 100)
#     ax4.set_ylim(-20, 20)
#     ax4.grid()

#     ax5 = fig.add_subplot(3,3,5)
#     ax5.plot(np.mean(data["markers"]["ank_flex"].to_numpy() - data["markerless"]["ank_flex"].to_numpy(), axis=1), color='r', linewidth=3)
#     mean = np.mean(data["markers"]["ank_flex"].to_numpy() - data["markerless"]["ank_flex"].to_numpy(), axis=1)
#     std = np.std(data["markers"]["ank_flex"].to_numpy() - data["markerless"]["ank_flex"].to_numpy(), axis=1)
#     x = np.arange(0,101)
#     ax5.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     ax5.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax5.transAxes)
#     ax5.set_xlabel("Step Cycle [%]")
#     ax5.set_xlim(0, 100)
#     ax5.set_ylim(-20, 20)
#     ax5.grid()

#     # ax6 = fig.add_subplot(3,3,6)
#     # ax6.plot(np.mean(data["markers"]["ank_ev_inv"].to_numpy() - data["markerless"]["ank_ev_inv"].to_numpy(), axis=1), color='r', linewidth=3)
#     # mean = np.mean(data["markers"]["ank_ev_inv"].to_numpy() - data["markerless"]["ank_ev_inv"].to_numpy(), axis=1)
#     # std = np.std(data["markers"]["ank_ev_inv"].to_numpy() - data["markerless"]["ank_ev_inv"].to_numpy(), axis=1)
#     # x = np.arange(0,101)
#     # ax6.fill_between(x, mean-std, mean+std, color="gray", alpha=0.3)
#     # rmse = np.round(np.sqrt((np.mean(mean)**2)), 1)
#     # ax6.text(0, 0, f"RMSE = {rmse}$^\circ$", fontsize=18, horizontalalignment='left', verticalalignment='bottom', transform=ax6.transAxes)
#     # ax6.set_xlabel("Step Cycle [%]")
#     # ax6.set_xlim(0, 100)
#     # ax6.set_ylim(-20, 20)
#     # ax6.grid()

#     plt.subplots_adjust(wspace=0.3, hspace=0.3)
#     plt.show()


def orientation_plot(data, segment, act, seg_name):
    # combo plot - x,y,z
    fig = plt.figure()

    ax1 = fig.add_subplot(3, 3, 1)
    ax1.plot(data["markers"][f"{segment}_x"], color="r")
    ax1.plot(data["markerless"][f"{segment}_x"], color="b")
    ax1.set_title(f"{seg_name} X Rotation - {act}")
    ax1.set_ylabel("Orientation Angle [$^\circ$]")
    ax1.set_xlim(0, 100)
    # ax1.set_ylim(-40, 60)
    ax1.grid()

    ax2 = fig.add_subplot(3, 3, 2)
    ax2.plot(data["markers"][f"{segment}_y"], color="r")
    ax2.plot(data["markerless"][f"{segment}_y"], color="b")
    ax2.set_title(f"{seg_name} Y Rotation - {act}")
    ax2.set_xlim(0, 100)
    # ax2.set_ylim(-40, 60)
    ax2.grid()

    ax3 = fig.add_subplot(3, 3, 3)
    ax3.plot(data["markers"][f"{segment}_z"], color="r")
    ax3.plot(data["markerless"][f"{segment}_z"], color="b")
    ax3.set_title(f"{seg_name} Z Rotation - {act}")
    ax3.set_xlim(0, 100)
    # ax3.set_ylim(-40, 60)
    ax3.grid()

    ax1 = fig.add_subplot(3, 3, 4)
    ax1.plot(
        np.mean(
            data["markers"][f"{segment}_x"].to_numpy()
            - data["markerless"][f"{segment}_x"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        data["markers"][f"{segment}_x"].to_numpy()
        - data["markerless"][f"{segment}_x"].to_numpy(),
        axis=1,
    )
    std = np.std(
        data["markers"][f"{segment}_x"].to_numpy()
        - data["markerless"][f"{segment}_x"].to_numpy(),
        axis=1,
    )
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
            data["markers"][f"{segment}_y"].to_numpy()
            - data["markerless"][f"{segment}_y"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        data["markers"][f"{segment}_y"].to_numpy()
        - data["markerless"][f"{segment}_y"].to_numpy(),
        axis=1,
    )
    std = np.std(
        data["markers"][f"{segment}_y"].to_numpy()
        - data["markerless"][f"{segment}_y"].to_numpy(),
        axis=1,
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
        np.mean(
            data["markers"][f"{segment}_z"].to_numpy()
            - data["markerless"][f"{segment}_z"].to_numpy(),
            axis=1,
        ),
        color="r",
        linewidth=3,
    )
    mean = np.mean(
        data["markers"][f"{segment}_z"].to_numpy()
        - data["markerless"][f"{segment}_z"].to_numpy(),
        axis=1,
    )
    std = np.std(
        data["markers"][f"{segment}_z"].to_numpy()
        - data["markerless"][f"{segment}_z"].to_numpy(),
        axis=1,
    )
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


def plot_temp_data(data, trial):
    fig = plt.figure()

    ax1 = fig.add_subplot(3, 3, 1)
    ax1.plot(data["markers"]["hip_flex"][trial], color="r")
    ax1.plot(data["markerless"]["hip_flex"][trial], color="b")
    ax1.set_title(f"Hip Flex/Ext - {trial}")
    ax1.set_ylabel("Joint Angle [$^\circ$]")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(-40, 60)
    ax1.grid()

    ax2 = fig.add_subplot(3, 3, 2)
    ax2.plot(data["markers"]["hip_ad_ab"][trial], color="r")
    ax2.plot(data["markerless"]["hip_ad_ab"][trial], color="b")
    ax2.set_title(f"Hip Ab/Ad - {trial}")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-40, 60)
    ax2.grid()

    ax3 = fig.add_subplot(3, 3, 3)
    ax3.plot(data["markers"]["hip_rot"][trial], color="r")
    ax3.plot(data["markerless"]["hip_rot"][trial], color="b")
    ax3.set_title(f"Hip Int/Ext Rot - {trial}")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(-40, 60)
    ax3.grid()

    ax4 = fig.add_subplot(3, 3, 4)
    ax4.plot(data["markers"]["knee_flex"][trial], color="r")
    ax4.plot(data["markerless"]["knee_flex"][trial], color="b")
    ax4.set_title(f"Knee Flex/Ext - {trial}")
    ax4.set_ylabel("Joint Angle [$^\circ$]")
    ax4.set_xlabel("Step Cycle [%]")
    ax4.set_xlim(0, 100)
    ax4.set_ylim(0, 130)
    ax4.grid()

    ax5 = fig.add_subplot(3, 3, 5)
    ax5.plot(data["markers"]["ank_flex"][trial], color="r")
    ax5.plot(data["markerless"]["ank_flex"][trial], color="b")
    ax5.set_title(f"Ankle Flex/Ext - {trial}")
    ax5.set_xlabel("Step Cycle [%]")
    ax5.set_xlim(0, 100)
    ax5.set_ylim(-40, 40)
    ax5.grid()

    ax6 = fig.add_subplot(3, 3, 6)
    ax6.plot(data["markers"]["ank_ev_inv"][trial], color="r")
    ax6.plot(data["markerless"]["ank_ev_inv"][trial], color="b")
    ax6.set_title(f"Ankle Ab/Ad - {trial}")
    ax6.set_xlabel("Step Cycle [%]")
    ax6.set_xlim(0, 100)
    ax6.set_ylim(-40, 40)
    ax6.grid()

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.draw()
    check = plt.waitforbuttonpress(0)
    if check:
        plt.close(fig)
        return None
    else:
        plt.close(fig)
        return trial


def plot_temp_lumbar_data(data, trial):
    fig = plt.figure()

    ax1 = fig.add_subplot(1, 3, 1)
    ax1.plot(data["markers"]["hip_ad_ab"][trial], color="r")
    ax1.plot(data["markerless"]["hip_ad_ab"][trial], color="b")
    ax1.set_title(f"Lumbar Flex/Ext - {trial}")
    ax1.set_ylabel("Joint Angle [$^\circ$]")
    ax1.set_xlim(0, 100)
    # ax1.set_ylim(-40, 60)
    ax1.grid()

    ax2 = fig.add_subplot(1, 3, 2)
    ax2.plot(data["markers"]["lumbar_bending"][trial], color="r")
    ax2.plot(data["markerless"]["lumbar_bending"][trial], color="b")
    ax2.set_title(f"Lumbar Bending - {trial}")
    ax2.set_xlim(0, 100)
    # ax2.set_ylim(-40, 60)
    ax2.grid()

    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(data["markers"]["lumbar_rotation"][trial], color="r")
    ax3.plot(data["markerless"]["lumbar_rotation"][trial], color="b")
    ax3.set_title(f"Lumbar Rot - {trial}")
    ax3.set_xlim(0, 100)
    # ax3.set_ylim(-40, 60)
    ax3.grid()

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.draw()
    check = plt.waitforbuttonpress(0)
    if check:
        plt.close(fig)
        return None
    else:
        plt.close(fig)
        return trial
