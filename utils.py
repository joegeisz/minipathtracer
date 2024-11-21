import numpy as np

def random_unit_sphere():
    theta0 = 2*np.pi*np.random.rand()
    theta1 = np.arccos(1-2*np.random.rand())
    x1 = np.sin(theta0)*np.sin(theta1)
    x2 = np.cos(theta0)*np.sin(theta1)
    x3 = np.cos(theta1)
    return np.array([x1,x2,x3])

def hemisphere_sample(normal):
    rand_vec = random_unit_sphere()
    if np.dot(normal,rand_vec) < 0:
        return -rand_vec
    else:
        return rand_vec