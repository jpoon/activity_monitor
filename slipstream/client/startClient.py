#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-a Server Address] [-p Server Port]
Options:
    -h  Prints this message and exits
    -a  Address in which server is located (e.g. 127.0.0.1)
    -p  Port in which server is located (e.g. 4000)
"""

from calibrate import *
from slipstream import *
from sensor import *
from graph import *
from threading import *
import logging

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

if __name__ == '__main__':
    (host, port) = ParseArguments()

    Watcher()

    sensors = {}
    sensors['left_arm'] = Sensor("left_arm")
    sensors['right_arm'] = Sensor("right_arm")
    sensors['left_leg'] = Sensor("left_leg")
    sensors['right_leg'] = Sensor("right_leg")

    t1 = Calibrate_Thread(sensors, host, port)
    t1.start()
    t1.join()

    t2 = Graph_Thread(sensors, host, port)
    t2.start()

