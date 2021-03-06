import socket
from sensor import *
from util import *
import logging

class SlipStream:
    def __init__(self, host, port):
        self.logging = logging.getLogger("slipstream")

        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(1)
        self.connect()

    def connect(self):
        # hack: since we are using UDP, theres no way to
        # determine whether you are actually connected
        # sending an initial packet such that the server
        # accepts the connection and starts forwarding
        # packets to our address
        self.logging.debug('Attempting to connect to %s %s' % self.addr)
        message = "%s connected\r\n" % socket.gethostname()
        self.sock.sendto(message, self.addr)

    def send(self, msg):
        self.logging.debug('Sending %s' % msg)
        self.sock.sendto(msg, self.addr) 

    def receive(self):
        try:
            msg = self.sock.recv(255)

            msg = msg.split()
            nodeId = int(msg.pop(0))
            sensor = self.__convertNodeIdToSensorLocation(nodeId)
            self.logging.debug('Received packet from %s' % sensor)
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
            self.logging.error('Illegal Node ID of %d' % nodeId)

class SlipStream_Thread(StoppableThread):
    def __init__ (self, host, port, sensorList):
        Thread.__init__(self)
        super(SlipStream_Thread, self).__init__()
        self.setName("SlipStream Thread")

        self.logging = logging.getLogger("slipstream")

        self.host = host
        self.port = port
        self.sensorList = sensorList

        self.update = {}

    def setCond(self, cond):
        self.cond = cond

    def getUpdate(self):
        updateList = self.update.keys()
        self.update.clear()
        return updateList

    def run(self):
        self.logging.debug("Starting %s" % self.getName())
        client = SlipStream(self.host, self.port)
        while True:
            if self.stopped():
                if hasattr(self, "cond"):
                    with self.cond:
                        self.cond.notifyAll()
                self.logging.debug("%s has exited properly" % self.name)
                return

            (sensor, msg) = client.receive()
            
            if msg is not None:
                if hasattr(self, "cond"):
                    with self.cond:
                        self.__run(sensor, msg)
                else:
                    self.__run(sensor, msg)

    def __run(self, sensor, msg):
        self.sensorList.addSample(sensor, msg)
        self.update[sensor] = 1
        self.cond.notifyAll()
 
