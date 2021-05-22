import sys
import random
import pandas
import numpy

dataPandas = pandas.read_csv(open(r'costumer.data'), na_values=['?'], sep='[,\s]*', engine='python')

def kMeans(dataNumpy, k, n):
    centroids = dataNumpy[numpy.random.choice(range(dataNumpy.shape[0]), k, replace=False), :]

    for iteration in range(n):
        euclidianDistance = numpy.sum((centroids[:, numpy.newaxis, :] - dataNumpy) ** 2, axis=2)
        closestPoints = numpy.argmin(euclidianDistance, axis=0)

        for i in range(k):
            centroids[i, :] = dataNumpy[closestPoints == i, :].mean(axis=0)

    return centroids


def kMeansClustering(dataPandas, k, n):

    dataChannelRegion = dataPandas.iloc[:, 0:2].values

    dataPandas.drop('Channel', 1, inplace=True)
    dataPandas.drop('Region', 1, inplace=True)
    dataPandas.dropna()
    headers = list(dataPandas.columns)

    dataNumpy = dataPandas.iloc[:, :].values
    centroids = kMeans(dataNumpy, k, n)

    euclidianDistance = numpy.sum((centroids[:, numpy.newaxis, :] - dataNumpy) ** 2, axis=2)
    clusterId = numpy.argmin(euclidianDistance, axis=0)

    for j in range(0, k):

        print("--------------------------------------")
        print("")
        print("CLUSTER NO:", j + 1)



        indices = numpy.where(clusterId == j)[0]
        channelStats = {1: 0, 2: 0}
        regionStats = {1: 0, 2: 0, 3: 0}

        for index in indices:
            channel = dataChannelRegion[index, 0]
            region = dataChannelRegion[index, 1]

            channelStats[channel] += 1
            regionStats[region] += 1


        count = 0

        for key in channelStats.keys():
            row = "Number of cases with channel equals: " + repr(key) + ": " + repr(channelStats[key])
            count +=channelStats[key]
            print(row)
        print("-----------")

        for key in regionStats.keys():
            row = "Number of cases with region equals: " + repr(key) + ": " + repr(regionStats[key])
            print(row)

        print("TOTAL Number of cases: ", count)
        print("-----------")
        print("CENTROID VALUES: ")

        for i in range(0, 6):
            row = repr(headers[i]) + ': ' + repr(centroids[j][i])
            print(row)

    print("--------------------------------------")



kMeansClustering(dataPandas, 3, 10)


