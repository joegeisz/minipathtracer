import glob
import numpy as np
import matplotlib.pyplot as plt 


if __name__ == '__main__':
    x = 125
    y = 125
    samples = glob.glob("data1/*.npy")
    Rvals = []
    Gvals = []
    Bvals = []
    Rtot = 0
    Ravs = []
    for i, sample in enumerate(samples):
        img = np.load(sample)
        color = img[x,y,:]
        Rvals.append(color[0])
        Gvals.append(color[1])
        Bvals.append(color[2])
        Rtot += color[0]
        Ravs.append(Rtot/(i+1.0))
    fig = plt.figure("Red Radiance at pixel (125,125) by Sample")
    plt.title("Red Radiance at pixel (125,125) by Sample")
    plt.xlabel("Sample number")
    plt.ylabel("Radiance Value")
    plt.plot(Rvals,'r.')
    fig = plt.figure()
    plt.title("Histogram of Red Radiance Values at pixel (125,125)")
    plt.xlabel("Number of Samples")
    plt.ylabel("Bin Value")
    plt.hist(Rvals,bins=10,color="Red")
    fig = plt.figure()
    plt.title("Running Average of Red Radiance Values at Pixel (125,125)")
    plt.xlabel("Number of Samples Averaged")
    plt.ylabel("Average Radiance Value")
    plt.plot(Ravs,color = "Red")
    plt.show()
    
        






