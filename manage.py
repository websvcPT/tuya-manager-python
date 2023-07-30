import sys
import argparse
import tinytuya



# Example data
# 'b654a3f895r5y75a54fqug',
# '192.168.1.253',
# '_x$vRDcFmbTY^%hjk-=' > '_y\$pDXmBR^%bjj-='  # Need to escape special characters when in bash
#
# python manage.py --ip 192.168.1.253 --id b654a3f895r5y75a54fqug --key '_y\$pDXmBR^%bjj-=' status -d

def tuya_device(ip: str, id: str, key: str, version: float=3.4):
    """Connect to device

    Args:
        ip (str): Device local IP
        id (str): Device ID
        key (str): Device local Key
        version (float, optional): Tuya protocol version (3.1, 3.2, 3.3, 3.4 or 3.5). Defaults to 3.4.

    Returns:
        OutletDevice: Represents a Tuya based Smart Plug or Switch
    """
    return tinytuya.OutletDevice(
        id,
        ip,
        key,
        version=version
    )

def find(element: str, json: dict):
    """Filter JSON object key from given path

    Args:
        element str: path to key
        json dict: json object

    Returns:
        misc: key value
    """
    keys = element.split('.')
    rv = json
    for key in keys:
        rv = rv[key]
    return rv

def get_status(device, data_key='dps.1'):
    """_summary_

    Args:
        device OutletDevice: device object
        data_key (str, optional): Key to filter device status from output. Defaults to 'dps.1'.

    Returns:
        bool|json: boolean status or data in JSON format if filter empty
    """
    data = device.status()

    print('Device status (full): %r' % data) if DEBUG else None
    if data_key != '':
        status = bool(find(data_key, data))
        print('Device status: %r' % status) if DEBUG else None
        return status
    else:
        return data

def toggle(device, action):
    """Toggles relay state

    Args:
        device OutletDevice: device object
        action str: action to take on the device relay
    """
    if action == 'ON':
        res = device.turn_on()
        print(res) if DEBUG else None

    if action == 'OFF':
        res = device.turn_off()
        print(res) if DEBUG else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tuya Manager - Tuya smart socket control and status check',
        usage='%(prog)s [options] {action}'
    )
    parser.add_argument('-d', default=False, action='store_true', dest='debug',
        help='Enable debug messages'
    )
    parser.add_argument('-e', default=False, action='store_true', dest='extended',
        help='Enable extended output'
    )
    parser.add_argument('--ip', type=str, default=None,
        action='store',
        help='Device IP'
    )
    parser.add_argument('--id', type=str, default=None,
        action='store',
        help='Device ID'
    )
    parser.add_argument('--key', type=str, default=None,
        action='store',
        help='Device local Key'
    )
    parser.add_argument('--version', type=float, default=3.4,
        action='store',
        help='Tuya protocol version used (3.1, 3.2, 3.3, 3.4 or 3.5) default: 3.4'
    )
    parser.add_argument('--status-filter-key', '--sfk', type=str, default='dps.1',
        action='store',
        help='Key to filter device status out of socket output data'
    )
    parser.add_argument('action', type=str, default=3,
        action='store',
        help='Action to take into device'
    )
    args = parser.parse_args()
    DEBUG = args.debug
    EXTENDED = args.extended

    print("args: %s", args) if args.debug else None

    device = tuya_device(args.ip, args.id, args.key, args.version)
    print(device) if DEBUG else None

    if device:

        if args.action == 'status':
            print(get_status(device, args.status_filter_key))
        elif args.action == 'ON' or args.action == 'OFF':
            # Start by getting current status
            print('Device current status: %r' % get_status(device, args.status_filter_key)) if EXTENDED else None
            # Toggle relay
            toggle(device, args.action)
            # Get status after operation
            print(get_status(device, args.status_filter_key))
        else:
            print('Unknown action')
            sys.exit(1)
        sys.exit(0)
    else:
        print("Unable to connect to device")

sys.exit(1)
