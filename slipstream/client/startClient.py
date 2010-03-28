#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-a Server Address] [-p Server Port]
Options:
    -h  Prints this message and exits
    -a  Address in which server is located (e.g. 127.0.0.1)
    -p  Port in which server is located (e.g. 4000)
    -d  Sensor graphs will be placed in "graphs/". Use this option
        to denote a subdirectory in which to place the graphs.
        Eg. -d running will place the graphs under graphs/running
"""

from calibrate import *
from slipstream import *
from sensor import *
from util import *
import os
import logging

killThread = False

def ParseArguments():
    logging.basicConfig(level=logging.DEBUG)

    host = "127.0.0.1"
    port = 4000
    prefix_graph_dir = "graphs"
    graph_dir = ""

    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpad:", ["help", "port=", "addr=", "dir="])
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__ 
                sys.exit()
            if o in ("-p", "--port"):
                portNum = a
            if o in ("-a", "--addr"):
                host = a
            if o in ("-d", "--dir"):
                graph_dir = a
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    except IndexError, err:
        print __doc__ % argv[0]
        print "Error: Missing argument(s)"
        sys.exit(2)

    graph_dir = prefix_graph_dir + "/" + graph_dir 
    os.system("mkdir %s &> /dev/null" % graph_dir)

    return (host, port, graph_dir)

class SlipStream_Thread(StoppableThread):
    def __init__ (self, cond, sensors, updateStack, host, port):
        Thread.__init__(self)
        super(SlipStream_Thread, self).__init__()

        self.cond = cond
        self.sensors = sensors
        self.update = updateStack
        self.host = host
        self.port = port
        self.name = "SlipStream Thread"

    def run(self):
        logging.debug("Starting %s" % self.name)
        client = SlipStream(self.host, self.port)
        while True:
            if self.stopped():
                with self.cond:
                    self.cond.notifyAll()
                logging.debug("%s has exited properly" % self.name)
                break

            (sensor, msg) = client.receive()
            
            if msg is not None:
                with self.cond:
                    self.sensors[sensor].add(msg)
                    self.update.append(sensor)
                    self.cond.notifyAll()

class Graph_Thread(StoppableThread):
    def __init__(self, cond, sensors, updateStack):
        Thread.__init__(self)
        super(Graph_Thread, self).__init__()

        self.cond = cond
        self.sensors = sensors
        self.update = updateStack
        self.name = "Graph Thread"

    def run(self):
        logging.debug("Starting %s" % self.name)
        while True:
            if self.stopped():
                logging.debug("%s has exited properly" % self.name)
                break

            with self.cond:
                self.cond.wait()
                try:
                    sensor_location = self.update.pop()
                    numSamples = self.sensors[sensor_location].getNumSamples()

                    if (numSamples > 0 and numSamples % 5 == 0):
                        self.sensors[sensor_location].createGraphSensor()

                except:
                    pass


if __name__ == '__main__':
    (host, port, dir) = ParseArguments()

    condition = Condition()

    sensors = {}
    sensors['left_arm'] = Sensor(dir, "left_arm")
    sensors['right_arm'] = Sensor(dir, "right_arm")
    sensors['left_leg'] = Sensor(dir, "left_leg")
    sensors['right_leg'] = Sensor(dir, "right_leg")

    graphUpdateStack = []

    t1 = SlipStream_Thread(condition, sensors, graphUpdateStack, host, port)

    t2 = Calibrate_Thread(condition, sensors)
    t3 = Graph_Thread(condition, sensors, graphUpdateStack)

    t1.start()

    t2.start()
    t2.join()

    t3.start()

    while True:
        import time
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            t1.stop()
            t2.stop()
            t3.stop()
            break

