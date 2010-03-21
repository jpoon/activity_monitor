import logging

class Sensor:
    def __init__(self):
        pass

    def set(self, attr, val):
        val = int(val)
        if attr == "bat":
            self.battery = val
        elif attr == "temp":
            self.temperature = val
        elif attr == "light":
            self.light = val
        elif attr == "mic":
            self.microphone = val
        elif attr == "acc_x":
            self.acc_x = val
        elif attr == "acc_y":
            self.acc_y = val
        elif attr == "acc_z":
            self.acc_z = val
        else:
            logging.error('Unknown attribute: %s' % attr)

