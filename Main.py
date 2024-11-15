from Scene import *
from SpecialObjects import *
from Primatives import *
import matplotlib.pyplot as plt 

plane = Plane([0,0,1],0)
s1 = Sphere([10,10,2],2)
s2 = Sphere([7,10,1],1)
cam = Camera([0,0,10],[10,10,2],300,150,1.5)
layout = Scene([plane,s1,s2],cam)
# imgs = layout.object_images()
# for img in imgs:
#     plt.figure()
#     plt.imshow(img)
# print(np.array(imgs).shape)
# plt.figure()
# plt.imshow(np.min(np.array(imgs),axis=0))
# plt.figure()
# plt.imshow(np.min(np.array(imgs),axis=0)-imgs[0])
# fig1 = plt.figure()
# plt.imshow(layout.intersection_image())
fig2 = plt.figure()
plt.imshow(np.log(layout.time_image()))
fig3 = plt.figure()
plt.imshow(layout.object_image())
# fig4 = plt.figure()
# img = layout.dist_image()
# plt.imshow(20*img/np.max(np.ma.masked_invalid(img)))
plt.show()


