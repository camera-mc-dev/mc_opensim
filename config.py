"""Config file for BatchIK and TrcGenerator

"""


# Set path to directory containing data. Data can seperated into 
# futher subdirectories as all subdirs will be searched recursively.
PATH = "/home/ln424/Downloads/mc_opensim_test/markers"


#
# GENERAL SETTINGS
#

# Are we working with markerless data i.e. COCO keypoint outputs? If
# so, set to True. Otherwise if using BioCV markerset based data set
# to False. Other models will require custom paths settings
IS_MARKERLESS = False

# It is assumed that default .osim, scale settings (.xml) and IK settings
# (.xml) are stored here for both marker and markerless data. Defaults
# will be used unless and custom path is supplied.
DEFAULT_MODELS_PATH = "./configs/"

# Use to set a path to a custom model or custom scaling/IK settings. To 
# use default option, ensure that custom path is set to None.
CUSTOM_MODEL_PATH = None
CUSTOM_SCALE_SETTINGS_PATH = None
CUSTOM_IK_SETTINGS_PATH = None


#
# TRC GENERATION SETTINGS
#

# We can attempt to validate the .trc files that we create and if
# they fail, attempt to fix them. However, this will increase 
# processing time.
VALIDATE_TRC = True

# During .trc generation we can apply a rotation to the coordinate
# global coordinate system if needed. OpenSim expects the y-axis to
# be normal to the x-z ground plane. If no rotation is needed set 
# each rotation var to 0.
# The rotation in degree to be applied to each axis.
ROTATE_X = -90
ROTATE_Y = 0
ROTATE_Z = -90


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
IK_TIME_RANGE = [0, 0.2]

# Flag indicating whether or not to report 
# marker errors from the inverse kinematics solution.
IK_REPORT_ERRORS = False

# Flag indicating whether or not to report model marker 
# locations. Note, model marker locations are expressed in Ground.
IK_REPORT_MARKER_LOCATIONS = False