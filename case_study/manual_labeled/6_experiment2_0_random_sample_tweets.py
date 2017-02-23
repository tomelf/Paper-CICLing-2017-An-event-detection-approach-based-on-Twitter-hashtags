import os
import shutil
import json
import random

def main():
    num_samples = 200
    src_folder = "preprocessed_must_contain_location"
    folders = os.listdir(src_folder)

    for folder in folders:
        if folder.startswith("2015"):
            tweets = dict()
            full_path = os.path.join(src_folder, folder)
            filepaths = os.listdir(full_path)

            for filepath in filepaths:
                with open(os.path.join(full_path, filepath), "r") as f:
                    for idx, line in enumerate(f):
                        tweet = json.loads(line)
                        hashtags = tweet["hashtags"]
                        if len(hashtags) > 0:
                            tweets[tweet["original_id"]] = line

            random_ids = random.sample(tweets.keys(), num_samples)
            with open("selected.content.{0}.txt".format(folder), "w") as output:
                for idx, random_id in enumerate(random_ids):
                    obj = json.loads(tweets[random_id])
                    content = u"{0}".format(obj["original_text"]).encode('utf-8').strip()
                    output.write("{0:d} ======================\n\n".format(idx+1))
                    output.write(content)
                    output.write("\n\n")
            with open("selected.{0}.txt".format(folder), "w") as output:
                for random_id in random_ids:
                    output.write(tweets[random_id])


if __name__ == '__main__':
    main()
