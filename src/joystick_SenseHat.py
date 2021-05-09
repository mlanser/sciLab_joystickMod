import time
from datetime import datetime
from copy import deepcopy

from evdev import InputDevice, list_devices, ecodes
from sense_hat import SenseHat

from .joystick_base import _JoystickBase

# =========================================================
#                      G L O B A L S
# =========================================================
_JOYSTICK_TYPE_: str = 'SenseHat'
_JOYSTICK_NAME_: str = 'Raspberry Pi Sense HAT Joystick'

_CENTER_X_ = 3          # Center X coord on 8x8 grid
_CENTER_Y_ = 3          # Center Y      - " -

_DEFAULT_SETTINGS_ = {
    'holdTime': 0.1,    # Min amount of time between position checks
    'restrict': True,   # If FALSE, then joystick action can increase/decrease X/Y coords indefinitely.
    'loop': True,       # If 'restrict' and 'loop' are TRUE, then X/Y coords loop around, else stop at min/max coords.
    'minX': 0,          # Min X coord
    'maxX': 7,          # Max  - " -
    'minY': 0,          # Min Y coord
    'maxY': 7,          # Max  - " -
}


def _no_action(*args):
    pass


_DEFAULT_ACTIONS_ = {
    'actionUp': _no_action,
    'actionDwn': _no_action,
    'actionLft': _no_action,
    'actionRht': _no_action,
    'actionAny': _no_action,
}


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Joystick(_JoystickBase):
    def __init__(self, initX=None, initY=None, actions=None, settings=None):
        _settings = _DEFAULT_SETTINGS_ if settings is None else {**_DEFAULT_SETTINGS_, **settings}

        _initX = _CENTER_X_ if initX is None else super()._normalize(
            initX,
            _settings['minX'],
            _settings['maxX'],
            _settings['restrict'],
            _settings['loop']
        )
        _initY = _CENTER_Y_ if initY is None else super()._normalize(
            initY,
            _settings['minY'],
            _settings['maxY'],
            _settings['restrict'],
            _settings['loop']
        )

        super().__init__(
            _initX,
            _initY,
            _DEFAULT_ACTIONS_ if actions is None else {**_DEFAULT_ACTIONS_, **actions},
            _settings,
            _JOYSTICK_TYPE_
        )
        self._joystick = SenseHat()

    def get_events(self):
        return self._joystick.stick.get_events()

    def found_joystick(self):
        found = False
        devices = [InputDevice(fn) for fn in list_devices()]
        for dev in devices:
            if dev.name == _JOYSTICK_NAME_:
                found = True
                break

        return found


