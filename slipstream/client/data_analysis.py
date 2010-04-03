from __future__ import division
import logging
import math

class Data_Analysis:
    def __init__(self):
        self.logging = logging.getLogger("data")

    def getAverage(self, dataList, startIndex, endIndex):
        def average(dataList):
            sum = 0
            for val in dataList:
                sum += val
            return sum/len(dataList)

        avg_x = average(dataList.acc_x[startIndex:endIndex])
        avg_y = average(dataList.acc_y[startIndex:endIndex])
        avg_z = average(dataList.acc_z[startIndex:endIndex])

        return (avg_x, avg_y, avg_z)

    def getVariance(self, dataList, startIndex, endIndex):
        def variance(dataList, avg):
            print dataList

            sum = 0
            for val in dataList:
                sum += (val - avg)**2

            return sum/(len(dataList) - 1)

        (avg_x, avg_y, avg_z) = self.getAverage(dataList, startIndex, endIndex)
        var_x = variance(dataList.acc_x[startIndex:endIndex], avg_x)
        var_y = variance(dataList.acc_y[startIndex:endIndex], avg_y)
        var_z = variance(dataList.acc_z[startIndex:endIndex], avg_z)

        return (var_x, var_y, var_z)

    def getStndDeviation(self, dataList, startIndex, endIndex):
        stndDeviation = []
        for axis in self.getVariance(dataList, startIndex, endIndex):
            stndDeviation.append(math.sqrt(axis))
        return stndDeviation
        
