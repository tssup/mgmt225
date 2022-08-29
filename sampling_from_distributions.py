from random import sample
import numpy as np 
import seaborn as sb
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



def sample_generator(i):
    n_bins = 80
    #sample = np.random.normal(loc = float(sys.argv[1]), scale = float(sys.argv[2]), size = (1000,))
    #sample = np.random.choice([40, 20, 80], p = [0.4, 0.1, 0.5], size=(1000,))
    
    #dice
    sample = np.random.choice([1,2,3,4], p = [0.25, 0.25, 0.25, 0.25], size=(100000,))
    plt.subplot(1,2,1)
    plt.cla()
    sb.histplot(sample)
    
    plt.subplot(1,2,2)
    plt.cla()
    sb.distplot(sample, hist = False)
  
  

if __name__ == '__main__':
    fig = plt.figure()
    #fig.set_size_inches(5,5)
    ani = FuncAnimation(fig, sample_generator, interval = 4000)
    plt.show()
    






    