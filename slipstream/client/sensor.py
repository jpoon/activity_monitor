from __future__ import division
from datetime import datetime
import os
import logging
import cairoplot

class Sensor:
    def __init__(self, dir, name):
        self.logging = logging.getLogger("sensor")

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

        self.calibrated = False

    def add(self, pkt):
        for item in pkt:
            attr, val = item.split('=')
            val = int(val.strip(','))
     
            try:
                getattr(self, attr).append(val)
            except:
                self.logging.error('Unknown attribute: %s' % attr)

        self.time.append(datetime.time(datetime.now()).strftime("%M:%S"))

    def setCalibration(self, adcCounts_per_g, zero_g_value):
        self.calibrated = True
        self.adcCounts_per_g = adcCounts_per_g
        self.zero_g_value = zero_g_value
       
    def getNumSamples(self):
        return len(self.time)

    def createGraphSensor(self):
        data = {}
        y_bounds = None

        if self.calibrated:
            for key in self.adcCounts_per_g.keys():
                dataset = []
                for datapoint in getattr(self,key):
                    try:
                        converted_value = (datapoint-self.zero_g_value[key])/self.adcCounts_per_g[key]
                        dataset.append(converted_value)
                    except ZeroDevisionError:
                        self.logging.error("Zero Divison Error: (%s-%s)/%s" % (datapoint, self.zero_g_value[key], self.adcCounts_per_g[key]))
                data[key] = dataset

            y_bounds = (-4, 4)
        else:
            data["acc_x"] = self.acc_x
            data["acc_y"] = self.acc_y
            data["acc_z"] = self.acc_z


        filename = self.dir + "/" + self.name
        cairoplot.dot_line_plot(name=filename,
                                data=data,
                                width=900,
                                height=900,
                                border=5,
                                axis=True,
                                grid=True,
                                series_legend=True,
                                x_labels=self.time,
                                x_title = "Time (minutes:seconds)",
                                y_bounds = y_bounds,
                                y_title = "")

        self.__convertToPng(filename)
        self.logging.debug("Updating %s graph" % self.name)

    def __convertToPng(self, filename):
        os.system("gimp -i -b '(svg-to-raster \"%s.svg\" \"%s.png\" 72 0 0)' -b '(gimp-quit 0)' &> /dev/null &" % (filename, filename))
