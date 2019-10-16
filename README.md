# webapp

[![Documentation Status](https://readthedocs.org/projects/vve-webapp/badge/?version=latest)](https://vve-webapp.readthedocs.io/en/latest/?badge=latest)

Flask webapp for interacting and remotely controlling the MASCCOT robot via WiFi.


# How to Contribute
check out our [contributing guidelines](https://github.com/DVC-Viking-Robotics/about-us/blob/master/Contributing%20Guidelines.rst)

# How to add or change the documentation
check out our guide on [contributing documentation](https://github.com/DVC-Viking-Robotics/about-us/blob/master/Contributing%20Documentation.rst)

## Setup instructions
```bash
# Clone the repository and its submodules
git clone https://github.com/DVC-Viking-Robotics/webapp
cd webapp
git checkout master
git submodule update --init --recursive

# Prepare the virtual environment
pip install virtualenv
python -m venv env
```
```bash
# Activate the virtual environment
# FOR WINDOWS
env\\Scripts\\activate.bat

# FOR LINUX
source env/bin/activate

pip install -r requirements.txt
```

On the Raspberry Pi, you'll need to install the `picamera` module via `apt`:
```bash
sudo apt-get install python3-picamera
```

## Setting up the server
You'll need to generate the `secret.key` file in order to enable the database for user management and place it in the `secret/` folder. The secret file is for encrypting the database URI. Alternatively, you can go to `webapp/config.py` and set `LOCAL_DATABASE` to `True`, but you will also have to run `tools/init_test_db.py` in order to initialize the local database.

## Running the server
```bash
python -m webapp.app
```