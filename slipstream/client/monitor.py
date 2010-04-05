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

    activity_frequency = 5

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
        slipstream_thread.start()

        graph_timer = Timer(Monitor_Thread.graph_frequency, self.update_graph, [filename, cond])
        graph_timer.start()

        activity_timer = Timer(Monitor_Thread.activity_frequency, self.check_activity, [cond])
        activity_timer.start()
 
        while True:
            if self.stopped():
                slipstream_thread.stop()
                self.logging.debug("%s has exited properly" % self.getName())
                return

    def update_graph(self, *args):
        filename = args[0]
        cond = args[1]

        while True:
            with cond:
                cond.wait()

                self.sensorList.createGraph(filename)

            time.sleep(Monitor_Thread.graph_frequency)

    def check_activity(self, *args):
        cond = args[0]

        while True:
            with cond:
                cond.wait()

                for sensor_location in self.sensorList.getSensorKeys():
                    numSamples = self.sensorList.getNumSamples(sensor_location)
                    if numSamples > 10:
                        avg = statistics.getAverage(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        stdDeviation = statistics.getStndDeviation(self.sensorList.getSensor(sensor_location), numSamples-10, numSamples)
                        self.activity.add(sensor_location, avg, stdDeviation)


                self.activity.doAllTests()

            time.sleep(Monitor_Thread.activity_frequency)
