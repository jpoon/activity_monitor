import socket
from sensor import *
import logging

class SlipStream:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.connect()

    def connect(self):
        # hack: since we are using UDP, theres no way to
        # determine whether you are actually connected
        # sending an initial packet such that the server
        # accepts the connection and starts forwarding
        # packets to our address
        logging.debug('Attempting to connect to %s %s' % self.addr)
        message = "%s connected\r\n" % socket.gethostname()
        self.sock.sendto(message, self.addr)

    def send(self, msg):
        logging.debug('Sending %s' % msg)
        self.sock.sendto(msg, self.addr) 

    def receive(self):
        try:
            msg, server = self.sock.recvfrom(255)

            msg = msg.split()
            nodeId = int(msg.pop(0))
            sensor = self.__convertNodeIdToSensorLocation(nodeId)
            logging.debug('Received packet from %s' % sensor)
            return (sensor, msg) 
        except:
            return (None, None)

    def close(self):
        self.sock.close()

    def __convertNodeIdToSensorLocation(self, nodeId):
        if nodeId == 16:
            return "left_arm"
        elif nodeId == 17:
            return "right_arm"
        elif nodeId == 18:
            return "left_leg"
        elif nodeId == 19:
            return "right_leg"
        else:
            logging.error('Illegal Node ID of %d' % nodeId)


