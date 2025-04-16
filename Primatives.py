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
            v0 = -np.dot(self.nhat,ray.x) + self.d
            t = v0/vd
            if t < 0:
                pass
            else:
                intersect = ray.x + t * ray.dir
                normal = self.nhat
        return intersect, t, normal

class Tri(Primative):
    """Rectangle Class - like plane but bounded"""

    def __init__(self,p1,p2,p3,**kwargs):
        super().__init__(**kwargs)
        self.p1 = np.array(p1).astype(float)
        self.p2 = np.array(p2).astype(float)
        self.p3 = np.array(p3).astype(float)
        e1 = self.p1-self.p2
        e2 = self.p2-self.p3

        self.n = -np.cross(e1,e2)
        self.nhat = self.n/np.linalg.norm(self.n)
        self.d = np.dot(self.nhat,p1)
        print(self.nhat, self.d)
        self.plane = Plane(self.nhat,self.d)

    def ray_intersect_time_normal(self,ray):
        # find where ray intersects plane in which triangle lies
        intersect, t, normal = self.plane.ray_intersect_time_normal(ray)
        
        # if the ray is parallel, or intersects behind ray, ignore
        if np.isnan(t) or t <= 0:
            intersect = np.full(3,np.nan).astype(float)
            normal = np.full(3,np.nan).astype(float)
            t = np.nan

        # check to see if intersection is within triangle
        else:
            dom_coord = np.argmax(normal)
            uv = [0,1]
            if dom_coord == 0: uv = [1,2]
            elif dom_coord == 1: uv = [0,2]
            p1p = self.p1[uv]-intersect[uv]
            p2p = self.p2[uv]-intersect[uv]
            p3p = self.p3[uv]-intersect[uv]
            nc = 0
            sh = 1
            if p1p[1] < 0: sh = -1
            for a, b in zip([p1p,p2p,p3p],[p2p,p3p,p1p]):
                nsh = 1
                if b[1] < 0: nsh = -1
                if sh != nsh: 
                    if a[0] >= 0 and b[0] >= 0:
                        nc += 1
                    elif a[0] <= 0 and b[0] <= 0:
                        pass 
                    else:
                        uintersect = a[0] - a[1]*(b[0]-a[0])/(b[1]-a[1])
                        if uintersect >= 0:
                            nc += 1
                sh = nsh
            if nc % 2 == 0: # point is outside
                intersect = np.full(3,np.nan).astype(float)
                normal = np.full(3,np.nan).astype(float)
                t = np.nan
        
        return intersect, t, normal

