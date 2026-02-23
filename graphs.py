import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# fake price x time data
price_bins = 50
time_bins = 100
data = np.random.rand(price_bins, time_bins)

plt.figure(figsize=(12, 6))
sns.heatmap(
    data,
    cmap='inferno',
    cbar=True
)

plt.xlabel("Time")
plt.ylabel("Price level")
plt.title("Liquidity Heatmap")
plt.show()
