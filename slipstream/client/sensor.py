import logging
from graph.line_graph import *

class Sensor:
    class Value:
        def __init__(self):
            self.battery = []
            self.temperature = []
            self.light = []
            self.microphone = []
            self.acc_x = []
            self.acc_y = []
            self.acc_z = []

        def add(self, pkt):
            for item in pkt:
                attr, val = item.split('=')
                val = int(val.strip(','))
                
                if attr == "bat":
                    self.battery.append(val)
                elif attr == "temp":
                    self.temperature.append(val)
                elif attr == "light":
                    self.light.append(val)
                elif attr == "mic":
                    self.microphone.append(val)
                elif attr == "acc_x":
                    self.acc_x.append(val)
                elif attr == "acc_y":
                    self.acc_y.append(val)
                elif attr == "acc_z":
                    self.acc_z.append(val)
                else:
                    logging.error('Unknown attribute: %s' % attr)

    def __init__(self):
        self.left_arm = Sensor.Value()
        self.right_arm = Sensor.Value()
        self.left_leg = Sensor.Value()
        self.right_leg = Sensor.Value()

    def add(self, nodeId, pkt):
        if nodeId == 16:
            self.left_arm.add(pkt)

        graph = LineGraph()
        if len(self.left_arm.acc_x) == 10:
            graph.create("leftarm", self.left_arm.acc_x)

    def graph(self):
        graph = Graph()
         
