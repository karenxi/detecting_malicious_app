import json
import fastcluster
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import pdist

import sys # Provide code for both Python 2 and Python 3
if sys.hexversion < 0x03000000:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen
#f = urlopen('http://scipy-cluster.googlecode.com/svn/trunk/hcluster'
            #'/tests/iris.txt')

#X = np.loadtxt(f)
f = open("col_matrix.txt")
X = np.loadtxt(f)
f.close()
'''
f = open('col_matrix.json')
X = json.load(f)
'''
N = len(X)


#Since we have 807 apps, we choose 280 below to make sure 280 * 3 > 807, otherwise it will lead to the threshold problem
classes = ['g'] * 280 + ['r'] * 280 + ['c'] * 280 

def plot_with_labels(Z, num_clust):
    # plot the dendrogram
    threshold = Z[-num_clust + 1, 2]
    dg = dendrogram(Z, no_labels = True, color_threshold = threshold)
    # plot color bars under the leaves
    color = [classes[k] for k in dg['leaves']]
    b = .1 * Z[-1, 2]
    plt.bar(np.arange(N) * 10, np.ones(N) * b, bottom = -b, width = 10,
            color = color, edgecolor = 'none')
    plt.gca().set_ylim((-b, None))
    plt.show()

#Z = fastcluster.linkage(X, method = 'single')
#plot_with_labels(Z, 2)

#D = pdist(X, metric = 'cityblock')
Z = fastcluster.linkage(X, method = 'weighted')

#the 2nd parameter 1.5*X is the threshold we choose to apply when forming flat clusters, the bigger the threshold, the less the clusters
ind = sch.fcluster(Z, 1.5*X.max(), 'distance') 
print ind
plot_with_labels(Z, 3)
