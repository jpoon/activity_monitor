from __future__ import division
from datetime import datetime
import os
import logging
import cairoplot

class SensorList:
    class Sensor:
        def __init__(self, name):
            self.time = []
            self.bat = []
            self.temp = []
            self.light = []
            self.mic = []
            self.acc_x = []
            self.acc_y = []
            self.acc_z = []

            self.logging = logging.getLogger(name)

            self.calibrated = False

        def add(self, attr, val):
            if self.calibrated:
                if attr in self.adcCounts_per_g.keys():
                    try:
                        val = (val-self.zero_g_value[attr])/self.adcCounts_per_g[attr]
                    except:
                        self.logging.error("Math Error: (%s-%s)/%s" % (val, self.zero_g_value[attr], self.adcCounts_per_g[attr]))

            try:
                getattr(self, attr).append(val)
            except:
                self.logging.error('Unknown attribute: %s' % attr)

        def addDone(self):
            self.time.append(datetime.time(datetime.now()).strftime("%M:%S"))

        def setCalibration(self, adcCounts_per_g, zero_g_value):
            self.calibrated = True
            self.adcCounts_per_g = adcCounts_per_g
            self.zero_g_value = zero_g_value

            self.clearData()

        def clearData(self):
            del self.time[:]
            del self.bat[:]
            del self.temp[:]
            del self.light[:]
            del self.mic[:]
            del self.acc_x[:]
            del self.acc_y[:]
            del self.acc_z[:]
           
        def getNumSamples(self):
            return len(self.time)

        def createGraph(self, filename):
            if self.calibrated:
                y_bounds = (-4, 4)
            else:
                y_bounds = None

            data = {}
            data["acc_x"] = self.acc_x
            data["acc_y"] = self.acc_y
            data["acc_z"] = self.acc_z

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

    def __init__(self):
        self._sensorDict = {}
        self.logging = logging.getLogger("activity")

    def addSensor(self, name):
        self._sensorDict[name] = self.Sensor(name)

    def addSample(self, name, pkt):
        for item in pkt:
            attr, val = item.split('=')

            if val.isdigit():
                val = int(val)
                self._sensorDict[name].add(attr, val)
            else:
                self.logging.error('Received value of %s could not be parsed into integer: %s' % (val, item))

        self._sensorDict[name].addDone()

    def getSensor(self, name):
        return self._sensorDict[name]

    def getSensorKeys(self):
        return self._sensorDict.keys()

    def getNumSamples(self, name):
        return self._sensorDict[name].getNumSamples()

    def calibrate(self, data):
        for k in self.getSensorKeys():
            (adcCount, zero_g) = data[k]
            self._sensorDict[k].setCalibration(adcCount, zero_g) 

    def createGraph(self, name, filedir, convertToPng=False):
        filename = filedir + "/" + name
        self._sensorDict[name].createGraph(filename)

        if convertToPng:
            import os
            os.system("gimp -i -b '(svg-to-raster \"%s.svg\" \"%s.png\" 72 0 0)' -b '(gimp-quit 0)' &> /dev/null &" % (filename, filename))

