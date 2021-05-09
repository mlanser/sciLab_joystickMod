import sys
import time
from evdev import InputDevice, list_devices, ecodes

import pprint
from faker import Faker
import argparse

# =========================================================
#                       G L O B A L S
# =========================================================
# Initiate 'Faker' and 'PrettyPrinter' :-)
pp = pprint.PrettyPrinter(indent=4)
faker = Faker()

_JOYSTICK_ATTRIBS_ = {
    'sensehat': {
        'holdTime': 0.1,    # Min amount of time between position checks
        'restrict': True,   # If FALSE, then joystick action can increase/decrease X/Y coords indefinitely.
        'loop': True,       # If 'restrict' and 'loop' are TRUE, then X/Y coords loop around, else stop at min/max coords.
        'minX': 0,          # Min X coord
        'maxX': 7,          # Max  - " -
        'minY': 0,          # Min Y coord
        'maxY': 7,          # Max  - " -
    }
}


# =========================================================
#                      H E L P E R S
# =========================================================
def show_up(dspl=None):
    if dspl is None:
        pass
    dspl.show_letter('U')


def show_down(dspl=None):
    if dspl is None:
        pass
    dspl.show_letter('D')


def show_left(dspl=None):
    if dspl is None:
        pass
    dspl.show_letter('L')


def show_right(dspl=None):
    if dspl is None:
        pass
    dspl.show_letter('R')


def pprint_stuff(something):
    pp.pprint(something)


def list_device_names():
    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
        pp.pprint(dev.name)


# =========================================================
#                  C L I   P A R S E R
# =========================================================
def shell():
    parser = argparse.ArgumentParser(
        description="React to joystick moves via 'joystickMod' module",
        epilog="NOTE: Only call a module if the corresponding hardware/driver is installed"
    )
    parser.add_argument(
        '--joystick',
        action='store',
        type=str,
        required=True,
        help="Joystick module to use"
    )

    args = parser.parse_args()
    joystick = None

    if args.joystick not in _JOYSTICK_ATTRIBS_:
        print("ERROR: '{}' is not a valid sensor module!".format(args.joystick))
        exit(1)

    if args.joystick == 'sensehat':
        from sense_hat import SenseHat
        display = SenseHat()    # Need this for testing only ;-)
        display.clear()

        _JOYSTICK_ACTIONS_ = {
            'up':  [
                {'fnc': show_up, 'arg': display},
                {'fnc': pprint_stuff, 'arg': [1, 2, 3]}
            ],
            'dwn': [
                {'fnc': show_down, 'arg': display}
            ],
            'lft': [
                {'fnc': show_left, 'arg': display}
            ],
            'rht': [
                {'fnc': show_right, 'arg': display}
            ],
        }

        from .joystick_SenseHat import Joystick
        joystick = Joystick(
            3, 3,
            _JOYSTICK_ACTIONS_,
            _JOYSTICK_ATTRIBS_[args.joystick]
        )

    # elif args.joystick == 'braincraft':
    #     from .joystick_BrainCraft import Joystick
    #     joystick = Joystick(_JOYSTICK_ATTRIBS_[args.joystick])

    curX, curY = joystick.get_position()
    pp.pprint((curX, curY))

    print('SenseHat exists: {}'.format(joystick.found_joystick()))

    list_device_names()


try:
    shell()

except KeyboardInterrupt:
    print('\nCancelling...')

except Exception as e:
    print('ERROR: {}'.format(e))
