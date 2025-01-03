import numpy as np

class Ray:
    """Ray Class"""
    def __init__(self,start,direction):
        self.x = np.array(start).astype(float)
        direction = np.array(direction).astype(float)
        self.dir = direction/np.linalg.norm(direction)


class Camera:
    """Camera Class"""
    def __init__(self,center,point_at,xpix,ypix,width):
        self.c = np.array(center).astype(float)
        dir = np.array(point_at).astype(float) - self.c
        self.dir = dir / np.linalg.norm(dir)
        self.nx = xpix
        self.ny = ypix 
        self.w = width
        self.R = self.rotation_matrix()
        assert np.isnan(self.R).any() == False

    def rotation_matrix(self):
        # Get angles of rotation
        phi = -np.arctan2(self.dir[2], np.sqrt(self.dir[0]**2+self.dir[1]**2))
        theta = np.arctan2(self.dir[1], self.dir[0])

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
        halfwx = self.w / 2.0
        halfwy = self.ny * dw / 2.0
        for x in range(self.nx):
            for y in range(self.ny):
                plane_pt = np.array([1, dw*x - halfwx, halfwy - dw*y]).astype(float)
                direction = np.dot(self.R, plane_pt)
                yield Ray(self.c, direction), x, y
