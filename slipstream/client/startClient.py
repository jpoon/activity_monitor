#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-c] [-a Server Address] [-p Server Port]
Options:
    -h  Prints this message and exits
    -c  Load calibration data
    -a  Address in which server is located (e.g. 127.0.0.1)
    -p  Port in which server is located (e.g. 4000)
"""

from sensor import *
from calibrate import *
from monitor import *
import logging

def ParseArguments():
    logging.basicConfig(level=logging.DEBUG)

    host = "127.0.0.1"
    port = 4000
    loadCalibrationData = None

    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcpa:", ["help", "cal", "port=", "addr="])
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__ 
                sys.exit()
            if o in ("-c", "--cal"):
                loadCalibrationData = True
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

    return (host, port, loadCalibrationData)

if __name__ == '__main__':
    (host, port, loadCalibrationData) = ParseArguments()

    Watcher()

    sensorList = SensorList()
    sensorList.addSensor("left_arm")
    sensorList.addSensor("right_arm")
    sensorList.addSensor("left_leg")
    sensorList.addSensor("right_leg")

    t1 = Calibrate_Thread(sensorList, host, port, loadCalibrationData)
    t1.start()
    t1.join()

    t2 = Monitor_Thread(sensorList, host, port)
    t2.start()

