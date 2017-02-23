import os
import shutil
import json
import random

def main():
    labels_dict = dict()
    with open("selected.20151117_1_id-labels.txt", "r") as f:
        for idx, line in enumerate(f):
            items = line.rstrip().split('\t')
            original_id, label = items
            labels_dict[original_id] = label

    with open("selected.20151117_1_labeled.txt", "w") as output:
        with open("selected.20151117_1.txt", "r") as f:
            for idx, line in enumerate(f):
                tweet = json.loads(line)
                tweet_id = str(tweet["original_id"])
                tweet["manual_label"] = labels_dict[tweet_id]
                output.write("{0}\n".format(
                        json.dumps(tweet)
                    )
                )


if __name__ == '__main__':
    main()
