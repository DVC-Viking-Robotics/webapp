# webapp
Flask webapp for interacting and remotely controlling the MASCCOT robot via WiFi.

## Setup instructions
```bash
# Clone the repository and its submodules
git clone https://github.com/DVC-Viking-Robotics/webapp
cd webapp
git checkout nondrive-R2D2
git submodule update --init --recursive

# Prepare the virtual environment
pip install virtualenv
python -m venv env
```
```bash
# Activate the virtual environment
# FOR WINDOWS
env\Scripts\activate.bat

# FOR LINUX
source env/bin/activate

pip3 install -r requirements.txt
```

On the Raspberry Pi, you'll need to install the `picamera` module via `apt`:
```bash
sudo apt-get install python3-picamera
```

## Running the server
```bash
python -m webapp.app [cmd args]
# cmd args currently not supported
```

