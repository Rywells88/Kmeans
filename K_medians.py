import sys

import matplotlib
import numpy as np
from numpy import pi, exp
from scipy.io import loadmat
import matplotlib.pyplot as plt
import random
import sys

max_iterations = 10


# --- initalize clusters------------
def initClusters(k, method,data):
    clusters = []

    if(method == "random"):
        for i in range(k):
            clusters.append((random.uniform(4.3, 8.0),(random.uniform(4.3, 6.0))))
        return clusters
    if (method == "furthestfirst"):
        clusters.append((data[random.randint(0,149)]))
        for c in range(k-1):
            distance_list = []
            for i in range(data.shape[0]):
                point = data[i, :]
                d = sys.maxsize
                for j in range(len(clusters)):
                    temp_dist = distancefunc(point, clusters[j])
                    d = min(d, temp_dist)
                distance_list.append(d)

                ## select data point with maximum distance as our next centroid
            distance_list = np.array(distance_list)
            next_centroid = data[np.argmax(distance_list), :]
            clusters.append(next_centroid)
        return clusters

def distancefunc(point1, point2):
    return np.sum((point1 - point2) ** 2)

def kmedian(data, centres, iterations, assignments):
    global max_iterations


    if (iterations >= max_iterations):
        return assignments
    else:
        c_x = []
        c_y = []

        x = []
        y = []
        classes = []

        iterations += 1
    # -------- E step: assign each datapoint to the cluster whose centre is closest to that datapoint -------
        for point in data:
            distance_list = []
            x.append(point[0])
            y.append(point[1])
            for centre in centres:
                distance = abs(centre[0] - point[0]) + abs(centre[1] - point[1])
                distance_list.append(distance)

            cluster = distance_list.index(min(distance_list))
            assignments.append((cluster, point))

            distance_list.clear()


        for k in centres:
            c_x.append(k[0])
            c_y.append(k[1])
        for i in assignments:
            classes.append(i[0])

        plt.scatter(c_x, c_y, marker='X', linewidths=5)
        colors = ["red", "yellow", "green", "purple"]
        colormap = matplotlib.colors.ListedColormap(colors)
        plt.scatter(x,y,c=classes, cmap=colormap)
        plt.show()
        x = np.array(list(assignments), dtype=object)

        if(iterations != max_iterations):
            assignments.clear()

    # ---------M step: Update each cluster's centres to be the mean of all points assigned to that cluster --

        medianList = []

        for centre in range(len(centres)):
            tmp_list = []
            for point in range(len(x)):
                if(x[point][0] == centre):
                    tmp_list.append(x[point][1])
            if(len(tmp_list) != 0):
                medianList.append((np.median(tmp_list, axis=0)))
                tmp_list.clear()
            else:
                medianList.append(centres[centre])


    if (iterations >= max_iterations):
        return assignments, medianList
    else:
        return kmedian(data, medianList, iterations, assignments)



def main():
    file = loadmat('data.mat')  # dictionary types

    data = file['data']

    initial = initClusters(2,"furthestfirst", data)

    newList = kmedian(data, initial, 0, [])

    print("final assignments", newList[0])

    x = []
    y = []
    centres_x = []
    centres_y = []
    classes = []
    colors = ["red", "yellow", "green","purple"]

    for j in newList[1]:
        centres_x.append(j[0])
        centres_y.append(j[1])


    for i in newList[0]:
        x.append(i[1][0])
        y.append(i[1][1])
        classes.append(i[0])

    colormap = matplotlib.colors.ListedColormap(colors)
    plt.scatter(centres_x,centres_y,marker='X',linewidths=5)
    plt.scatter(x,y, c=classes, cmap=colormap)
    plt.show()







if __name__ == '__main__':
    main()
