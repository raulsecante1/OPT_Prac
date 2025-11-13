import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Modified Griewank function for visualization
def griewank_modified(x, y, scale=1000):
    # exaggerate the quadratic term by using a smaller divisor
    return 1 + (x**2 + y**2)/scale - np.cos(x) * np.cos(y / np.sqrt(2))

# Create a meshgrid
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)
Z = griewank_modified(X, Y, scale=500)  # Try 4000 (original), 1000, 500, etc.

# Plot
fig = plt.figure(figsize=(12, 5))

# 3D surface plot
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax1.set_title('Modified Griewank Function (3D Surface)')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('f(X, Y)')
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)

# Mark the global minimum
ax1.scatter(0, 0, griewank_modified(0, 0, 500), color='r', s=50, label='Global minimum (0,0)')
ax1.legend()

# 2D contour plot
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contourf(X, Y, Z, levels=50, cmap='viridis')
ax2.set_title('Modified Griewank Function (2D Contour)')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
fig.colorbar(contour, ax=ax2)

plt.tight_layout()
plt.show()
