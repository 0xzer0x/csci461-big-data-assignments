import numpy as np
import pandas as pd

"""
this version of the model basically implements the same KMeans algorithm on multiple features all at once (no 2D combining of features combinatorically to visualize 
the clustering and the centers in pyplot... so this one has no visualization
"""

def distance(points1, points2):
    #sq( ( (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2 + ... + (m2-m1)^2) )
    return np.sqrt(np.sum((points2-points1)**2))


# assign clusters and update
def KMeans(Data, K, maxIterations=100):
    data = None

    if (not isinstance(Data, np.ndarray)):
        data = Data.to_numpy()
    else:
        data = np.copy(Data)
    numPoints = Data.shape[0]
    numFeatures = Data.shape[1]  # also determines the dimension of our points, for example if they're 3 features our points will be in 3D and harder to plot and visualize

    if (not K) or (str(K).strip() == "") or (K <= 0):
        K = numFeatures
        print(f"Assigned K automatically... K = {K}")

    distanceAssignments = np.zeros(numPoints,dtype=int)  # holds indices of the centers for each point in the data - the index represents the closest center to that point
    # the idea is mapping corresponding order of points from the data rows to the indices array (indices determine which center the points are assigned to)

    #prevDistanceAssignments = np.zeros(numPoints, dtype=int)
    prevDistanceAssignments = np.copy(distanceAssignments)

    DistancesToCenters = np.zeros(K)
    scaler = np.random.default_rng(None).uniform(low=data.min(), high=data.max(), size=1)
    # = np.random.uniform() #uniformly distributed centers to ensure all centers will find closest points most of the time
    #print(scalesArr)
    Centers = scaler * np.random.random((K, numFeatures)) #scale the generated centers between 0 and 1 to a uniform range depending on the max and min of the dataset

    for T in range(maxIterations):
        for i in range(numPoints):  # iterating over all points
            currPoint = data[i]

            for j in range(K):  # calculating distance between all centers and each point
                DistancesToCenters[j] = distance(currPoint, Centers[j])

            closestCenterIndex = np.argmin(DistancesToCenters)  # getting the index of the closest center to the current point

            #print(f"\nprevious distance assignments: {prevDistanceAssignments}\n")
            distanceAssignments[i] = closestCenterIndex

        # if (np.array_equal(distanceAssignments, prevDistanceAssignments)): #break early when you notice that the updated center distances are exactly the same
        #   break

        # the center update loop should happen here

        for z in range(K):
            assignedPoints = data[distanceAssignments == z]
            #print(f"Assigned points for center {z}: {assignedPoints}")

            # print(distanceAssignments, distanceAssignments.flatten())
            # print(f"centers: {Centers[z]}\n mean: {mean}")

            if (len(assignedPoints) > 0): #because sometimes the assignedPoints array yields nan
                Centers[z] = assignedPoints.mean(axis=0).copy()

        if (np.array_equal(distanceAssignments, prevDistanceAssignments)):
            print(f"exited at T = {T}")
            break
        prevDistanceAssignments = np.copy(distanceAssignments)


    return Centers, distanceAssignments

file = r"res_dpre.csv"
df = pd.read_csv(file)

X = df[["radius_mean", "compactness_mean", "area_mean", "concave_points_mean"]]
print(X.head())
k = 3 #number of centers

centers, assignedPoints = KMeans(X, K=k) #4D Clustering with k = 3 (3 centers)
fname = "k_nd.txt"

centerIndices, uniquesCount = np.unique(assignedPoints, return_counts=True)
with open(fname, "a") as f:
    f.write(f"*******************************************\nNew execution log: (ran with K = {k})\n(this is appended to the file each time model_ND_version.py is run)\n*******************************************\n")
    for i in centerIndices:
        f.write(f"points assigned to center {centerIndices[i]}: {uniquesCount[i]} points\n")

#print(f"Centers from clustering:\n{centers}\n-------------------\nAssigned points from the data to the center indices:\n{assignedPoints}")
