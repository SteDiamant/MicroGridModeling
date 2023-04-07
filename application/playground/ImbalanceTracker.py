import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the data into a pandas DataFrame
data = pd.read_csv('data\data_original.csv', index_col='Time', parse_dates=True)

# Define a new feature to capture seasonality
data['Month'] = data.index.month
data = data[~data.index.duplicated(keep='first')]

# Normalize the data
scaler = StandardScaler()
X_norm = pd.DataFrame(scaler.fit_transform(data[['General Demand (W)', 'PV (W)']]), columns=['General Demand (W)', 'PV (W)'])

# Apply k-means clustering with seasonality
kmeans = KMeans(n_clusters=4, random_state=42)
pred_y = kmeans.fit_predict(pd.concat([X_norm, data['Month']], axis=1))

# Add the cluster labels back to the original data
data['Cluster'] = pred_y

# Compute the mean values for each cluster
cluster_means = data.groupby('Cluster').mean()

# Print the mean values for each cluster
print(cluster_means)

# Visualize the mean values for each cluster
plt.scatter(X_norm.iloc[:, 0], X_norm.iloc[:, 1], c=pred_y)
plt.scatter(cluster_means.iloc[:, 0], cluster_means.iloc[:, 1], marker='x', s=200, linewidths=3, color='r')
for i, txt in enumerate(cluster_means.index):
    plt.annotate(txt, (cluster_means.iloc[i, 0], cluster_means.iloc[i, 1]), fontsize=12, color='r')
plt.title('Clusters of General Demand and PV Production')
plt.xlabel('General Demand (normalized)')
plt.ylabel('PV Production (normalized)')
plt.show()
