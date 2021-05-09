from abc import ABC, abstractmethod


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class _JoystickBase(ABC):
    def __init__(self, initX, initY, actions, settings, joystickType):
        self._curX = initX
        self._curY = initY
        self._actions = actions
        self._settings = settings
        self._type = joystickType

    def __str__(self):
        return '{}'.format(self._type)

    def __repr__(self):
        return "TYPE: '{}'".format(self._type)

    @staticmethod
    def _parse_attribs(attribs, key, default=None):
        if attribs is None:
            return default

        return attribs.get(key, default)

    @staticmethod
    def _normalize(inVal, minVal, maxVal, restrict=False, loop=False):
        if restrict:
            if loop:
                return (int(inVal) % (int(maxVal) - int(minVal) + 1)) + int(minVal)

            return min(int(maxVal), max(int(minVal), int(inVal)))

        return int(inVal)

    @property
    def type(self):
        return self._type

    @property
    def curX(self):
        return self._curX

    @property
    def curY(self):
        return self._curY

    def reset(self, newX=0, newY=0, settings=None):
        if settings is not None:
            self._settings = {**self._settings, **settings}     # Overwrite existing settings with new values

        self._curX = newX
        self._curY = newY

    def get_position(self):
        return self._curX, self._curY

    def set_position(self, newX, newY, action=None):
        self._curX = newX
        self._curY = newY

        if action is not None:
            action()

    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def found_joystick(self):
        pass
