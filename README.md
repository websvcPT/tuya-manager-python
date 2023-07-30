# Tuya Manager - Tuya smart socket control and status check

This script allows checking the status and control relay state of a Tuya smart socket

It was developed to control a smart socket via klipper, but since it's a standalone script it's use it's not limited to it.

## Requirements

- Tuya smart socket
- Python

## Info for setup

This relies on TinyTuya python module, that allows to interface with Tuya WiFi smart devices. https://github.com/jasonacox/tinytuya

In order to identify the required information to communicate with the smart socket, follow the wizard provided by TinyTuya: https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys

Here's another guide that also works (they instruct the same): https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md

## Deployment

Clone the repo or download to desired location

### Virtual environment

```bash
virtualenv --python=python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### System wide

```bash
pip install -r requirements.txt
```

## Execution

```bash
# virtualenvironment

/path/to/.venv/bin/python3 /path/to/manage.py --ip {IP-ADDRESS} --id {DEVICE-ID} --key '{DEVICE-LOCAL_KEY}' {ACTION}

# with requirements installed system wide

python3 /path/to/manage.py --ip {IP-ADDRESS} --id {DEVICE-ID} --key '{DEVICE-LOCAL_KEY}' {ACTION}

```

### Usage options

```bash
$ python3 manage.py  --help
usage: manage.py [options] {action}

Tuya Manager - Tuya smart socket control and status check

positional arguments:
  action                Action to take into device

optional arguments:
  -h, --help            show this help message and exit
  -d                    Enable debug messages
  -e                    Enable extended output
  --ip IP               Device IP
  --id ID               Device ID
  --key KEY             Device local Key
  --version VERSION     Tuya protocol version used (3.1, 3.2, 3.3, 3.4 or 3.5) default: 3.4
  --status-filter-key STATUS_FILTER_KEY, --sfk STATUS_FILTER_KEY
                        Key to filter device status out of socket output data
```
