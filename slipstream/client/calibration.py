from slipstream import *
from util import *
from sensor import *
import statistics
import logging
import pickle

class Calibrate_Thread(StoppableThread):
    sample_size = 10
    key_dataStart = "dataStart"
    filename_savedData = "calibration.tmp"

    class Position:
        def __init__(self):
            self.positionList = []
            self.outputResponse = {}
            self.description = {}

        def add(self, position, outputResponse, description):
            self.positionList.append(position)
            self.outputResponse[position] = outputResponse
            self.description[position] = description 

        def getPositionList(self):
            return self.positionList

        def getOutputResponse(self, position):
            return self.outputResponse[position]

        def getPositionDescription(self, position):
            return self.description[position] 

    class Axis_Data():
        def __init__(self, data):
            self.outputResponse, self.datapoints = zip(*data)

        def get_zero_g_value(self):
            for i in range(len(self.datapoints)):
                if self.outputResponse[i] == 0:
                    return self.datapoints[i]

        def get_adcCounts_per_g(self):
            for i in range(len(self.datapoints)-1):
                diff = self.outputResponse[i]-self.outputResponse[i+1]

                if diff != 0:
                    return abs((self.datapoints[i] - self.datapoints[i+1])/diff)

    def __init__(self, sensorList, host, port, recalibrate):
        # for each sensor location, create a dictionary with keys being
        # the states (e.g. POSITION_1, POSITION_2). The values of each
        # corresponding key represent ADC values at each position

        Thread.__init__(self)
        super(Calibrate_Thread, self).__init__()
        self.setName("Calibration Thread")

        self.logging = logging.getLogger("calibrate")

        self.host = host
        self.port = port
        self.sensorList = sensorList
        self.recalibrate = recalibrate

        self.position = self.Position()
        self.position.add("position_1", (0, 0, 1), "node lying flat horizontally")
        self.position.add("position_2", (1, 0, 0), "node placed upright with 'FireFly' text upright")
        self.position.add("position_3", (0, 1, 0), "node lying on its side with LEDs situated on the top edge")

        # Create dictionary for each sensor location
        for sensor_location in self.sensorList.getSensorKeys():
            setattr(self, sensor_location, {})

    def run(self):
        self.logging.debug("Starting %s" % self.getName())

        if not self.recalibrate:
            self.__loadSavedCalibration()
            return

        # for each calibration position, obtain a set of samples from each sensor node
        for calibrate_position in self.position.getPositionList():
            self.__printPrompt(calibrate_position)

            cond = Condition()
            slipstream_thread = SlipStream_Thread(self.host, self.port, self.sensorList)
            slipstream_thread.setCond(cond)
            slipstream_thread.start()

            progress_bar = Progress_Bar()
            current_progress = 0

            while True:
                if self.stopped():
                    slipstream_thread.stop()
                    self.logging.debug("%s has exited properly" % self.getName())
                    return

                with cond:
                    cond.wait()

                    for sensor_location in slipstream_thread.getUpdate():
                        if calibrate_position in getattr(self, sensor_location):
                            # we've already obtained calibration data for sensor_location
                            break

                        current_sample_id = self.sensorList.getNumSamples(sensor_location)

                        if Calibrate_Thread.key_dataStart not in getattr(self, sensor_location):
                            # Set Start Index
                            getattr(self, sensor_location)[Calibrate_Thread.key_dataStart] = current_sample_id
                            progress_bar.add(5)
                        else:
                            data_start = getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]
                            numSamples = current_sample_id - data_start

                            progress_bar.add(20/Calibrate_Thread.sample_size)
                            if (numSamples == Calibrate_Thread.sample_size):
                                # Collected enough samples. Now let's analyze it.
                                getattr(self, sensor_location)[calibrate_position] = statistics.getAverage(self.sensorList.getSensorData(sensor_location, data_start, current_sample_id))
                                del getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]

                    if self.__isDone(calibrate_position):
                        # done
                        progress_bar.done()
                        break

            slipstream_thread.stop()
            slipstream_thread.join()

        self.__analysis()
        self.logging.debug("%s has exited properly" % self.name)

    def __isDone(self, position):
        for sensor_location in self.sensorList.getSensorKeys():
            if position not in getattr(self, sensor_location):
                return False

        return True

    def __analysis(self):
        calibratedData = {}
        for sensor_location in self.sensorList.getSensorKeys():
            x = []
            y = []
            z = []
            for calibrate_position in self.position.getPositionList():
                outputResponse = self.position.getOutputResponse(calibrate_position)
                data = getattr(self, sensor_location)[calibrate_position]

                x.append((outputResponse[0], data[0]))
                y.append((outputResponse[1], data[1]))
                z.append((outputResponse[2], data[2]))

            adcCount = {}
            adcCount['x'] = self.Axis_Data(x).get_adcCounts_per_g()
            adcCount['y'] = self.Axis_Data(y).get_adcCounts_per_g()
            adcCount['z'] = self.Axis_Data(z).get_adcCounts_per_g()

            zero_g_value = {}
            zero_g_value['x'] = self.Axis_Data(x).get_zero_g_value()
            zero_g_value['y'] = self.Axis_Data(y).get_zero_g_value()
            zero_g_value['z'] = self.Axis_Data(z).get_zero_g_value()

            calibratedData[sensor_location] = [adcCount, zero_g_value]

        self.sensorList.calibrate(calibratedData) 
        self.__saveCalibration(calibratedData)

    def __saveCalibration(self, data):
        f = open(self.filename_savedData, 'w')
        self.logging.debug("calibration data saved to %s" % self.filename_savedData)
        pickle.dump(data, f)
        f.close()

    def __loadSavedCalibration(self):
        try:
            f = open(self.filename_savedData, 'r')
            self.logging.debug("calibration data loaded from %s" % self.filename_savedData)
            data = pickle.load(f)
            self.sensorList.calibrate(data)
        except IOError:
            self.logging.error("unable to load saved calibration data")

    def __printPrompt(self, position):
       raw_input("\nCalibration: Move sensors to %s where %s. Once ready, press any to continue." % (position, self.position.getPositionDescription(position)))
