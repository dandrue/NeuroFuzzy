import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def objective(val1, val2):
    return val2 * np.sin(val1) + val1 * np.cos(val2)


def evaluate():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    # print(X)
    # print(Y)

    Z = objective(X, Y).T
    print(Z.max())
    print(Z.min())
    # print(Z)
    return X, Y, Z


def plotting():
    X, Y, Z = evaluate()
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    _ = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)
    _ = ax.set_xlabel('X')
    _ = ax.set_ylabel('Y')
    _ = ax.set_zlabel('Z')
    _ = ax.set_title('Objective')

    # surface_plot with color grading and color bar
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    _ = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=matplotlib.cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()
