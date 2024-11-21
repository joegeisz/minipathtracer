import numpy as np

class Primative:
    def __init__(self, emmitance = np.array([0.0,0.0,0.0],  dtype=float), material_color = np.array([0.5,0.5,0.5],  dtype=float), reflectance = np.array([0.5,0.5,0.5],  dtype=float) ):
        self.emit = np.array(emmitance,dtype=float)
        self.color = np.array(material_color,dtype=float)
        self.reflectance = np.array(reflectance,dtype=float)

    def ray_intersect_time_normal(self,ray):
        return np.full(3,np.nan,dtype=float), np.nan, np.full(3,np.nan,dtype=float)

    def ray_intersect_time(self,ray):
        i,t,n = self.ray_intersect_time_normal(ray)
        return i, t

    def ray_intersect(self,ray):
        return self.ray_intersect_time(ray)[0]
    
    def ray_time(self,ray):
        return self.ray_intersect_time(ray)[1]
    

class Sphere(Primative):
    """Sphere class"""
    def __init__(self,center,radius, **kwargs):
        super().__init__(**kwargs)
        self.c = np.array(center).astype(float)
        self.r = float(radius)

    def ray_intersect_time_normal(self, ray):
        intersect = np.full(3,np.nan).astype(float)
        normal = np.full(3,np.nan).astype(float)
        t = np.nan
        b = 2*np.dot(ray.dir,ray.x-self.c)
        c = np.dot(ray.x-self.c,ray.x-self.c) - self.r**2
        desc = b**2-4*c 
        if desc < 0:
            return intersect, t, normal
        else:
            t0 = (-b - np.sqrt(desc))/2
            t1 = (-b + np.sqrt(desc))/2
            if t0 > 0:
                intersect = ray.x + t0 * ray.dir
                t = t0
                normal = (intersect - self.c)/self.r
            elif t1 > 0:
                t1 = (-b + np.sqrt(desc))/2
                intersect = ray.x + t1 * ray.dir
                t = t1
                normal = (intersect - self.c)/self.r
        return intersect, t, normal
    


class Plane(Primative):
    """Plane Class"""
    def __init__(self,normal,dist,**kwargs):
        super().__init__(**kwargs)
        self.d = float(dist)
        self.n = np.array(normal).astype(float)
        self.nhat = normal/np.linalg.norm(normal)

    def ray_intersect_time_normal(self,ray):
        intersect = np.full(3,np.nan).astype(float)
        normal = np.full(3,np.nan).astype(float)
        t = np.nan
        vd = np.dot(self.nhat,ray.dir)
        if np.abs(vd) < 1.0e-5:
            pass
        else:
            v0 = -np.dot(self.nhat,ray.x) - self.d
            t = v0/vd
            if t < 0:
                pass
            else:
                intersect = ray.x + t * ray.dir
                normal = self.nhat
        return intersect, t, normal
