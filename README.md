# FrED factory FJ24

Collaborative Robotics Challenge with MIT for the Manufacturing Systems Automation class.

## Setup

For easier multiplatform environment setup, a python `venv` will be created. In Windows, `Python 11` is being used. 

### Cloning the repo

**Git** is required to collaborate and have the latest version of the code, install it from [here](https://git-scm.com/download/win). When the installer is opened, click `Next` for the default installation until it is finished.

Then, open `CMD`, navigate to your preffered location with `cd` commands, and execute:

```bash
git clone https://github.com/afr2903/FrED-factory.git
cd FrED-factory
```

Additionally, to pull the `xArm SDK` submodule to see the examples
```bash
git submodule init
git submodule update --recursive
```

### Virtual environment:

A virtual environment allows to work in an isolated Python environment:
```bash
python -m venv fred-env # Create a virtual enviroment called "fred-env"
.\fred-env\Scripts\activate.bat # If in CMD
pip install -r requirements.txt
```

### Teleop test
To test the environment was properly set, you can try the `gripper-teleop.py` script. Make sure the gripper is connected to the xArm and the router is connected and the WiFi led is on.

Connect to the network `RoboMaze` with password `RoBorregos2024`.

And execute the script:
```bash
python gripper-teleop.py
```