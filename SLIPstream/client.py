#!/usr/bin/python
"""
USAGE: %s <server> <word> <port>
"""
 
from socket import *
import time

def main():

    # Set the socket parameters
    host = "127.0.0.1"
    port = 4000
    buf = 1024
    addr = (host,port)
   # Create socket
    sock = socket(AF_INET, SOCK_DGRAM)
    msg = "Whatever message goes \r\n"
    sock.sendto(msg,addr)
 
    while True:

        messin, server = sock.recvfrom(255)
        print "Received:", messin
 
    sock.close()


"""
    import getopt, sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                sys.exit()

        taskList = []
        for arg in args:
            taskParams = arg.split(',')
            task = Task(taskParams[0], taskParams[1])
            taskList.append(task)

        if len(taskList) == 0:
            raise IndexError

        simulate = Edf(taskList).start()

    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    except IndexError, err:
        print __doc__ % argv[0]
        print "Error: Missing argument(s)"
        sys.exit(2)
"""
if __name__ == '__main__':
    main()
