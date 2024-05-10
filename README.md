# FrED factory FJ24

Collaborative Robotics Challenge with MIT for the Manufacturing Systems Automation class.

## Setup

For easier multiplatform environment setup, a python `venv` will be created. In Windows, `Python 11` is being used. 

### Cloning the repo

**Git** is required to collaborate and have the latest version of the code, install it from [here](https://git-scm.com/download/win). When the installer is opened, click `Next` for the default installation until it is finished.

Then, open `PowerShell`, navigate to your preffered location with `cd` commands, and execute:

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
python -m venv fred-env
.\fred-env\Scripts\Activate.ps1
pip install -r requirements.txt
```