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

        def getNumDataPoints(self):
            return len(self.avg["x"])

    def __init__(self, keys):
        self.logging = logging.getLogger("activity")

        self._sensorDict = {}
        for k in keys:
            self._sensorDict[k] = Activity.Properties()

    def add(self, name, avg, std_deviation):
        self._sensorDict[name].add(avg, std_deviation)

    def isLyingDown(self):
        for k in self._sensorDict.keys():
            avg_x = self._sensorDict[k].avg["x"][-1]
            avg_y = self._sensorDict[k].avg["y"][-1]
            avg_z = self._sensorDict[k].avg["z"][-1]

            if self.__isHorizontal(avg_x,avg_y,avg_z) is False:
                print "%s - %s %s %s" % (k, avg_x, avg_y, avg_z)
                return False

            dev_x = self._sensorDict[k].std_deviation["x"][-1]
            dev_y = self._sensorDict[k].std_deviation["y"][-1]
            dev_z = self._sensorDict[k].std_deviation["z"][-1]

            if self.__isStable(dev_x, dev_y, dev_z) is False:
                print "%s - %s %s %s" % (k, dev_x, dev_y, dev_z)
                return False

        return True

def __isHorizontal(self, x, y, z):
    errorMargin = 0.15

    if (-errorMargin) <= x <= (errorMargin):
        if (-errorMargin) <= y <= (errorMargin):
            if (1-errorMargin) <= z <= (1+errorMargin):
                return True

    return False
        
    def __isStable(self, x, y, z):
        errorMargin = 0.15
        if (-errorMargin) <= x <= (errorMargin):
            if (-errorMargin) <= y <= (errorMargin):
                if (-errorMargin) <= z <= (errorMargin):
                    return True

        return False
 
