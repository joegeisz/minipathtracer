from Scene import *
from SpecialObjects import *
from Primatives import *
import matplotlib.pyplot as plt 
import time

if __name__ == '__main__':
    plane = Plane([0,0,1],0, material_color = [1,0,0],reflectance = [1,1,1],emmitance = [0,0,0])
    s1 = Sphere([10,10,2],2, material_color=[1,0,0],reflectance = [1.0,0.9,0.9], emmitance = [1,1,1])
    s2 = Sphere([7,10,1],1, material_color = [1,0,0],reflectance = [0,0,1], emmitance = [0,0,0])
    s3 = Sphere([10,7,0.5],0.5, material_color = [1,0,0],reflectance = [0,1,0], emmitance = [0,0,0])
    cam = Camera([0,0,5],[10,10,2],256,256,0.5)
    layout = Scene([s1,s2,s3,plane],cam)
    #layout = Scene([plane],cam)
    # imgs = layout.object_images()
    # for img in imgs:
    #     plt.figure()
    #     plt.imshow(img)
    # print(np.array(imgs).shape)
    # plt.figure()
    # t1 = time.time()
    # im1 = layout.color_mix_image_samples(30,5)
    # print("non-mp: ",time.time()-t1)
    # plt.imshow(im1)

    # plt.figure()
    # t1 = time.time()
    # im2 = layout.color_mix_image_samples_mp(100,5,n_processors=6)
    # print("mp: ",time.time()-t1)
    # plt.imshow(im2)

    plt.figure()
    plt.imshow(layout.path_trace_image(14,n_processors=7))


    # plt.figure()
    # plt.imshow(layout.path_image())

    plt.figure()
    plt.imshow(layout.normal_image())
    # plt.figure()
    # plt.imshow(np.min(np.array(imgs),axis=0))
    # plt.figure()
    # plt.imshow(np.min(np.array(imgs),axis=0)-imgs[0])
    # fig1 = plt.figure()
    # plt.imshow(layout.intersection_image())
    # fig2 = plt.figure()
    # plt.imshow(np.log(layout.time_image()))
    # fig3 = plt.figure()
    # plt.imshow(layout.object_image())
    # fig4 = plt.figure()
    # img = layout.dist_image()
    # plt.imshow(20*img/np.max(np.ma.masked_invalid(img)))
    plt.show()


