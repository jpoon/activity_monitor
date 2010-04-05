from __future__ import division
import math

def getAverage(dataList, startIndex, endIndex):
    def average(dataList):
        sum = 0
        for val in dataList:
            sum += val
        return sum/len(dataList)

    avg_x = average(dataList.x[startIndex:endIndex])
    avg_y = average(dataList.y[startIndex:endIndex])
    avg_z = average(dataList.z[startIndex:endIndex])

    return (avg_x, avg_y, avg_z)

def getVariance(dataList, startIndex, endIndex):
    def variance(dataList, avg):
        sum = 0
        for val in dataList:
            sum += (val - avg)**2

        return sum/(len(dataList) - 1)

    (avg_x, avg_y, avg_z) = getAverage(dataList, startIndex, endIndex)
    var_x = variance(dataList.x[startIndex:endIndex], avg_x)
    var_y = variance(dataList.y[startIndex:endIndex], avg_y)
    var_z = variance(dataList.z[startIndex:endIndex], avg_z)

    return (var_x, var_y, var_z)

def getStndDeviation(dataList, startIndex, endIndex):
    stndDeviation = []
    for axis in getVariance(dataList, startIndex, endIndex):
        stndDeviation.append(math.sqrt(axis))
    return stndDeviation
    
