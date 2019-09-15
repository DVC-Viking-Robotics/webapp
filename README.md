# webapp
Flask webapp for interacting and remotely controlling the MASCCOT robot via WiFi.

[OLD] Required BEFORE Install:
* gevent==1.4.0
* gevent-websocket==0.10.1

## Setup instructions
```bash
# Clone the repository and its submodules
git clone --recursive https://github.com/DVC-Viking-Robotics/webapp
cd webapp

# Prepare the virtual environment
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

On the Raspberry Pi, you'll need to install the `picamera` module via `apt`:
```bash
sudo apt-get install python3-picamera
```

## Running the server
```bash
python3 -m webapp.app [cmd args]
```