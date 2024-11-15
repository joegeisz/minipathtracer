import numpy as np

class Scene:
    """Scene Class"""
    def __init__(self,object_list,camera):
        self.objects = object_list 
        self.nobjects = len(object_list)
        self.camera = camera 

    def intersection_image(self):
        img = np.full([self.camera.ny,self.camera.nx],np.inf,dtype=float)
        for ray, x, y in self.camera.iterate_rays():
            for ob in self.objects:
                intersect, t = ob.ray_intersect_time(ray)
                if np.isnan(t):
                    pass
                elif t < img[y,x]:
                    img[y,x] = np.linalg.norm(intersect)
        return img
    
    def dist_image(self):
        img = np.full([self.camera.ny,self.camera.nx,3],np.inf,dtype=float)
        time_img = np.full([self.camera.ny,self.camera.nx],np.inf)
        for ray, x, y in self.camera.iterate_rays():
            for ob in self.objects:
                intersect, t = ob.ray_intersect_time(ray)
                if np.isnan(t):
                    pass
                elif t < time_img[y,x]:
                    time_img[y,x] = t
                    img[y,x,:] = intersect
        return img
    
    def time_image(self):
        img = np.full([self.camera.ny,self.camera.nx],np.inf,dtype=float)
        for ray, x, y in self.camera.iterate_rays():
            for ob in self.objects:
                intersect_time = ob.ray_time(ray)
                if np.isnan(intersect_time):
                    pass
                elif intersect_time < img[y,x]:
                    img[y,x] = intersect_time
        return img
    
    def object_image(self):
        background_color = [0,0,0]
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(int)
        time_img = np.full([self.camera.ny,self.camera.nx],np.inf)
        img[:,:,0] = background_color[0]
        img[:,:,1] = background_color[1]
        img[:,:,2] = background_color[2]
        ob_colors = np.random.randint(0,255,[self.nobjects,3])
        for ray, x, y in self.camera.iterate_rays():
            for i, ob in enumerate(self.objects):
                intersect_time = ob.ray_time(ray)
                if (not np.isnan(intersect_time)) and (intersect_time < time_img[y,x]) :
                    img[y,x,:] = ob_colors[i,:]
                    time_img[y,x] = intersect_time
                    
        return img
    
    def object_images(self):
        imgs = []
        for ob in self.objects:
            img = np.full([self.camera.ny,self.camera.nx],np.inf,dtype=float)
            for ray, x, y, in self.camera.iterate_rays():
                intersect, t = ob.ray_intersect_time(ray)
                if not np.isnan(t):
                    img[y,x] = np.linalg.norm(intersect)
            imgs.append(img)
        return imgs
