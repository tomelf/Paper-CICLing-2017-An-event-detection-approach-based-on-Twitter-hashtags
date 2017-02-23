import os
import shutil
import json
import random

def main():
    folder = "clusters_kmeans/20151117_1/hashtag_170_word_7185"
    cluster_filenames = os.listdir(folder)
    hashtag_cluster_dict = dict()
    for cluster_filename in cluster_filenames:
        if cluster_filename.startswith("hashtag_cluster"):
            items = cluster_filename.split('.')[0].split("_")
            cluster_id = items[-1]
            hashtag_cluster_dict[cluster_id] = dict()
            with open(os.path.join(folder, cluster_filename), "r") as f:
                for idx, line in enumerate(f):
                    items = line.rstrip().split("\t")
                    h_id, h_text = items
                    hashtag_cluster_dict[cluster_id][h_text] = h_id

    cluster_ids = hashtag_cluster_dict.keys()
    cluster_ids.sort()
    with open("selected.20151117_1_labeled_kmeansCluster.txt", "w") as output:
        with open("selected.20151117_1_labeled.txt", "r") as f:
            for idx, line in enumerate(f):
                tweet = json.loads(line)
                hashtags = tweet["hashtags"]
                hashtag_clusters = []
                for hashtag in hashtags:
                    for cluster_id in cluster_ids:
                        if hashtag in hashtag_cluster_dict[cluster_id]:
                            hashtag_clusters.append(cluster_id)

                tweet["kmeans_clusters"] = hashtag_clusters
                output.write("{0}\n".format(
                        json.dumps(tweet)
                    )
                )


    folder = "clusters_streamcubes/20151117_1/hashtag_170_word_7185"
    cluster_filenames = os.listdir(folder)
    hashtag_cluster_dict = dict()
    for cluster_filename in cluster_filenames:
        if cluster_filename.startswith("hashtag_cluster"):
            items = cluster_filename.split('.')[0].split("_")
            cluster_id = items[-1]
            hashtag_cluster_dict[cluster_id] = dict()
            with open(os.path.join(folder, cluster_filename), "r") as f:
                for idx, line in enumerate(f):
                    items = line.rstrip().split("\t")
                    h_id, h_text = items
                    hashtag_cluster_dict[cluster_id][h_text] = h_id

    cluster_ids = hashtag_cluster_dict.keys()
    cluster_ids.sort()
    with open("selected.20151117_1_labeled_streamcubesCluster.txt", "w") as output:
        with open("selected.20151117_1_labeled.txt", "r") as f:
            for idx, line in enumerate(f):
                tweet = json.loads(line)
                hashtags = tweet["hashtags"]
                hashtag_clusters = []
                for hashtag in hashtags:
                    for cluster_id in cluster_ids:
                        if hashtag in hashtag_cluster_dict[cluster_id]:
                            hashtag_clusters.append(cluster_id)

                tweet["streamcubes_clusters"] = hashtag_clusters
                output.write("{0}\n".format(
                        json.dumps(tweet)
                    )
                )


if __name__ == '__main__':
    main()
