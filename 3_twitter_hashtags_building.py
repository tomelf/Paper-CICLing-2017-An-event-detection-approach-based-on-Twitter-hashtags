# Step 3: build unigram array for hashtags #

import json
import os

def main():
    file_dir = "preprocessed_must_contain_location"
    time_dirs = [d for d in os.listdir(file_dir) if d.startswith("2015")]
    time_dirs.sort()

    for time_dir in time_dirs:
        src_dir = os.path.join(file_dir, time_dir)

        filenames = os.listdir(src_dir)
        filenames.sort()

        all_hashtags = dict()

        for filename in filenames:
            if filename.startswith("preprocessed"):
                with open(os.path.join(src_dir, filename), 'r') as f:
                    print "Process file {0}...".format(filename)

                    for idx, line in enumerate(f):
                        if (idx+1)%1000 == 0:
                            print "== Process record {0:d}...".format(idx+1)
                        tweet = json.loads(line)

                        hashtags = tweet["hashtags"]
                        text = tweet["filtered_text"]

                        for hashtag in hashtags:
                            # first dict: word features; second dict: hashtag features
                            if hashtag not in all_hashtags.keys():
                                all_hashtags[hashtag] = [dict(), dict(), 1]
                            else:
                                all_hashtags[hashtag][2] += 1

                            other_hashtags = list(set(hashtags) - set([hashtag]))
                            for other_hashtag in other_hashtags:
                                if other_hashtag not in all_hashtags[hashtag][1].keys():
                                    all_hashtags[hashtag][1][other_hashtag] = 1
                                else:
                                    all_hashtags[hashtag][1][other_hashtag] += 1


                        words = text.split()
                        for word in words:
                            for hashtag in hashtags:
                                if word not in all_hashtags[hashtag][0].keys():
                                    all_hashtags[hashtag][0][word] = 1
                                else:
                                    all_hashtags[hashtag][0][word] += 1

        out_dir = os.path.join("features", time_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(os.path.join(out_dir, "all_hashtags.json"), 'w') as output:
            for hashtag in all_hashtags.keys():
                output.write("{0}\n".format(
                        json.dumps(
                            {'hashtag': hashtag, 'num_post': all_hashtags[hashtag][2], 'words': all_hashtags[hashtag][0], 'other_hashtags': all_hashtags[hashtag][1]},
                            sort_keys=True
                        )
                    )
                )



if __name__ == '__main__':
    main()
