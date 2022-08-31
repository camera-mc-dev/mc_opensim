# mc_opensim

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

**Tools for running [mc_reconstruction](https://github.com/camera-mc-dev) outputs through [OpenSim's](https://github.com/opensim-org/opensim-core) IK solver**

A set of scripts to:
- Convert .c3d data from `mc_reconstruction` to a `OpenSim` compatible format.
- Batch process .c3d outputs from `mc_reconstruction` outputs through `OpenSim's` IK solver.

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
foo@bar:~./mc_opensim$ python3.9 -m venv ./venv
```

```console
foo@bar:~./mc_opensim$ source venv/bin/activate
```

```console
(venv) foo@bar:~./mc_opensim$ pip3.9 install -r requirements.txt
```


## Usage

## Developer Notes
