import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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


#combo scatterer for visualizing clustering on all the 2D (NC2) combinations of the selected features

def ScatterBatch(data, *columns, k=0):
    columnLength = len(columns)
    numPlots = (columnLength * (columnLength - 1)) // 2  # calculating the number of unique subplots for 2D (nC2)
    cols = 2  # Set 2 plots per row
    rows = int(np.ceil(numPlots / cols))  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))

    # Flatten the axes array for easier indexing
    axes = axes.flatten()

    plotIndex = 0
    fname = "k.txt"
    with open(fname, "a") as F:
        F.write(f"*******************************************\nNew execution log: (ran with K = {k})\n(this is appended to the file each time model.py is run)\n*******************************************\n")
    for i in range(columnLength):
        for j in range(i + 1, columnLength):

            centers, assignedPoints = KMeans(data[[columns[i], columns[j]]], k)
            axes[plotIndex].scatter(x=data[columns[i]], y=data[columns[j]], c = assignedPoints)

            axes[plotIndex].scatter(centers[:, :1], centers[:, 1:], c="red", marker="X", linewidth=5)

            axes[plotIndex].set_title(f"{columns[i]} vs {columns[j]}")
            plotIndex += 1
            centerIndices, uniquesCount = np.unique(assignedPoints, return_counts=True)


            with open(fname, "a") as f:
                f.write(f"2D clustering for: {columns[i]} vs {columns[j]}\n")
                for Y in centerIndices:
                    f.write(f"\n points assigned to center {centerIndices[Y]}: {uniquesCount[Y]} points\n")
                f.write("--------------------\n\n")
    # Turn off any unused axes
    for idx in range(plotIndex, len(axes)):
        fig.delaxes(axes[idx])  # Remove unused subplots (because the subplotting always results in an even sized grid of subplots)

    fig.tight_layout()  #tight fit to avoid any overlapping


file = r"res_dpre.csv"
df = pd.read_csv(file)
print(df.head())


k = 3 #number of centers

#deciding which features are best to implement the clustering on (high correlation is the goal)
"""
corr_matrix = df.drop(["diagnosis", "radius_category", "texture_category"],axis=1).corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix, annot=True)
#great balancing combination of features: radius_mean, compactness_mean, area_mean, concave_points_mean
"""

ScatterBatch(df, "radius_mean", "compactness_mean", "concave_points_mean", "symmetry_mean", k=k)

plt.show()

