import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Read data from CSV
csv_path = "C:\\Users\\Ömer Yiğit Kavas\\Downloads\\exoplanet.eu_catalog.csv"
data = pd.read_csv(csv_path)

data = data.sort_values(by=['orbital_period', 'mass'], ascending=[False, False]).iloc[500:]

# Erase the 10 planets with the lowest mass
data = data.iloc[10:]

data = data[['mass', 'orbital_period', 'radius']].dropna(subset=['mass', 'orbital_period', 'radius'])

if data.empty:
    print("No valid data remaining after removing rows with missing 'mass', 'orbital_period', or 'radius'.")
else:
    x = data.values

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    gm = GaussianMixture(n_components=5).fit(x_scaled)
    centers = scaler.inverse_transform(gm.means_)
    print("Cluster Centers:\n", centers)

    pred = gm.predict(x_scaled)

    df = pd.DataFrame({'mass': x[:, 0], 'orbital_period': x[:, 1], 'radius': x[:, 2], 'label': pred})
    groups = df.groupby('label')

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for name, group in groups:
        ax.scatter(np.log10(group.mass), np.log10(group.orbital_period), np.log10(group.radius), label=name, s=8)

    # Plot cluster centers
    ax.scatter(np.log10(centers[:, 0]), np.log10(centers[:, 1]), np.log10(centers[:, 2]),
               marker='X', c='red', s=100, label='Cluster Center')

    ax.set_xlabel('Log10(Mass)')
    ax.set_ylabel('Log10(Orbital Period)')
    ax.set_zlabel('Log10(Radius)')
    ax.set_title('Clustered Exoplanet Data in 3D (Logarithmic Mass, Orbital Period, and Radius)')
    plt.legend()
    plt.show()
