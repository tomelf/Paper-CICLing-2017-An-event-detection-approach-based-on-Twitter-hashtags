# Step 5: streamcubes clustering #

import sys
import json
import os
import numpy as np
import math
from copy import copy
from operator import add
from numpy.linalg import norm
from scipy import spatial

alpha = 0.5
beta = 0.5

def cosine_distance(u, v):
    if norm(u) == 0 or norm(v) == 0:
        return 0
    return spatial.distance.cosine(u, v)

def distance(u, v):
    u_word_vec = u[1:1+num_words]
    v_word_vec = v[1:1+num_words]
    u_hashtag_vec = u[-1*num_hashtags:]
    v_hashtag_vec = v[-1*num_hashtags:]
    return alpha * cosine_distance(u_word_vec, v_word_vec) + beta * cosine_distance(u_hashtag_vec, v_hashtag_vec)

def hashtag_cluster_static(E, h):
    # e = nearest-neighbor(E, h)
    nearest_index = nearest_neighbor(E, h)
    if nearest_index:
        e_vec, e_hashtags = E[nearest_index]
        dis_h = distance(e_vec, h)
        # The minimum threshold for event e is the
        # nearest distance between e and any other clusters
        e_threshold = min([distance(e_vec, e_other[0]) for idx, e_other in enumerate(E) if idx <> nearest_index])
        if dis_h > e_threshold:
            # add h to E as a new event
            new_e_vec = copy(h)
            new_e_hashtags = [h]
            E.append([new_e_vec, new_e_hashtags])
        else:
            # add h to the existing event e
            e_vec = map(add, e_vec, h)
            e_hashtags.append(h)
    else:
        new_e_vec = copy(h)
        new_e_hashtags = [h]
        E.append([new_e_vec, new_e_hashtags])
    return E

def nearest_neighbor(E, h):
    if len(E) == 0:
        return None
    min_index = 0
    min_distance = 1
    for idx, e in enumerate(E):
        dis = distance(h, e[0])
        if dis < min_distance:
            min_distance = dis
            min_index = idx
    return min_index

def hashtag_cluster_static_ex(E, e):
    nearest_index = nearest_neighbor_ex(E, e)
    if nearest_index:
        e_vec, e_hashtags = E[nearest_index]
        e_vec_2, e_hashtags_2 = e
        dis_e = distance(e_vec, e_vec_2)
        # The minimum threshold for event e is the
        # nearest distance between e and any other clusters
        e_threshold = min([distance(e_vec, e_other[0]) for idx, e_other in enumerate(E) if idx <> nearest_index])
        if dis_e > e_threshold:
            E.append(e)
        else:
            # absorb
            e_vec = map(add, e_vec, e_vec_2)
            e_hashtags += e_hashtags_2
    else:
        E.append(e)

    return E

def nearest_neighbor_ex(E, e_target):
    if len(E) == 0:
        return None
    min_index = 0
    min_distance = 1
    for idx, e in enumerate(E):
        e_target_vec, e_target_hashtags = e_target
        e_vec, e_hashtags = e
        dis = distance(e_target_vec, e_vec)
        if dis < min_distance:
            min_distance = dis
            min_index = idx
    return min_index

def main():
    global num_hashtags
    global num_words

    src_dir = "features"
    time_dirs = [d for d in os.listdir(src_dir) if d.startswith("2015")]
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

            print "Start clustering..."
            clusters = []
            for idx, vec in enumerate(vec_features):
                clusters = hashtag_cluster_static(clusters, vec)

            # add a check point to re-clustering for small events
            curr_iter = 0
            max_iter = 1
            while curr_iter < max_iter:
                curr_iter += 1
                ori_count = len(clusters)
                for i in range(ori_count):
                    if len(clusters) <= 1:
                        break
                    c = clusters.pop(0)
                    clusters = hashtag_cluster_static_ex(clusters, c)
                # converge
                if ori_count == len(clusters):
                    break

            print "Finish clustering..."

            print "Write hashtag clusters to files..."

            clusters_dir = "clusters_streamcubes/{0}/hashtag_{1:d}_word_{2:d}".format(time_dir, num_hashtags, num_words)
            if not os.path.exists(clusters_dir):
                os.makedirs(clusters_dir)

            hashtag_dict = dict()

            for idx, cluster in enumerate(clusters):
                with open(os.path.join(clusters_dir, "hashtag_cluster_{0:d}.txt".format(idx)), "w") as output:
                    vec, hashtags = cluster
                    for hashtag_obj in hashtags:
                        hashtag_id = hashtag_obj[0]
                        hashtag = all_hashtags[hashtag_id]
                        output.write(u"{0:d}\t".format(hashtag_id))
                        output.write(hashtag.encode('UTF-8'))
                        output.write(u"\n")
                        hashtag_dict[hashtag_id] = idx

            with open(os.path.join(clusters_dir, "all_hashtags.txt"), "w") as output:
                # num of clusters
                output.write(u"{0:d}\n".format(len(clusters)))

                for idx, hashtag in enumerate(all_hashtags):
                    output.write(u"{0:d}\t".format(idx))
                    output.write(hashtag.encode('UTF-8'))
                    output.write(u"\t{0:d}\n".format(hashtag_dict[idx]))

            print "==================="

        print "Done!"

if __name__ == '__main__':
    main()
