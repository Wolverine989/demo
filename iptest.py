from PIL import Image
import os.path
import os
from numpy import asarray
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode
from statistics import median
import math


im = Image.open(r"C:\Users\bisho\OneDrive\Desktop\gui\image1.JPG")
# Setting the points for cropped image
left = 212
top = 241
right = 380
bottom = 270
 

im = im.crop((left, top, right, bottom))
im = im.convert('L') 
im.show()
numpydata = asarray(im)
a_data = np.average(numpydata, axis=0)

for i in range(len(a_data)):
    a_data[i]=256-a_data[i]

    min_value = min(a_data)
    for i in range(len(a_data)):
        a_data[i] -= min_value
    a_data = slopefix(a_data) #fixx slope
    a_data = smooth(a_data) #smooothen

    #clip_value = 20
    clip_value = 10
    clip = [20 for i in range(len(a_data))]
    for i in range(len(a_data)):
        if a_data[i]>clip_value:
            clip[i] = 50

##
    dervi = [0 for i in range(len(clip))]
    for i in range(len(clip)):
        if i:
            dervi[i] = clip[i]-clip[i-1]
    get_indexes = lambda x, xs : [i for (y,i) in zip(xs, range(len(xs))) if x==y ]
    get_width = lambda x: str(float(5/300)*x)+" mm"

    max_ = max(dervi)
    max_c = dervi.count(max_)
    max_ = get_indexes(max_, dervi)

    if max_c == 1 :
        plt.plot(a_data)
        # plt.plot(clip, label = "clip at 20")
        # plt.plot(dervi, label ="der")
        # plt.plot(endu, label="final")

        # plt.plot(smooth(a_data))
        plt.legend()
        plt.show()
        print("one line only")
        #return False 

    min_ = min(dervi)
    min_c = dervi.count(min_)
    min_ = get_indexes(min_ , dervi)

    ## 300px = 5mm aprox
    w_c = min_[0]-max_[0]
    w_t = min_[1]-max_[1]

    w_c = get_width(w_c)
    w_t = get_width(w_t)

    print(w_c)
    print(w_t)

    dist = ((max_[1]+min_[1])/2) - ((max_[0]+min_[0])/2)
    dist = get_width(dist)

    print(dist)
    endu = [0 for i in range(len(a_data))]

    local_max_c = max(a_data[max_[0]: min_[0]])
    local_max_t = max(a_data[max_[1]: min_[1]])

    for i in range (max_[0],min_[0]):
        endu[i]= local_max_c
    for i in range (max_[1],min_[1]):
        endu[i]= local_max_t
    

    # x = [ i for i in range(len(a_data))]
    data_graph= im + "\n C  : " + w_c + "\n T  : " + w_t + "\n C-T : " + dist+ "\n "+ str(local_max_t)
    # plt.plot(a_data)
    plt.plot(a_data, label=data_graph)
    # plt.plot(clip, label = "clip at 20")
    # plt.plot(dervi, label ="der")
    plt.plot(endu, label="final")

    # plt.plot(smooth(a_data))
    plt.legend()
    plt.show()
    #return local_max_t

    def smooth(data):

        for i in range(20):
            for i in range(len(data)-1):
                if i:
                    avg = (data[i-1]+data[i+1])/2
                    data[i] += avg
                    data[i] /= 2

    # for i in range(len(data)): data[i]-=10

        return data

def slopefix(data):
    leng = len(data)
    left  = min(data[0:50])
    right = min(data[-50:-1])
    fixer = (left-right)/len(data)
    fixer = [i*fixer for i in range(len(data))]
    fixer.reverse()

    for i in range(len(data)):
        data[i] -= fixer[i]

    return data


