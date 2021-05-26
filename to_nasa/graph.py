import numpy as np
from mpl_toolkits.mplot3d import Axes3D
# Axes3D import has side effects, it enables using projection='3d' in add_subplot
import matplotlib.pyplot as plt
import random

def plot(nx, ny, data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = range(nx)
    y = range(ny)
    X, Y = np.meshgrid(x, y)
    zs = np.array(data)
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
