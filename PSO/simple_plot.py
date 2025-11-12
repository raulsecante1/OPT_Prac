import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the Rastrigin function
def rastrigin(x1, x2):
    return 20 + x1**2 + x2**2 - 10 * (np.cos(2 * np.pi * x1) + np.cos(2 * np.pi * x2))

# Create a grid of values
x1 = np.linspace(-5.12, 5.12, 400)
x2 = np.linspace(-5.12, 5.12, 400)
X1, X2 = np.meshgrid(x1, x2)
Z = rastrigin(X1, X2)

# Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('f(x1, x2)')
ax.set_title('Rastrigin Function')
plt.show()
