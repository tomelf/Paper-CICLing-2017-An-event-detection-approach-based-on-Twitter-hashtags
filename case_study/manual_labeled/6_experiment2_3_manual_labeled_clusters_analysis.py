import numpy as np
import os
from sklearn import metrics
import shutil
import json
import random
from collections import Counter

def purity_score(clusters_list, classes_list):
    clusters = np.array(clusters_list)
    classes = np.array(classes_list)
    A = np.c_[(clusters,classes)]
    n_accurate = 0.
    for j in np.unique(A[:,0]):
        z = A[A[:,0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])
    return n_accurate / A.shape[0]

def nmi_score(labels_true, labels_pred):
    return metrics.normalized_mutual_info_score(labels_true, labels_pred)


def main():
    label_occurrence_in_clusters = dict()
    filename = "selected.20151117_1_labeled_kmeansCluster.txt"
    label_list = []
    cluster_list = []
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            tweet = json.loads(line)
            manual_label = tweet["manual_label"]
            clusters = tweet["kmeans_clusters"]

            for cluster in clusters:
                label_list.append(int(manual_label))
                cluster_list.append(int(cluster))

    print "Results of Kmeans:"
    print "  Purity: {0:f}".format(purity_score(cluster_list, label_list))
    print "  NMI: {0:f}".format(nmi_score(label_list, cluster_list))




    label_occurrence_in_clusters = dict()
    filename = "selected.20151117_1_labeled_streamcubesCluster.txt"
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            tweet = json.loads(line)
            manual_label = tweet["manual_label"]
            clusters = tweet["streamcubes_clusters"]

            for cluster in clusters:
                label_list.append(int(manual_label))
                cluster_list.append(int(cluster))

    print "Results of StreamCubes:"
    print "  Purity: {0:f}".format(purity_score(cluster_list, label_list))
    print "  NMI: {0:f}".format(nmi_score(label_list, cluster_list))



if __name__ == '__main__':
    main()
