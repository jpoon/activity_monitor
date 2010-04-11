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
        self.history = None

        self._sensorDict = {}
        for k in keys:
            self._sensorDict[k] = Activity.Properties()

    def add(self, name, avg, std_deviation):
        self._sensorDict[name].add(avg, std_deviation)

    def doAllTests(self):
        legs = ["left_leg", "right_leg"]
        arms = ["left_arm", "right_arm"]

        for k in self._sensorDict.keys():
            if self._sensorDict[k].getNumDataPoints() <= 0:
                return

        legs_stationary = True
        for k in legs:
            std_dev = self._sensorDict[k].getStdDeviation()

            if not self.__isStable(std_dev):
                legs_stationary = False
                break

        if legs_stationary:
            # stationary: sitting, lying down, standing
            if self.isHorizontal(legs):
                if self.isHorizontal(arms):
                    # lying down
                    if self.history is not "lying_down":
                        print "Lying Down"
                        self.history = "lying_down"
                else:
                    # sitting
                    if self.history is not "sitting":
                        print "Sitting"
                        self.history = "sitting"
            else:
                # standing
                if self.history is not "standing":
                    print "Standing"
                    self.history = "standing"
        else:
            # moving: running, walking
            print "moving.."

    def isHorizontal(self, list):
        def horizontal((x, y, z)):
            errorMargin = 0.20

            if (-errorMargin) <= x <= (errorMargin):
                if (-errorMargin) <= x <= (errorMargin):
                        return True
            return False
 
        for k in list:
            avg = self._sensorDict[k].getAverage()
            if not horizontal(avg):
                return False
        return True

    def isVertical(self, list):
        def vertical((x, y, z)):
            errorMargin = 0.20

            if (-errorMargin) <= y <= (errorMargin):
                if (-errorMargin) <= z <= (errorMargin):
                    return True
            return False

        for k in list:
            avg = self._sensorDict[k].getAverage()
            if not vertical(avg):
                return False
        return True

    def __isStable(self, (x, y, z)):
        errorMargin = 0.15

        if (-errorMargin) <= x <= (errorMargin):
            if (-errorMargin) <= y <= (errorMargin):
                if (-errorMargin) <= z <= (errorMargin):
                    return True

        return False
 
