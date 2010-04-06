import logging

class Activity:
    class Properties:
        def __init__(self):
            self.avg = {}
            self.avg["x"] = []
            self.avg["y"] = []
            self.avg["z"] = []

            self.std_deviation = {}
            self.std_deviation["x"] = []
            self.std_deviation["y"] = []
            self.std_deviation["z"] = []

        def add(self, average, std_deviation):
            # average
            self.avg["x"].append(average[0])
            self.avg["y"].append(average[1])
            self.avg["z"].append(average[2])

            # stnd deviation
            self.std_deviation["x"].append(std_deviation[0])
            self.std_deviation["y"].append(std_deviation[1])
            self.std_deviation["z"].append(std_deviation[2])

        def getAverage(self):
            x = self.avg["x"][-1]
            y = self.avg["y"][-1]
            z = self.avg["z"][-1]

            return (x, y, z)

        def getStdDeviation(self):
            x = self.std_deviation["x"][-1]
            y = self.std_deviation["y"][-1]
            z = self.std_deviation["z"][-1]

            return (x, y, z)

        def getNumDataPoints(self):
            return len(self.avg["x"])

    def __init__(self, keys):
        self.logging = logging.getLogger("activity")

        self._sensorDict = {}
        for k in keys:
            self._sensorDict[k] = Activity.Properties()

    def add(self, name, avg, std_deviation):
        self._sensorDict[name].add(avg, std_deviation)

    def doAllTests(self):
        for k in self._sensorDict.keys():
            if self._sensorDict[k].getNumDataPoints() <= 0:
                return

        isStationary = True
        for k in ["left_leg", "right_leg"]:
            std_dev = self._sensorDict[k].getStdDeviation()

            if not self.__isStable(std_dev):
                isStationary = False
                break

        if isStationary:
            self.logging.info("Lying Down:\t%s", self.isLyingDown())
            self.logging.info("Standing:\t\t %s", self.isStanding())
            self.logging.info("Sitting:\t\t %s", self.isSitting())
        else:
            self.logging.info("legs are moving")

    def isLyingDown(self):
        for k in self._sensorDict.keys():
            avg = self._sensorDict[k].getAverage()

            if not self.__isHorizontal(avg):
                return False
 
        return True

    def isSitting(self):
        for k in self._sensorDict.keys():
            avg = self._sensorDict[k].getAverage()

            if k in ["left_arm", "right_arm"]:
                if not self.__isVertical(avg):
                    return False
            else:
                if not self.__isHorizontal(avg):
                    return False

        return True


    def isStanding(self):
        for k in self._sensorDict.keys():
            avg = self._sensorDict[k].getAverage()

            if not self.__isVertical(avg):
                return False
 
        return True

    def __isVertical(self, (x, y, z)):
        errorMargin = 0.20

        if (1-errorMargin) <= x <= (1+errorMargin):
            if (-errorMargin) <= y <= (errorMargin):
                if (-errorMargin) <= z <= (errorMargin):
                    return True

        return False

    def __isHorizontal(self, (x, y, z)):
        errorMargin = 0.20

        if (-errorMargin) <= x <= (errorMargin):
            if (-errorMargin) <= y <= (errorMargin):
                if (1-errorMargin) <= z <= (1+errorMargin):
                    return True

        return False
        
    def __isStable(self, (x, y, z)):
        errorMargin = 0.15

        if (-errorMargin) <= x <= (errorMargin):
            if (-errorMargin) <= y <= (errorMargin):
                if (-errorMargin) <= z <= (errorMargin):
                    return True

        return False
 
