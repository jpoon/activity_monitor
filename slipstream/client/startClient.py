#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-a Server Address] [-p Server Port]
Options:
    -h  Prints this message and exits
    -a  Address in which server is located (e.g. 127.0.0.1)
    -p  Port in which server is located (e.g. 4000)
"""

from slipstream import *
from sensor import *
import logging
from threading import *

killThread = False

def ParseArguments():
    logging.basicConfig(level=logging.DEBUG)

    host = "127.0.0.1"
    port = 4000

    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpa:", ["help", "port=", "addr="])
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__ 
                sys.exit()
            if o in ("-p", "--port"):
                portNum = a
            if o in ("-a", "--addr"):
                host = a
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    except IndexError, err:
        print __doc__ % argv[0]
        print "Error: Missing argument(s)"
        sys.exit(2)

    return (host, port)

class StoppableThread (Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class SlipStream_Thread(StoppableThread):
    def __init__ (self, cond, sensor, host, port, name=None):
        Thread.__init__(self)
        super(SlipStream_Thread, self).__init__()
        self.cond = cond
        self.sensor = sensor
        self.host = host
        self.port = port
        self.name = "SlipStream Thread"

    def run(self):
        client = SlipStream(self.host, self.port)

        while True:
            if self.stopped():
                with self.cond:
                    self.cond.notify()
                logging.debug("%s has exited properly" % self.name)
                break

            (sensor_location, msg) = client.receive()

            with self.cond:
                self.sensor.add(sensor_location, msg)
                self.cond.notify()

class Graph_Thread(StoppableThread):
    def __init__(self, cond, sensor, name=None):
        Thread.__init__(self)
        super(Graph_Thread, self).__init__()
        self.cond = cond
        self.sensor = sensor
        self.name = "Graph Thread"

    def run(self):
        while True:
            if self.stopped():
                logging.debug("%s has exited properly" % self.name)
                break

            with self.cond:
                self.cond.wait()

                for sensor_location in sensor.__dict__:
                    try:
                        numSamples = getattr(self.sensor, sensor_location).getNumSamples()

                        if (numSamples > 0 and numSamples % 5 == 0):
                            self.sensor.createGraphSensor(sensor_location)
                    except:
                        pass


if __name__ == '__main__':
    (host, port) = ParseArguments()

    sensor = Sensor()
    condition = Condition()

    t1 = SlipStream_Thread(condition, sensor, host, port)
    t2 = Graph_Thread(condition, sensor)

    t1.start()
    t2.start()

    while True:
        import time
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            t1.stop()
            t2.stop()
            break

