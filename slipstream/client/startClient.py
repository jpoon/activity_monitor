#!/usr/bin/python
"""
Usage: 
    ./startClient [-h] [-a Server Address] [-p Server Port]
Options:
    -h  Prints this message and exits
    -a  Address in which server is located (e.g. 127.0.0.1)
    -p  Port in which server is located (e.g. 4000)
"""

from threading import Thread
from slipstream import *
import logging
def main():
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

#    t = Thread(target=slipstream, args=(host,port,))
#    t.start()
    slipstream(host, port)

def slipstream(host, port):
    client = SlipStream(host, port)
    client.connect()
    client.receive()

if __name__ == '__main__':
    main()
