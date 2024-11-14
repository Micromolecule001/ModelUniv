# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

#       1       Load dataset
data = pd.read_csv("Abalone.csv")
print("Initial Data Preview:")
print(data.head())

# Remove or encode non-numeric columns (like 'Sex' in this case)
data = data.drop('Sex', axis=1)

# Scale data for clustering
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
print("Scaled Data Preview:")
print(scaled_data[:5])

#       2       Number of clusters 
n_clusters = 3 # None Male Female

# K-means clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(scaled_data)
labels = kmeans.labels_

# Display the first few labels assigned to the data points
print("Labels for clusters:", labels[:10])

# Get cluster centroids
centroids = kmeans.cluster_centers_

#       3       Plotting clusters with centroids 
plt.figure(figsize=(14, 8))
pairs = [(0, 1), (1, 2), (2, 3), (3, 4)]  # Specify parameter pairs for visualization
for i, (x, y) in enumerate(pairs):
    plt.subplot(2, 2, i+1)
    plt.scatter(scaled_data[:, x], scaled_data[:, y], c=labels, cmap='viridis', s=50, alpha=0.6)
    plt.scatter(centroids[:, x], centroids[:, y], c='red', marker='X', s=100, label='Centroids')
    plt.xlabel(data.columns[x])
    plt.ylabel(data.columns[y])
    plt.title(f"Cluster Visualization for {data.columns[x]} vs {data.columns[y]}")
plt.tight_layout()
plt.legend()
plt.show()

#       4       Count instances in each cluster
cluster_counts = np.bincount(labels)
print("Instances per Cluster:", cluster_counts)

# Add clustering labels to the dataset for analysis
data['Cluster'] = labels

# Count distribution of samples in each cluster
class_counts = data.groupby('Cluster').size()
print("\nClass Distribution in Each Cluster:")
print(class_counts)

#        5         Determine optimal cluster count using various metrics
wcss = []  # Within-cluster sum of squares (WCSS) for elbow method
silhouette_scores = []  # Silhouette score for separation measure
davies_bouldin_scores = []  # Davies-Bouldin index for compactness and separation

# Test cluster counts from 2 to 10
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))
    davies_bouldin_scores.append(davies_bouldin_score(scaled_data, kmeans.labels_))

# Plot evaluation metrics for optimal cluster count
plt.figure(figsize=(16, 5))

# Elbow Method (WCSS)
plt.subplot(1, 3, 1)
plt.plot(range(2, 11), wcss, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal Clusters')

# Silhouette Score
plt.subplot(1, 3, 2)
plt.plot(range(2, 11), silhouette_scores, marker='o', color='green')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for Optimal Clusters')

# Davies-Bouldin Score
plt.subplot(1, 3, 3)
plt.plot(range(2, 11), davies_bouldin_scores, marker='o', color='red')
plt.xlabel('Number of Clusters')
plt.ylabel('Davies-Bouldin Score')
plt.title('Davies-Bouldin Score for Optimal Clusters')

plt.tight_layout()
plt.show()

#        6       Clustering without scaling for comparison
kmeans_unscaled = KMeans(n_clusters=n_clusters, random_state=0)
kmeans_unscaled.fit(data.drop('Cluster', axis=1))
print("Inertia with scaled data:", kmeans.inertia_)
print("Inertia with unscaled data:", kmeans_unscaled.inertia_)

