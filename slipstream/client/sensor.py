import logging
import cairoplot
from datetime import datetime

class Sensor:
    graph_min = 100
    graph_max = 700

    def __init__(self, dir, name):
        self.dir = dir
        self.name = name

        self.time = []
        self.bat = []
        self.temp = []
        self.light = []
        self.mic = []
        self.acc_x = []
        self.acc_y = []
        self.acc_z = []

    def add(self, pkt):
        try:
            for item in pkt:
                attr, val = item.split('=')
                val = int(val.strip(','))
         
                try:
                    getattr(self, attr).append(val)
                except:
                    logging.error('Unknown attribute: %s' % attr)

            self.time.append(datetime.time(datetime.now()).strftime("%M:%S"))
        except:
            logging.error('Unknown sensor location: %s' % sensor_location)

    def getNumSamples(self):
        return len(self.time)

    def createGraphSensor(self):
        data = {}
        data['acc_x'] = self.acc_x
        data['acc_y'] = self.acc_y
        data['acc_z'] = self.acc_z

        cairoplot.dot_line_plot(name=self.dir + "/" + self.name,
                                data=data,
                                width=900,
                                height=900,
                                border=5,
                                axis=True,
                                grid=True,
                                series_legend=True,
                                x_labels=self.time,
                                y_bounds=(Sensor.graph_min, Sensor.graph_max),
                                x_title = "Time (minutes:seconds)",
                                y_title = "")

        logging.debug("Updating %s graph" % self.name)

