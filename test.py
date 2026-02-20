import numpy as np
from sklearn.cluster import KMeans

# CPU data
X = np.random.rand(10000, 4)

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print([labels, centroids])