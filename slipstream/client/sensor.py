from __future__ import division
from datetime import datetime
import os
import logging
import cairoplot

class SensorList:
    max_graph_data = 100

    class Adxl:
        def __init__(self, name):
            self.time = []
            self.x = []
            self.y = []
            self.z = []

            self.logging = logging.getLogger("sensor." + name)
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

        def get(self, begin, end):
            x = self.x[begin:end]
            y = self.y[begin:end]
            z = self.z[begin:end]
            return (x, y, z) 

        def setCalibration(self, adcCounts_per_g, zero_g_value):
            self.calibrated = True
            self.adcCounts_per_g = adcCounts_per_g
            self.zero_g_value = zero_g_value

            # clear data
            del self.time[:]
            del self.x[:]
            del self.y[:]
            del self.z[:]
           
        def getNumSamples(self):
            return len(self.time)

        def createGraph(self, filename):
            if self.getNumSamples() < 5:
                self.logging.debug('Not enough samples to create %s graph' % filename)
                return
            else:
                self.logging.debug('Updating %s graph' % filename)

            if self.calibrated:
                y_bounds = (-4, 4)
                y_title = "Acceleration (g)"
            else:
                y_bounds = None
                y_title = "ADC Counts"

            data = {}
            for axis in ["x", "y", "z"]:
                index = min(len(getattr(self, axis)), SensorList.max_graph_data)
                data[axis] = getattr(self, axis)[-index:]

            cairoplot.dot_line_plot(name=filename,
                                    data=data,
                                    width=900,
                                    height=900,
                                    border=3,
                                    axis=True,
                                    grid=True,
                                    series_legend=True,
                                    x_labels=self.time,
                                    x_title = "Time (minutes:seconds)",
                                    y_bounds = y_bounds,
                                    y_title = y_title) 

    def __init__(self):
        self._sensorDict = {}
        self.logging = logging.getLogger("sensorlist")

    def addSensor(self, name):
        self._sensorDict[name] = self.Adxl(name)

    def addSample(self, name, pkt):
        for item in pkt:
            attr, val = item.split('=')

            if val.isdigit():
                val = int(val)
                self._sensorDict[name].add(attr, val)
            else:
                self.logging.error('Received value of %s could not be parsed into integer: %s' % (val, item))

        self._sensorDict[name].addDone()

    def getSensorData(self, name, begin, end):
        return self._sensorDict[name].get(begin, end)

    def getSensorKeys(self):
        return self._sensorDict.keys()

    def getNumSamples(self, name):
        return self._sensorDict[name].getNumSamples()

    def calibrate(self, data):
        for k in self.getSensorKeys():
            (adcCount, zero_g) = data[k]
            self._sensorDict[k].setCalibration(adcCount, zero_g) 
            self.logging.info('%s', k)
            self.logging.info('adcCount=%s', adcCount)
            self.logging.info('zero_g=%s', zero_g)

    def createGraph(self, filepath, convertToPng=False):
        for k in self.getSensorKeys():
            filename = filepath + "/" + k
            self._sensorDict[k].createGraph(filename)

            if convertToPng:
                import os
                os.system("gimp -i -b '(svg-to-raster \"%s.svg\" \"%s.png\" 72 0 0)' -b '(gimp-quit 0)' &> /dev/null &" % (filename, filename))

