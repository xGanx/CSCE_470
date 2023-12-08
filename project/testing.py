import pandas as pd
import numpy as np

# Assuming your data is in a DataFrame df
# Attributes: Danceability, Energy, Loudness, Speechiness, Acousticness, Instrumentalness, Valence, Tempo, Key

colors = ['blue','green']

# Example data (replace this with your actual data)
data = {
    'Danceability': [0.8, 0.6, 0.75, 0.9],  # Replace with your danceability values
    'Energy': [0.7, 0.5, 0.85, 0.65],  # Replace with your energy values
    'Loudness': [-5, -8, -3, -6],  # Replace with your loudness values
    'Speechiness': [0.1, 0.3, 0.05, 0.15],  # Replace with your speechiness values
    'Acousticness': [0.2, 0.4, 0.1, 0.3],  # Replace with your acousticness values
    'Instrumentalness': [0.15, 0.8, 0.05, 0.9],  # Replace with your instrumentalness values
    'Valence': [0.85, 0.3, 0.9, 0.7],  # Replace with your valence values
    'Tempo': [120, 100, 130, 115],  # Replace with your tempo values
    'Key': ['C', 'G', 'D', 'A']  # Replace with your key values
}

df = pd.DataFrame(data)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Selecting attributes for analysis
selected_attributes = ['Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Valence', 'Tempo']

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[selected_attributes])

# Apply PCA for dimensionality reduction (assuming 2 components for visualization)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

import matplotlib.pyplot as plt

# Scatter plot of reduced dimensions
plt.figure(figsize=(8, 6))
plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.5, color='green')
plt.title('PCA Visualization of Music Attributes')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()
