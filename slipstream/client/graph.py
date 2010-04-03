from sensor import *
from util import *
from slipstream import *
from data_analysis import *
import logging
import os

class Graph_Thread(StoppableThread):
    graph_dir = "graphs"
    graph_frequency = 10

    def __init__(self, sensorList, host, port):
        Thread.__init__(self)
        super(Graph_Thread, self).__init__()
        self.setName("Graph Thread")
        self.logging = logging.getLogger("run")

        self.sensorList = sensorList
        self.host = host
        self.port = port
        self.data_analysis = Data_Analysis()

        os.system("mkdir %s &> /dev/null" % Graph_Thread.graph_dir)

    def run(self):
        self.logging.debug("Starting %s" % self.getName())

        testCase = raw_input("Graph: Name of Test Case:\n")
        filedir = Graph_Thread.graph_dir + "/" + testCase + "/"
        os.system("mkdir %s &> /dev/null" % filedir)

        cond = Condition()
        updateList = []

        slipstream_thread = SlipStream_Thread(self.host, self.port, self.sensorList)
        slipstream_thread.setCond(cond)
        slipstream_thread.setUpdateList(updateList)
        slipstream_thread.start()
        
        while True:
            if self.stopped():
                slipstream_thread.stop()
                self.logging.debug("%s has exited properly" % self.getName())
                return

            with cond:
                cond.wait()

                sensor_location = updateList.pop()
                numSamples = self.sensorList.getNumSamples(sensor_location)

                if (numSamples > 0):
                    if (numSamples % Graph_Thread.graph_frequency == 0):
                        filename = filedir + "/" + sensor_location
                        self.sensorList.getSensor(sensor_location).createGraphSensor(filename)
#                       self.__convertToPng(filename)

                    if (numSamples % 10 == 0):
                        print self.data_analysis.getAverage(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        print self.data_analysis.getStndDeviation(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)

    def __convertToPng(self, filename):
        os.system("gimp -i -b '(svg-to-raster \"%s.svg\" \"%s.png\" 72 0 0)' -b '(gimp-quit 0)' &> /dev/null &" % (filename, filename))

