# Step 5: k-kmeans clustering #

import sys
import json
import os
import operator
import numpy
import math
from copy import copy
from numpy.linalg import norm
from scipy import spatial
from nltk.cluster import KMeansClusterer

alpha = 0.5
beta = 0.5
default_num_K = 12

# To enable this config, run the streamcubes clustering first
is_dynamic_K = True

def cosine_distance(u, v):
    if norm(u) == 0 or norm(v) == 0:
        return 0
    return spatial.distance.cosine(u, v)

def hashtag_distance(u, v):
    u_word_vec = u[1:1+num_words]
    v_word_vec = v[1:1+num_words]
    u_hashtag_vec = u[-1*num_hashtags:]
    v_hashtag_vec = v[-1*num_hashtags:]

    distance = alpha * cosine_distance(u_word_vec, v_word_vec) + beta * cosine_distance(u_hashtag_vec, v_hashtag_vec)
    return distance

def main():
    global num_hashtags
    global num_words

    src_dir = "features"
    time_dirs = [d for d in os.listdir(src_dir) if d.startswith("2015")]

    num_clusters_list = []
    if is_dynamic_K:
        for time_dir in time_dirs:
            streamcubes_dir = "clusters_streamcubes"
            streamcubes_time_dir = os.path.join(streamcubes_dir, time_dir)
            clusters_dirs = [d for d in os.listdir(streamcubes_time_dir) if d.startswith("hashtag")]

            for clusters_dir in clusters_dirs:
                streamcubes_full_dir = os.path.join(streamcubes_time_dir, clusters_dir)
                streamcubes_hashtag_results = []

                with open(os.path.join(streamcubes_full_dir, "all_hashtags.txt"), 'r') as f:
                    for idx, line in enumerate(f):
                        if idx == 0:
                            num_clusters_list.append(int(line.strip()))
                            break

    for time_dir in time_dirs:
        print "processing folder: {0}".format(time_dir)

        hashtag_features = dict()
        all_hashtags = []

        features_dir = os.path.join("features", time_dir)

        print "Load hashtags..."
        with open(os.path.join(features_dir, "all_hashtags.json"), 'r') as f:
            for idx, line in enumerate(f):
                hashtag = json.loads(line)
                num_post = int(hashtag["num_post"])
                if num_post <= 3:
                    continue
                all_hashtags.append(hashtag["hashtag"])
        num_hashtags = len(all_hashtags)

        all_words_list = None
        with open(os.path.join(features_dir, "all_words.json"), 'r') as f:
            for idx, line in enumerate(f):
                all_words_list = json.loads(line)
                break

        len_all_words = len(all_words_list)
        num_words_list = [
            len_all_words
        ]

        print "Load hashtag features..."
        with open(os.path.join(features_dir, "features_hashtags_with_other_hashtags_{0:d}.json".format(num_hashtags)), "r") as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                hashtag_features[data["hashtag"]] = data["features"]

        for num_words in num_words_list:
            print "Start processing hashtag_{0:d}_word_{1:d} ...".format(num_hashtags, num_words)

            word_features = dict()

            print "Load unigram features..."
            with open(os.path.join(features_dir, "features_hashtags_with_words_{0:d}.json".format(num_words)), "r") as f:
                for idx, line in enumerate(f):
                    data = json.loads(line)
                    word_features[data["hashtag"]] = data["features"]

            vec_features = []
            for idx, hashtag in enumerate(all_hashtags):
                vec_feature = [idx]
                vec_feature += word_features[hashtag]
                vec_feature += hashtag_features[hashtag]
                vec_features.append(vec_feature)
                # if idx >= 200:
                #     break

            vectors = [numpy.array(f) for f in vec_features]

            print "Start clustering..."
            # decide the K for K-means
            num_clusters = default_num_K
            if is_dynamic_K:
                num_clusters = num_clusters_list.pop(0)

            init_means=[copy(vectors[i]) for i in range(num_clusters)]
            clusterer = KMeansClusterer(num_clusters, hashtag_distance,
                initial_means=init_means, avoid_empty_clusters=True)
            clusters = clusterer.cluster(vectors, True)
            print "Finish clustering..."
            # print('Clustered:', vectors)
            # print('As:', clusters)
            # print('Means:', clusterer.means())

            print "Write hashtag clusters to files..."
            hashtag_clusters = [[] for i in range(num_clusters)]
            for i in range(len(clusters)):
                hashtag_clusters[clusters[i]].append(vectors[i][0])

            clusters_dir = "clusters_kmeans/{0}/hashtag_{1:d}_word_{2:d}".format(time_dir, num_hashtags, num_words)
            if not os.path.exists(clusters_dir):
                os.makedirs(clusters_dir)

            hashtag_dict = dict()
            for idx, cluster in enumerate(hashtag_clusters):
                with open(os.path.join(clusters_dir, "hashtag_cluster_{0:d}.txt".format(idx)), "w") as output:
                    for hashtag_id in cluster:
                        hashtag = all_hashtags[hashtag_id]
                        output.write(u"{0:d}\t".format(hashtag_id))
                        output.write(hashtag.encode('UTF-8'))
                        output.write(u"\n")

                        hashtag_dict[hashtag_id] = idx

            with open(os.path.join(clusters_dir, "all_hashtags.txt"), "w") as output:
                # num of clusters
                output.write(u"{0:d}\n".format(num_clusters))

                for idx, hashtag in enumerate(all_hashtags):
                    output.write(u"{0:d}\t".format(idx))
                    output.write(hashtag.encode('UTF-8'))
                    output.write(u"\t{0:d}\n".format(hashtag_dict[idx]))

            print "==================="

        print "Done!"


if __name__ == '__main__':
    main()
