from sensor import *
from util import *
from slipstream import *
import logging

class Graph_Thread(StoppableThread):
    graph_dir = "graphs"

    def __init__(self, sensors, host, port):
        Thread.__init__(self)
        super(Graph_Thread, self).__init__()

        self.sensors = sensors
        self.host = host
        self.port = port

        self.setName("Graph Thread")

        import os
        os.system("mkdir %s &> /dev/null" % Graph_Thread.graph_dir)

    def run(self):
        logging.debug("Starting %s" % self.name)

        cond = Condition()
        updateList = []

        slipstream_thread = SlipStream_Thread(self.host, self.port, self.sensors)
        slipstream_thread.setCond(cond)
        slipstream_thread.setUpdateList(updateList)
        slipstream_thread.start()
        
        while True:
            if self.stopped():
                slipstream_thread.stop()
                logging.debug("%s has exited properly" % self.getName())
                return

            with cond:
                cond.wait()

                sensor_location = updateList.pop()
                numSamples = self.sensors[sensor_location].getNumSamples()

                if (numSamples > 0 and numSamples % 5 == 0):
                    filename = Graph_Thread.graph_dir + "/" + sensor_location
                    self.sensors[sensor_location].createGraphSensor(filename)

