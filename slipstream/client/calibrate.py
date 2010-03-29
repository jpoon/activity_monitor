from util import *
from sensor import *
import logging

class Calibrate_Thread(StoppableThread):
    sample_size = 5
    key_dataStart = "dataStart"

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
            self.axis_data = data

        def get_zero_g_value(self):
            for i in range(len(self.axis_data)):
                if self.axis_data[i][0] == 0:
                    return self.axis_data[i][1]

        def get_adcCounts_per_g(self):
            for i in range(len(self.axis_data)-1):
                item1 = self.axis_data[i]
                item2 = self.axis_data[i+1]

                outputResponse_diff = item1[0]-item2[0]
                if outputResponse_diff != 0:
                    count_diff = item1[1] - item2[1]
                    return abs((item1[1] - item2[1])/outputResponse_diff)

    def __init__(self, cond, sensors):
        # for each sensor location, create a dictionary with keys being
        # the states (e.g. POSITION_1, POSITION_2). The values of each
        # corresponding key represent ADC values at each position

        Thread.__init__(self)
        super(Calibrate_Thread, self).__init__()

        self.cond = cond
        self.sensors = sensors
        self.name = "Calibration Thread"

        self.position= self.Position()

        self.position.add("position_1", (0, 0, 1), "lying flat horizontally")
        self.position.add("position_2", (1, 0, 0), "node placed upright with 'FireFly' text upright")
        self.position.add("position_3", (0, 1, 0), "node lying on its side with LEDs situated on the top edge")

        # Create dictionary for each sensor location
        for key in self.sensors.keys():
            setattr(self, key, {})

    def run(self):
        logging.debug("Starting %s" % self.name)

        # for each calibration position, obtain a set of samples from each sensor node
        for calibrate_position in self.position.getPositionList():
            self.__printPrompt(calibrate_position)

            while True:
                if self.stopped():
                    logging.debug("%s has exited properly" % self.name)
                    return
 
                with self.cond:
                    self.cond.wait()

                    for sensor_location in self.sensors.keys():
                        # Determine whether we have already obtained values at
                        # the current position for the given sensor location
                        if calibrate_position not in getattr(self, sensor_location):
                            current_data_id = self.sensors[sensor_location].getNumSamples()

                            if Calibrate_Thread.key_dataStart not in getattr(self, sensor_location):
                                getattr(self, sensor_location)[Calibrate_Thread.key_dataStart] = current_data_id
                            else:
                                data_start = getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]
                                numSamples = current_data_id - data_start
                                if (numSamples == Calibrate_Thread.sample_size):
                                    getattr(self, sensor_location)[calibrate_position] = self.__getAverage(sensor_location, data_start, current_data_id)
                                    del getattr(self, sensor_location)[Calibrate_Thread.key_dataStart]

                    missing = []
                    for sensor_location in self.sensors.keys():
                        if calibrate_position not in getattr(self, sensor_location):
                            missing.append(sensor_location)

                    if len(missing) == 3:
                        break
                    else:
                        pass
                        #logging.debug("Missing calibration data from %s for %s" % (missing, calibrate_position))

        self.__doAnalysis()
        logging.debug("%s has exited properly" % self.name)

    def __getAverage(self, key, data_start, data_end):
        def average(list, start, end):
            sum = 0
            for val in list[data_start:data_end]:
                sum += val
            return sum/(data_end - data_start)

        acc_x = average(self.sensors[key].acc_x, data_start, data_end)
        acc_y = average(self.sensors[key].acc_y, data_start, data_end)
        acc_z = average(self.sensors[key].acc_z, data_start, data_end)

        return (acc_x, acc_y, acc_z)

    def __doAnalysis(self):
        calibratedSensors = {}
        for sensor_location in self.sensors.keys():
            x_axis = []
            y_axis = []
            z_axis = []
            for calibrate_position in self.position.getPositionList():
                try:
                    outputResponse = self.position.getOutputResponse(calibrate_position)
                    data = getattr(self, sensor_location)[calibrate_position]

                    x_axis.append((outputResponse[0], data[0]))
                    y_axis.append((outputResponse[1], data[1]))
                    z_axis.append((outputResponse[2], data[2]))
                except:
                    pass

            adcCount = (
                self.Axis_Data(x_axis).get_adcCounts_per_g(),
                self.Axis_Data(y_axis).get_adcCounts_per_g(),
                self.Axis_Data(z_axis).get_adcCounts_per_g(),
            )
            zero_g_value = (
                self.Axis_Data(x_axis).get_zero_g_value(),
                self.Axis_Data(y_axis).get_zero_g_value(),
                self.Axis_Data(z_axis).get_zero_g_value(),
            )

            calibratedSensors[sensor_location] = (
                adcCount,
                zero_g_value
            )

        print calibratedSensors
            
    def __printPrompt(self, position):
       import time
       time.sleep(1)
       raw_input("Calibration: Move sensors to %s where %s. Once ready, press 'y' to continue.\r\n" % (position, self.position.getPositionDescription(position)))
