import logging
import cairoplot

class Activity:
    class Properties:
        max_graph_data = 100

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

        def createGraph(self, filename):
            if self.getNumDataPoints() < 5:
                return
            else:
                pass

            data = {}
            for axis in ["x", "y", "z"]:
                index = min(len(self.avg[axis]), Activity.Properties.max_graph_data)
                data[axis] = self.avg[axis][-index:]
            file = filename + "_avg"
            cairoplot.dot_line_plot(name=file,
                                    data=data,
                                    width=900,
                                    height=900,
                                    border=3,
                                    axis=True,
                                    grid=True,
                                    y_bounds=(-2,2),
                                    series_legend=True,
                                    x_title = "Time (minutes:seconds)",
                                    y_title = "Average") 

            data = {}
            for axis in ["x", "y", "z"]:
                index = min(len(self.std_deviation[axis]), Activity.Properties.max_graph_data)
                data[axis] = self.std_deviation[axis][-index:]

            file = filename + "_std_dev"
            cairoplot.dot_line_plot(name=file,
                                    data=data,
                                    width=900,
                                    height=900,
                                    border=3,
                                    axis=True,
                                    grid=True,
                                    y_bounds=(0,1),
                                    series_legend=True,
                                    x_title = "Time (minutes:seconds)",
                                    y_title = "Standard Deviation") 





    def __init__(self, keys):
        self.logging = logging.getLogger("activity")
        self.history = None

        self._sensorDict = {}
        for k in keys:
            self._sensorDict[k] = Activity.Properties()

    def add(self, name, avg, std_deviation):
        self._sensorDict[name].add(avg, std_deviation)

    def createGraph(self, filepath, convertToPng=False):
        for k in self._sensorDict.keys():
            filename = filepath + "/" + k
            self._sensorDict[k].createGraph(filename)

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
            if self.__isHorizontal(legs):
                if self.__isHorizontal(arms):
                    # lying down
                    print "Lying Down"
                else:
                    # sitting
                    print "Sitting"
            else:
                # standing
                print "Standing"
        else:
            # moving: running, walking
            if self.__isRunning(legs):
                print "Running"
            else:
                print "Walking"

    def __isRunning(self, list):
        def running((x,y,z)):
            errorMargin = 0.25

            if x > errorMargin or \
               y > errorMargin or \
               z > errorMargin:
                    return True
            return False

        for k in list:
            std_dev = self._sensorDict[k].getStdDeviation()
            if running(std_dev):
                pass
            else:
                return False
        return True

    def __isHorizontal(self, list):
        def horizontal((x, y, z)):
            errorMargin = 0.20

            if (-errorMargin) <= x <= (errorMargin):
                return True
            return False
 
        for k in list:
            avg = self._sensorDict[k].getAverage()
            if not horizontal(avg):
                return False
        return True

    def __isVertical(self, list):
        def vertical((x, y, z)):
            errorMargin = 0.20

            if (-errorMargin) <= z <= (errorMargin):
                return True
            return False

        for k in list:
            avg = self._sensorDict[k].getAverage()
            if not vertical(avg):
                return False
        return True

    def __isStable(self, (x, y, z)):
        errorMargin = 0.05

        if x <= (errorMargin):
            if y <= (errorMargin):
                if z <= (errorMargin):
                    return True
        return False
 
