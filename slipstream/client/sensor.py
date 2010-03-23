import logging
from graph.line_graph import *

class Sensor:
    class Value:
        def __init__(self):
            self.bat = []
            self.temp = []
            self.light = []
            self.mic = []
            self.acc_x = []
            self.acc_y = []
            self.acc_z = []

        def parse(self, pkt):
            for item in pkt:
                attr, val = item.split('=')
                val = int(val.strip(','))
         
                try:
                    getattr(self, attr).append(val)
                except:
                    logging.error('Unknown attribute: %s' % attr)

        def getBounds(self, attr):
            list = getattr(self, attr)
            return (min(list), max(list))

        def getNumSamples(self):
            return len(self.bat)

    def __init__(self):
        self.left_arm = Sensor.Value()
        self.right_arm = Sensor.Value()
        self.left_leg = Sensor.Value()
        self.right_leg = Sensor.Value()

    def add(self, sensor_location, pkt):
        try:
            getattr(self, sensor_location).parse(pkt)
        except:
            logging.error('Unknown sensor location: %s' % sensor_location)

    def getNumSamples(self):
        return self.left_arm.getNumSamples()

    def graph(self):
        graph = LineGraph()
        bounds = self.left_arm.getBounds("acc_x")
        graph.create("leftarm", self.left_arm.acc_x)
        logging.debug("Updating graph")

