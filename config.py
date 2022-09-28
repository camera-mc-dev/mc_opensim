"""Config file for BatchIK and TrcGenerator

"""


# Set path to directory containing data. Data can seperated into 
# futher subdirectories as all subdirs will be searched recursively.
PATH = "/data2/bioCV/27/P27_RUN_01/op-recon/"
#PATH = "/data2/bioCV/27/P27_RUN_01/op-fused/"
#PATH = "/data2/bioCV/27/P27_RUN_01/"


#
# GENERAL SETTINGS
#

# Deprecated: The tool now gueses based on filename so that as it walks
#             through the directories it can choose for each file it finds.
#             thus, marker files _must_ now be markers.c3d otherwise it 
#             assumes markerless.
# Are we working with markerless data i.e. COCO keypoint outputs? If
# so, set to True. Otherwise if using BioCV markerset based data set
# to False. Other models will require custom paths settings
# IS_MARKERLESS = True

# It is assumed that default .osim, scale settings (.xml) and IK settings
# (.xml) are stored here for both marker and markerless data. Defaults
# will be used unless and custom path is supplied.
DEFAULT_MODELS_PATH = "./configs/"

# Use to set a path to a custom model or custom scaling/IK settings. To 
# use default option, ensure that custom path is set to None.
CUSTOM_MODEL_PATH = None
CUSTOM_SCALE_SETTINGS_PATH = None
CUSTOM_IK_SETTINGS_PATH = None

# Where are the opensim binaries (leave as None if installed on your path)
OPENSIM_BINARY_PATH = "/home/muzz/programming/notmine/opensim/opensim_install/bin/"


#
# Smoothing settings
#
# Previous work has used 0.01 and 15 for trans and obs respectively.
# But we can ask PyKalman to estimate suitable parameters. To do that
# set these to < 0
#

KALMAN_TRANS_NOISE = -1.0
KALMAN_OBS_NOISE   = -1.0





#
# TRC GENERATION SETTINGS
#

# We can attempt to validate the .trc files that we create and if
# they fail, attempt to fix them. However, this will increase 
# processing time.
VALIDATE_TRC = True

# Here in CAMERA we like to use z-up and and x-y ground plane.
# However, OpenSim is one of those weirdos that like to use
# y-up and an x-z ground plane, and thus the IK solver expects that.
# So _we_ apply a -90 degree rotation when converting our .c3d to .trc
# You, of course, may want to do something different.
ROTATE_X = -90
ROTATE_Y = 0
ROTATE_Z = 0


#
# SCALING SETTINGS
#

# Set to true if you want to search for static trails and generate
# a scaled osim model from that trial.
SCALE_MODEL = True

# The search will check that this sub string is present within any
# trc files that it finds. This can be useful if we have multiple
# statics within a session.
STATIC_NAME = "STATIC_01"

# Specifies the start and end times for the IK computation. Time 
# values are in whatever units of time were used in the marker and 
# coordinate files
SCALE_TIME_RANGE = [0, 1]


#
# IK SETTINGS
#

# Set to run the IK solver on any trc files that are found.
RUN_IK = True

# Specifies the start and end times for the IK computation. Time 
# values are in whatever units of time were used in the marker and 
# coordinate files
IK_TIME_RANGE = [0, 5.0]

# Flag indicating whether or not to report 
# marker errors from the inverse kinematics solution.
IK_REPORT_ERRORS = False

# Flag indicating whether or not to report model marker 
# locations. Note, model marker locations are expressed in Ground.
IK_REPORT_MARKER_LOCATIONS = False
