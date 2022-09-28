# OpenSim installation notes (on Ubuntu 18.04)

## Issues at run-time

To avoid problems with "Type 3 (and 7) not supported" when loading `.c3d` files, make sure that you are using OpenSim with a version `> 4.0`

## Issues during dependency build for OpenSim Core:

If openGL linking issues arises from simbody visualizer, it probably can't find ```libGL.so```
This can be suppressed by editing:

```shell
dependencies/CMakeLists.txt
```

and adding the following to the simbody CMAKE_ARGS:

```CMAKE
-DBUILD_VISUALIZER:BOOL=OFF
```

## Issues during opensim-core build:

- Ensure that cmake is set to compile ezc3d NOT BTK.

- If python wrapper does not link correctly (and it probably won't) fix as follows:

  - Ensure that python API has been built and installed:

    ```shell
    cd /opensim-core/lib/python3.6/site-packages
    sudo python3 setup.py install
    ```

    Ensure that opensim-core install/bin is added to .bashrc as Github issues suggest:

    ```shell
    echo 'export PATH=~/home/ln424/Documents/C++/opensim/opensim-core-source-install/bin:$PATH' >> ~/.bashrc
    ```

- But this isn't a complete solution. Also need to update ld.so.conf:

    edit ```/etc/ld.so.conf``` (might need sudo privileges for this) and add

    ```shell
    path/to/opensim-core-install/lib/
    ```

- Then it seems that during the install not all of the dependency libs are collected and placed in 
```./opensim-core-install/lib```
- Fix as follows:

  - symlink (or cp) all the .so files from ```/opensim-dependencies-install/adol-c/lib64``` and ```/opensim-dependencies-install/ipopt/lib```

    - Finally run

    ```shell
    sudo ldconfig
    ```

    to update the system's library database.

## ISSUES TO RESOLVE:

- Resolve OpenGL issue so that visualizer can be used.
- Resolve Java/Matlab test fails.
- Compile GUI - links to OpenGL issues
