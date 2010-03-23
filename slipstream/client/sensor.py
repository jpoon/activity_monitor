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

        def add(self, pkt):
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

    def __init__(self):
        self.left_arm = Sensor.Value()
        self.right_arm = Sensor.Value()
        self.left_leg = Sensor.Value()
        self.right_leg = Sensor.Value()

    def add(self, nodeId, pkt):
        if nodeId == 16:
            self.left_arm.add(pkt)

        graph = LineGraph()
        if (len(self.left_arm.acc_x) % 10) == 0:
            bounds = self.left_arm.getBounds("acc_x")
            graph.create("leftarm", self.left_arm.acc_x, bounds)
            print self.left_arm.acc_x

    def graph(self):
        graph = Graph()
         
