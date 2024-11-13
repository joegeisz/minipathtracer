import numpy as np

class Sphere:
    """Sphere class"""
    def __init__(self,center,radius):
        self.c = np.array(center)
        self.r = radius

    def ray_intersect(self,ray):
        intersect = np.empty(3)
        b = 2*np.dot(ray.dir,ray.x-self.c)
        c = np.dot(ray.x-self.c,ray.x-self.c) - self.r**2
        desc = b**2-4*c 
        if desc < 0:
            intersect[:] = np.nan
        else:
            t0 = -b - np.sqrt(desc)
            if t0 > 0:
                intersect = ray.x + t0 * ray.dir
            else:
                t1 = -b + np.sqrt(desc)
                intersect = ray.x + t1 * ray.dir
        return intersect


class Plane:
    """Plane Class"""
    def __init__(self,normal,dist):
        self.d = dist
        self.n = normal
        self.nhat = normal/np.linalg.norm(normal)

    def ray_intersect(self,ray):
        vd = np.dot(self.nhat,ray.dir)
        intersect = np.empty(3)
        if np.abs(vd) < 1.0e-5:
            intersect[:] = np.nan
            return intersect
        else:
            v0 = -np.dot(self.nhat,ray.x) - self.d
            t = v0/vd
            if t < 0:
                intersect[:] = np.nan
                return intersect
            else:
                intersect = ray.x + t * ray.dir
                return intersect

class Ray:
    """Ray Class"""
    def __init__(self,start,direction):
        self.x = start
        self.dir = direction/np.linalg.norm(direction)

class Camera:
    """Camera Class"""
    def __init__(self,center,point_at,xpix,ypix,width,up=np.array([0,0,1])):
        self.c = np.array(center)
        dir = np.array(point_at) - center
        self.dir = dir / np.linalg.norm(dir)
        self.nx = xpix
        self.ny = ypix 
        self.w = width
        self.up = up
        self.R = self.rotation_matrix()
        assert np.isnan(self.R).any() == False

    def rotation_matrix(self):
        # Get angles of rotation
        phi = -np.arctan2(self.dir[2], np.sqrt(self.dir[0]**2+self.dir[1]**2))
        theta = np.arctan2(self.dir[1], self.dir[0])
        print(theta*180/np.pi,phi*180/np.pi)

        # Rotation matrix around the z-axis
        R_z = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])

        # Rotation matrix around the y-axis
        R_y = np.array([
            [np.cos(phi), 0, np.sin(phi)],
            [0, 1, 0],
            [-np.sin(phi), 0, np.cos(phi)]
        ])

        # Combined rotation matrix
        R = np.dot(R_z, R_y)
        return R
    
    def iterate_rays(self):
        dw = self.w / self.nx
        halfwx = self.w / 2
        halfwy = self.ny * dw / 2
        for x in range(self.nx):
            for y in range(self.ny):
                plane_pt = np.array([1, dw*x - halfwx, halfwy - dw*y])
                direction = np.dot(self.R, plane_pt)
                yield Ray(self.c, direction), x, y

class Scene:
    """Scene Class"""
    def __init__(self,object_list,camera):
        self.objects = object_list 
        self.camera = camera 

    def intersection_image(self):
        img = np.zeros([self.camera.ny,self.camera.nx])
        for ray, x, y in self.camera.iterate_rays():
            for ob in self.objects:
                intersect = ob.ray_intersect(ray)
                if np.isnan(intersect).any():
                    pass
                else:
                    img[y,x] = 1/(10+np.linalg.norm(intersect))
        return img


