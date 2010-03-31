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
from graph import *
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

if __name__ == '__main__':
    (host, port, dir) = ParseArguments()

    condition = Condition()

    sensors = {}
    sensors['left_arm'] = Sensor(dir, "left_arm")
    sensors['right_arm'] = Sensor(dir, "right_arm")
    sensors['left_leg'] = Sensor(dir, "left_leg")
    sensors['right_leg'] = Sensor(dir, "right_leg")

    graphUpdateStack = []

    t1 = Calibrate_Thread(sensors, host, port)
    t1.start()
    t1.join()
 
    t2 = Graph_Thread(sensors, host, port)
    t2.start()

    while True:
        import time
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            t2.stop()
            break

