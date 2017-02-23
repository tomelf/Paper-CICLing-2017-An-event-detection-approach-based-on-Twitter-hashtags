# Step 6: cluster analysis #

import numpy as np
import os
from sklearn import metrics

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
    kmeans_dir = "clusters_kmeans"
    streamcubes_dir = "clusters_streamcubes"
    time_dirs = [d for d in os.listdir(kmeans_dir) if d.startswith("2015")]

    for time_dir in time_dirs:
        print "processing folder: {0}".format(time_dir)
        kmeans_time_dir = os.path.join(kmeans_dir, time_dir)
        streamcubes_time_dir = os.path.join(streamcubes_dir, time_dir)

        clusters_dirs = [d for d in os.listdir(kmeans_time_dir) if d.startswith("hashtag")]

        for clusters_dir in clusters_dirs:
            kmeans_full_dir = os.path.join(kmeans_time_dir, clusters_dir)
            streamcubes_full_dir = os.path.join(streamcubes_time_dir, clusters_dir)

            kmeans_hashtag_results = []
            streamcubes_hashtag_results = []

            print "Load hashtag clustering results..."

            kmeans_num_clusters = 0
            streamcubes_num_clusters = 0
            with open(os.path.join(kmeans_full_dir, "all_hashtags.txt"), 'r') as f:
                for idx, line in enumerate(f):
                    if idx == 0:
                        kmeans_num_clusters = int(line.strip())
                        continue
                    hashtag_id, hashtag_text, hashtag_cluster_id = line.rstrip().split('\t')
                    kmeans_hashtag_results.append(int(hashtag_cluster_id))

            with open(os.path.join(streamcubes_full_dir, "all_hashtags.txt"), 'r') as f:
                for idx, line in enumerate(f):
                    if idx == 0:
                        streamcubes_num_clusters = int(line.strip())
                        continue
                    hashtag_id, hashtag_text, hashtag_cluster_id = line.rstrip().split('\t')
                    streamcubes_hashtag_results.append(int(hashtag_cluster_id))

            print "Write analysis to files..."

            result_dir = "analysis/{0}/{1}".format(time_dir, clusters_dir)
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)

            with open(os.path.join(result_dir, "analysis.txt"), "w") as output:
                output.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
                        "kmeans_num_clusters",
                        "streamcubes_num_clusters",
                        "Purity(kmeans/streamcubes)",
                        "NMI(kmeans/streamcubes)",
                        "Purity(streamcubes/kmeans)",
                        "NMI(streamcubes/kmeans)"
                    )
                )
                output.write("{0:d}\t{1:d}\t{2:f}\t{3:f}\t{4:f}\t{5:f}\n".format(
                        kmeans_num_clusters,
                        streamcubes_num_clusters,
                        purity_score(kmeans_hashtag_results, streamcubes_hashtag_results),
                        nmi_score(kmeans_hashtag_results, streamcubes_hashtag_results),
                        purity_score(streamcubes_hashtag_results, kmeans_hashtag_results),
                        nmi_score(streamcubes_hashtag_results, kmeans_hashtag_results)
                    )
                )

            print "==================="

        print "Done!"

if __name__ == "__main__":
    main()
