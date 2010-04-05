from sensor import *
from util import *
from slipstream import *
from activity import *
import statistics
import logging
import os
import time
 
class Monitor_Thread(StoppableThread):
    graph_dir = "graphs"
    graph_frequency = 5

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
        updateSet = slipstream_thread.getUpdate()
        slipstream_thread.start()

        graph_timer = Timer(Monitor_Thread.graph_frequency, self.update_graph, [filename, cond])
        graph_timer.start()
       
        while True:
            if self.stopped():
                slipstream_thread.stop()
                self.logging.debug("%s has exited properly" % self.getName())
                return

            with cond:
                cond.wait()

                for sensor_location in updateSet:
                    numSamples = self.sensorList.getNumSamples(sensor_location)

                    if (numSamples % 10) == 0:
                        # calculate avg and std deviation for every 10 packets
                        avg = statistics.getAverage(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        stdDeviation = statistics.getStndDeviation(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        self.activity.add(sensor_location, avg, stdDeviation)

                updateSet.clear()

            time.sleep(5)

    def update_graph(self, *args):
        filename = args[0]
        cond = args[1]

        while True:
            with cond:
                cond.wait()

                self.sensorList.createGraph(filename)

            time.sleep(Monitor_Thread.graph_frequency)
