from util import *
from sensor import *
import logging

class Calibrate_Thread(StoppableThread):
    sample_size = 5
    key_dataStart = "dataStart"

    class State:
        def __init__(self):
            self.stateList = []
            self.outputResponse = {}
            self._iter = iter(self.stateList)

        def __repr__(self):
            return self.current_state

        def addState(self, stateName, outputResponse):
            self.stateList.append(stateName)
            self.outputResponse[stateName] = outputResponse

        def start(self):
            # append a "done" state to end of state list
            self.stateList.append("done")
            self.current_state = self._iter.next()

        def getStateList(self):
            return self.stateList[:-1]

        def getOutputResponse(self, state):
            return self.outputResponse[state]

        def next(self):
            self.current_state = self._iter.next()

        def isDone(self):
            if self.current_state == self.stateList[-1]:
                return True
            else:
                return False

    def __init__(self, cond, sensors):
        # for each sensor location, create a dictionary with keys being
        # the states (e.g. POSITION_1, POSITION_2). The values of each
        # corresponding key represent ADC values at each position

        Thread.__init__(self)
        super(Calibrate_Thread, self).__init__()

        self.cond = cond
        self.sensors = sensors
        self.name = "Calibration Thread"

        self.state = self.State()
        self.state.addState("position_1", (0, 0, 1))
        self.state.addState("position_2", (1, 1, 0))
        self.state.start()

        # Create dictionary for each sensor location
        for key in self.sensors.keys():
            setattr(self, key, {})

    def run(self):
        logging.debug("Starting %s" % self.name)

        while True:
            if self.stopped():
                logging.debug("%s has exited properly" % self.name)
                break

            with self.cond:
                self.cond.wait()

                for sensor_location in self.sensors.keys():
                    # Determine whether we have already obtained values at
                    # the current position for the given sensor location
                    if repr(self.state) not in getattr(self, sensor_location):
                        current_data_id = self.sensors[sensor_location].getNumSamples()

                        if Calibrate_Thread.key_dataStart not in getattr(self, sensor_location):
                            getattr(self, sensor_location)[Calibrate_Thread.key_dataStart] = current_data_id
                        else:
                            numSamples = current_data_id - getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]
                            if (numSamples == Calibrate_Thread.sample_size):
                                del getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]
                                getattr(self, sensor_location)[repr(self.state)] = self.__getAverage(sensor_location)

                missing = []
                for sensor_location in self.sensors.keys():
                    if repr(self.state) not in getattr(self, sensor_location):
                        missing.append(sensor_location)

                if len(missing) == 3:
                    self.state.next()
                    if self.state.isDone():
                        self.__doAnalysis()
                        logging.debug("%s has exited properly" % self.name)
                        break
                else:
                    logging.debug("Missing calibration data from %s for %s" % (missing, self.state))

    def __getAverage(self, key):
        def getAverage(list):
            sum = 0
            for val in list:
                sum += val
            return sum/len(list)

        acc_x = getAverage(self.sensors[key].acc_x)
        acc_y = getAverage(self.sensors[key].acc_y)
        acc_z = getAverage(self.sensors[key].acc_z)

        return (acc_x, acc_y, acc_z)

    def __doAnalysis(self):
        for sensor_location in self.sensors.keys():
            print "--"
            print sensor_location
            for state in self.state.getStateList():
                print self.state.getOutputResponse(state)
                try:
                    print state
                    print getattr(self, sensor_location)[state]
                except:
                    pass
