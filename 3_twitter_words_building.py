# Step 3: build occurrances of all unigrams #

import json
import os
import operator

def main():
    file_dir = "preprocessed_must_contain_location"
    time_dirs = [d for d in os.listdir(file_dir) if d.startswith("2015")]
    time_dirs.sort()

    for time_dir in time_dirs:
        src_dir = os.path.join(file_dir, time_dir)

        filenames = os.listdir(src_dir)
        filenames.sort()

        all_words = dict()

        for filename in filenames:
            if filename.startswith("preprocessed"):
                with open(os.path.join(src_dir, filename), 'r') as f:
                    print "Process file {0}...".format(filename)

                    for idx, line in enumerate(f):
                        if (idx+1)%1000 == 0:
                            print "== Process record {0:d}...".format(idx+1)
                        tweet = json.loads(line)

                        text = tweet["filtered_text"]

                        words = text.split()
                        for word in words:
                            if word not in all_words.keys():
                                all_words[word] = 1
                            else:
                                all_words[word] += 1

        sorted_all_words = sorted(all_words.items(), key=operator.itemgetter(1))
        sorted_all_words.reverse()

        out_dir = os.path.join("features", time_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(os.path.join(out_dir, "all_words.json"), 'w') as output:
            output.write("{0}\n".format(
                    json.dumps(
                        sorted_all_words
                    )
                )
            )

if __name__ == '__main__':
    main()
