import numpy as np

class Primative:
    def __init__(self):
        pass

    def ray_intersect_time(self,ray):
        return np.full(3,np.nan,dtype=float), np.nan

    def ray_intersect(self,ray):
        return self.ray_intersect_time(ray)[0]
    
    def ray_time(self,ray):
        return self.ray_intersect_time(ray)[1]
    

class Sphere(Primative):
    """Sphere class"""
    def __init__(self,center,radius):
        self.c = np.array(center).astype(float)
        self.r = float(radius)

    def ray_intersect_time(self,ray):
        intersect = np.empty(3).astype(float)
        t = np.nan
        b = 2*np.dot(ray.dir,ray.x-self.c)
        c = np.dot(ray.x-self.c,ray.x-self.c) - self.r**2
        desc = b**2-4*c 
        if desc < 0:
            intersect[:] = np.nan
        else:
            t0 = (-b - np.sqrt(desc))/2
            if t0 > 0:
                intersect = ray.x + t0 * ray.dir
                t = t0
            else:
                t1 = (-b + np.sqrt(desc))/2
                intersect = ray.x + t1 * ray.dir
                t = t1
        return intersect, t

class Plane(Primative):
    """Plane Class"""
    def __init__(self,normal,dist):
        self.d = float(dist)
        self.n = np.array(normal).astype(float)
        self.nhat = normal/np.linalg.norm(normal)

    def ray_intersect_time(self,ray):
        vd = np.dot(self.nhat,ray.dir)
        intersect = np.empty(3)
        t = np.nan
        if np.abs(vd) < 1.0e-5:
            intersect[:] = np.nan
        else:
            v0 = -np.dot(self.nhat,ray.x) - self.d
            t = v0/vd
            if t < 0:
                intersect[:] = np.nan
                t = np.nan
            else:
                intersect = ray.x + t * ray.dir
        return intersect, t
