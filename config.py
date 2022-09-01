"""Config file for BatchIK


"""

#
# GENERAL SETTINGS
#

# Set path to directory containing data. Data can seperated into 
# futher subdirectories as all subdirs will be searched recursively.
PATH = "/test/test/test/"

# Are we working with markerless data i.e. COCO keypoint outputs? If
# so, set to True. Otherwise if using BioCV markerset based data set
# to False. Other models will require custom paths settings
IS_MARKERLESS = True

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

# Set to True if we want to search for .c3d files and convert them
# to an OpenSim .trc format. If set to false we will assume that
# .trc files already exist and search for those instead of .c3ds.
CONVERT_C3D = True

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

#
SCALE_MODEL = True

#
STATIC_NAME = "STATIC"

#
SCALE_TIME_RANGE = [0, 1]


#
# IK SETTINGS
#


# Set to run the IK solver
RUN_IK = True

IK_TIME_RANGE = [0, 100]
IK_REPORT_ERRORS = False
IK_REPORT_MARKER_LOCATIONS = False