from sensor import *
from util import *
from slipstream import *
from data_analysis import *
from activity import *
import logging
import os

class Monitor_Thread(StoppableThread):
    graph_dir = "graphs"
    graph_frequency = 10

    def __init__(self, sensorList, host, port):
        Thread.__init__(self)
        super(Monitor_Thread, self).__init__()
        self.setName("Monitor Thread")
        self.logging = logging.getLogger("run")

        self.sensorList = sensorList
        self.activity = Activity(self.sensorList.getSensorKeys())
        self.host = host
        self.port = port

        os.system("mkdir %s &> /dev/null" % Monitor_Thread.graph_dir)

    def run(self):
        self.logging.debug("Starting %s" % self.getName())

        testCase = raw_input("Name of Test Case: ")
        filename = Monitor_Thread.graph_dir + "/" + testCase
        os.system("mkdir %s &> /dev/null" % filename)

        cond = Condition()
        slipstream_thread = SlipStream_Thread(self.host, self.port, self.sensorList)
        slipstream_thread.setCond(cond)
        updateList = slipstream_thread.getUpdateList()
        slipstream_thread.start()
        
        while True:
            if self.stopped():
                slipstream_thread.stop()
                self.logging.debug("%s has exited properly" % self.getName())
                return

            with cond:
                cond.wait()

                if self.sensorList.isReady():
                    sensor_location = updateList.pop()
                    numSamples = self.sensorList.getNumSamples(sensor_location)

                    if (numSamples % Monitor_Thread.graph_frequency == 0):
                        self.sensorList.createGraph(filename)

                    if (numSamples % 5 == 0):
                        avg = Data_Analysis.getAverage(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        stdDeviation = Data_Analysis.getStndDeviation(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)

                        self.activity.add(sensor_location, avg, stdDeviation)
