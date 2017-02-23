# Step 4: build hashtag-hashtag features #

import json
import os
import operator

def main():
    src_dir = "features"
    time_dirs = [d for d in os.listdir(src_dir) if d.startswith("2015")]
    for time_dir in time_dirs:
        print "processing folder: {0}".format(time_dir)

        hashtag_objs = []
        all_hashtags = []

        features_dir = os.path.join("features", time_dir)

        with open(os.path.join(features_dir, "all_hashtags.json"), 'r') as f:
            for idx, line in enumerate(f):
                hashtag = json.loads(line)
                num_post = int(hashtag["num_post"])
                if num_post <= 3:
                    continue

                hashtag_objs.append(hashtag)
                all_hashtags.append(hashtag["hashtag"])

        all_hashtags.sort()

        with open(os.path.join(features_dir, "features_hashtags_with_other_hashtags_{0:d}_list.json".format(len(all_hashtags))), 'w') as output:
            output.write("{0}\n".format(
                    json.dumps(
                        {'hashtags': all_hashtags}
                    )
                )
            )

        with open(os.path.join(features_dir, "features_hashtags_with_other_hashtags_{0:d}.json".format(len(all_hashtags))), 'w') as output:
            for hashtag_obj in hashtag_objs:
                other_hashtags = dict()
                for h in all_hashtags:
                    other_hashtags[h] = 0
                for h in hashtag_obj["other_hashtags"].keys():
                    if h in other_hashtags:
                        other_hashtags[h] = hashtag_obj["other_hashtags"][h]

                features = []
                for h in all_hashtags:
                    features.append(other_hashtags[h])

                output.write("{0}\n".format(
                        json.dumps(
                            {'hashtag': hashtag_obj["hashtag"], 'features': features}
                        )
                    )
                )

if __name__ == '__main__':
    main()
