from __future__ import division
import math

def getAverage(data):
    def average(dataList):
        sum = 0
        for val in dataList:
            sum += val
        return sum/len(dataList)

    (x, y, z) = data
    return (average(x), average(y), average(z))

def getVariance(data):
    def variance(dataList, avg):
        sum = 0
        for val in dataList:
            sum += (val - avg)**2

        return sum/(len(dataList) - 1)

    (avg_x, avg_y, avg_z) = getAverage(data)
    (x, y, z) = data
    var_x = variance(x, avg_x)
    var_y = variance(y, avg_y)
    var_z = variance(z, avg_z)

    return (var_x, var_y, var_z)

def getStndDeviation(data):
    stndDeviation = []
    for axis in getVariance(data):
        stndDeviation.append(math.sqrt(axis))
    return stndDeviation
    
