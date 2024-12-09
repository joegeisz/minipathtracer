import glob
import numpy as np
import matplotlib.pyplot as plt 


if __name__ == '__main__':
    samples = glob.glob("data1/*.npy")
    img = np.zeros_like(np.load(samples[0]))
    views = [1,10,100,1000]
    for i, sample in enumerate(samples):
        img = img + np.load(sample)
        if i+1 in views:
            fig = plt.figure(str(i+1) + " samples",figsize=(10,10))
            plt.imshow(img/(i+1.0))
            fig.savefig("figures/"+str(i+1)+"_samples.jpg")
            plt.show()






