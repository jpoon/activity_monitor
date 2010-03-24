import logging
import cairoplot
from datetime import datetime

class Sensor:
    graph_min = 100
    graph_max = 700

    class Value:
        def __init__(self):
            self.time = []
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

        def getNumSamples(self):
            return len(self.bat)

    def __init__(self):
        self.left_arm = Sensor.Value()
        self.right_arm = Sensor.Value()
        self.left_leg = Sensor.Value()
        self.right_leg = Sensor.Value()

    def add(self, nodeId, pkt):
        sensor_location = self.__nodeIdToSensorLocation(nodeId)

        try:
            getattr(self, sensor_location).parse(pkt)
            getattr(self, sensor_location).time.append(datetime.time(datetime.now()).strftime("%M:%S"))
        except:
            logging.error('Unknown sensor location: %s' % sensor_location)

    def __nodeIdToSensorLocation(self, nodeId):
        if nodeId == 16:
            return "left_arm"
        elif nodeId == 17:
            return "right_arm"
        elif nodeId == 18:
            return "left_leg"
        elif nodeId == 19:
            return "right_leg"
        else:
            logging.error('Illegal Node ID of %d' % nodeId)

    def getNumSamples(self, sensor):
        return getattr(self, sensor).getNumSamples()

    def createGraphSensor(self, sensor):
        data = {}

        acc_x = getattr(self, sensor).acc_x
        acc_y = getattr(self, sensor).acc_y
        acc_z = getattr(self, sensor).acc_z

        data['acc_x'] = acc_x
        data['acc_y'] = acc_y
        data['acc_z'] = acc_z

        cairoplot.dot_line_plot(name=sensor,
                                data=data,
                                width=900,
                                height=900,
                                border=5,
                                axis=True,
                                grid=True,
                                series_legend=True,
                                x_labels=getattr(self, sensor).time,
                                y_bounds=(Sensor.graph_min, Sensor.graph_max),
                                x_title = "Time (minutes:seconds)",
                                y_title = "")

        logging.debug("Updating for %s" % sensor)

