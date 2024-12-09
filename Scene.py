import numpy as np
from utils import *
from SpecialObjects import *
from multiprocessing import Pool
import copy

class Scene:
    """Scene Class"""
    def __init__(self,object_list,camera):
        self.objects = object_list 
        self.nobjects = len(object_list)
        self.camera = camera 

    def object_hit(self,ray):
        ob_ind = -1
        t = np.inf
        normal = np.full(3,np.nan,dtype=float)
        intersection = np.full(3,np.nan,dtype=float)
        for i, ob in enumerate(self.objects):
            intersect, t_hit, norm = ob.ray_intersect_time_normal(ray)
            if t_hit < t and t_hit > 1e-10:
                t = t_hit
                ob_ind = i
                normal = norm
                intersection = intersect
        return ob_ind, t, intersection, normal

    def trace_path(self, ray, depth, max_depth=5):
        if depth >= max_depth:
            return np.array([0.0,0.0,0.0], dtype=float)
        ob, t, inter, norm = self.object_hit(ray)
        #print(depth,ob,norm,t,inter)
        if ob == -1:
            return np.array([0.0,0.0,0.0], dtype=float)
        emit = self.objects[ob].emit
        newdir = hemisphere_sample(norm)
        new_ray = Ray(inter,newdir)
        p = 1/(2*np.pi)
        costheta = np.dot(newdir, norm)
        bdrf = self.objects[ob].reflectance/np.pi
        incoming = self.trace_path(new_ray,depth+1,max_depth)
        return emit + bdrf*incoming*costheta/p

    def path_image(self,maxsteps=5):
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        for ray, x, y in self.camera.iterate_rays():
            img[y,x,:] = self.trace_path(ray,0,maxsteps)                    
        return img
    
    def path_trace_image(self,samples,n_processors = 4):
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        with Pool(n_processors) as p:
            imgs = np.array(p.map(mp_path_trace, [copy.copy(self) for i in range(samples)]))
        img = np.mean(imgs,0)
        return img
    
    def save_path_trace_images(self,samples,maxsteps=5,n_processors = 4):
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        with Pool(n_processors) as p:
            p.map(mp_path_trace_save, [[copy.copy(self),i] for i in range(samples)])
        return img
    
    def color_mix_random_walk(self,start_ray, maxsteps):
        color = np.array([0.0,0.0,0.0], dtype=float)
        step = 0.0
        ray = start_ray
        while step < maxsteps:
            ob, t, intersect, normal = self.object_hit(ray)
            if ob == -1:
                break
            color += self.objects[ob].color
            step += 1.0
            ray = Ray(intersect,hemisphere_sample(normal))
        return color/step
    
    def color_mixing_image(self,maxsteps=5):
        background_color = [0,0,0]
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        img[:,:,0] = background_color[0]
        img[:,:,1] = background_color[1]
        img[:,:,2] = background_color[2]
        for ray, x, y in self.camera.iterate_rays():
            img[y,x,:] = self.color_mix_random_walk(ray,maxsteps)                    
        return img
    
    def color_mix_image_samples(self,samples,maxsteps = 5):
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        for s in range(samples):
            img += self.color_mixing_image(maxsteps=maxsteps)
        return img/float(samples)
    
    def color_mix_image_samples_mp(self,samples,maxsteps = 5,n_processors = 4):
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        with Pool(n_processors) as p:
            imgs = np.array(p.map(mp_color_mix_image, [copy.copy(self) for i in range(samples)]))
        img = np.mean(imgs,0)
        return img

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
    
    def normal_image(self):
        img = np.full([self.camera.ny,self.camera.nx,3],np.inf,dtype=float)
        time_img = np.full([self.camera.ny,self.camera.nx],np.inf)
        for ray, x, y in self.camera.iterate_rays():
            for ob in self.objects:
                intersect, t, normal = ob.ray_intersect_time_normal(ray)
                if np.isnan(t):
                    pass
                elif t < time_img[y,x]:
                    img[y,x,:] = np.abs(normal)
                    time_img[y,x] = t
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
        img = np.zeros([self.camera.ny,self.camera.nx,3]).astype(float)
        for ray, x, y in self.camera.iterate_rays():
            ob,_,_,_ = self.object_hit(ray)
            if ob != -1:
                img[y,x,:] = self.objects[ob].reflectance
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
    
def mp_color_mix_image(scene):
    return scene.color_mixing_image()

def mp_path_trace(scene):
    return scene.path_image()

def mp_path_trace_save(scene_num):
    scene = scene_num[0]
    num = scene_num[1]
    img = scene.path_image()
    filename = "data/sample" + str(num) + ".npy"
    np.save(filename,img)
