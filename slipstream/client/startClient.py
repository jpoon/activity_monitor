#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-c] [-d] [-a Server Address] [-p Server Port]

Options:
    -h, --help
        Prints this message and exits

    -c, --calibrate
        Recalibrates the sensors. If option is not set, we use the 
        previously saved hardware calibration data.

    -d, --debug=
        Logging levels. Possible options are 'debug', 'info', 
        'warning', 'error', 'critical'.

    -a, --addr=
        Address in which server is located (e.g. 127.0.0.1)

    -p, --port=
        Port in which server is located (e.g. 4000)
"""

from sensor import *
from calibration import *
from monitor import *
import logging

def ParseArguments():
    LEVELS = { 'debug':logging.DEBUG,
                'info':logging.INFO,
                'warning':logging.WARNING,
                'error':logging.ERROR,
                'critical':logging.CRITICAL }

    # default values
    host = "127.0.0.1"
    port = 4000
    calibrate = False
    level = logging.error

    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcpa:d:", ["help", "calibrate", "port=", "addr=", "debug="])
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__ 
                sys.exit()
            if o in ("-c", "--calibrate"):
                calibrate = True
            if o in ("-p", "--port"):
                portNum = a
            if o in ("-a", "--addr"):
                host = a
            if o in ("-d", "--debug"):
                level = LEVELS.get(a)
                
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    except IndexError, err:
        print __doc__ % argv[0]
        print "Error: Missing argument(s)"
        sys.exit(2)

    logging.basicConfig(level=level)
    return (host, port, calibrate)

if __name__ == '__main__':
    (host, port, calibrate) = ParseArguments()

    Watcher()

    sensorList = SensorList()
    sensorList.addSensor("left_arm")
    sensorList.addSensor("right_arm")
    sensorList.addSensor("left_leg")
    sensorList.addSensor("right_leg")

    t1 = Calibrate_Thread(sensorList, host, port, calibrate)
    t1.start()
    t1.join()

    t2 = Monitor_Thread(sensorList, host, port)
    t2.start()

