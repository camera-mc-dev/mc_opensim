# mc_opensim

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

**Tools for running [mc_reconstruction](https://github.com/camera-mc-dev) outputs through [OpenSim's](https://github.com/opensim-org/opensim-core) IK solver**

A set of scripts to:
- Fill gaps and smooth the output of a .c3d from `mc_reconstruction`.
- Batch convert .c3d data from `mc_reconstruction` to an `OpenSim` compatible format.
- Batch process converted outputs from `mc_reconstruction` outputs through `OpenSim's` IK solver.

Note:

`./isbs21_scripts` contains analysis scripts to produce results and figures for ISBS 2021 abstract.

`./paper2_scripts` contatins analysis scropts to produce results and figures for BioCV Paper 2.

## Installation

To install on Unbuntu 18.04 LTS:

1) Compile OpenSim from source using instruction [here](https://github.com/opensim-org/opensim-core#on-ubuntu-using-unix-makefiles). Make sure that you point CMake towards the python install that will use to create your venv in the next steps. Additional notes on some of the issues I encountered while compiling can be found [here](./opensim_install_notes.md)...good luck!

2) Once OpenSim is playing ball, clone the repository from [camera-mc-dev](https://github.com/camera-mc-dev):

```console
foo@bar:~$ git clone ...
```

```console
foo@bar:~$ cd mc_opensim
```

```console
foo@bar:~./mc_opensim$ python3.9 -m venv ./venv --system-site-packages
```

```console
foo@bar:~./mc_opensim$ source venv/bin/activate
```

```console
(venv) foo@bar:~./mc_opensim$ pip3.9 install -r requirements.txt
```

## Usage

**FillSmoothC3D.py** - Use to fill gaps and smooth a .c3d file.

- You can use this in one of two ways:
  1) Simply pass a list of `.c3d` files to the script on the command line, as well as the noise parameters for the Kalman filter.
  2) Set the `PATH` variable in the config.py file to the path of the _session_ directory.
     - the script will search beneath that dir for any .c3d files and try to smooth them.
     - noise parameters for the Kalman smoother will be taken from the config file.
     - If one or both of the noise parameters are set negative, then the script will ask PyKalman to estimate suitable parameters.
     - We use a constant acceleration filter.
     - increasing the transition noise or the reducing the observation noise allows the state to deviate from that assumption
     - reducing the transition noise or increasing the observation nose encourages the state to stick to that assumption
     
     
```console
(venv) foo@bar:~./mc_opensim$ python3 FillSmoothC3D.py False 0.01 15 file00.c3d file01.c3d ... fileNN.c3d
```

```console
(venv) foo@bar:~./mc_opensim$ python3 FillSmoothC3D.py True
```

**TrcGenerator.py** - Use to convert .c3d files to OpenSim .trc format.

- Update `config.py` by:
  - Setting `PATH` variable to the absolute path of the _session_ directory.
    - The script will walk through the filesystem looking for .c3d files and converting them.
  - Setting other trc settings as desired (details of each setting given in config file).
- Run:

```console
(venv) foo@bar:~./mc_opensim$ python3 TrcGenerator.py
```

**BatchIK.py** - Use to generate scaled osim model and run IK solver on motion files

- Ensure that .trc files have been generated.
- Update `config.py` by:
  - Setting `PATH` variable to the absolute path of the _session_ directory.
  - Setting other scaling and IK settings as desired (details of each setting given in config file).
  - For fine-grained control of IK settings see `.xml` files in `./configs/`.
- Run:

```console
(venv) foo@bar:~./mc_opensim$ python3 BatchIK.py
```

## Developer Notes

When running the IK solver, we currently assume the following:

- For markerbased data, we assume that the scaled model (.osim) is located in the same directory as the .trc files. e.g.

```console
session_dir
│
├──trial_01.trc
├──trial_02.trc
└──scaled_static.osim
```

- For markerless data, we assume that the scaled model (.osim) is located in the same parent directory as the motion trials e.g.

```console
session_dir
│
└──trial_01
|   |
|   └──trial.trc
└──trial_02
|   |
|   └──trial.trc
└──STATIC_01
    |
    └──scaled_static.osim
```
