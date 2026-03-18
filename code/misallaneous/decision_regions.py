import numpy as np
import matplotlib.pyplot as plt

# Fake classifier (vertical boundary at x = 0)
def model(X):
    return (X[:, 0] > 0).astype(int)

# Grid
x_min, x_max = -5, 5
y_min, y_max = -5, 5

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 200),
    np.linspace(y_min, y_max, 200)
)

# Flatten → predict → reshape
grid = np.c_[xx.ravel(), yy.ravel()]
Z = model(grid)
Z = Z.reshape(xx.shape)

# Plot regions
plt.pcolormesh(xx, yy, Z, shading='auto')

# Decision boundary
plt.contour(xx, yy, Z, levels=[0.5], colors='k')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.show()