# FrED factory FJ24

Collaborative Robotics Challenge with MIT for the Manufacturing Systems Automation class.

## Setup

For easier multiplatform environment setup, a python `venv` will be created. In Windows, `Python 11` is being used. 

Open `PowerShell`, then navigate to your preffered location and execute:

**Cloning:**
```bash
git clone https://github.com/afr2903/FrED-factory.git
cd FrED-factory
git submodule init
git submodule update --recursive
```

**Virtual environment:**
```bash
python -m venv fred-env
.\fred-env\Scripts\Activate.ps1
pip install -r requirements.txt
```