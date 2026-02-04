import numpy as np
import matplotlib.pyplot as plt
# Create a 1D array
import numpy as np

A = np.zeros((5, 4))        # 5 rows, 4 columns
B = np.random.rand(10, 4)   # random 2D array

b = np.gradient(B)

plt.scatter(B[0], B[1])
plt.show()