# Step 4: build hashtag-unigram features #

import json
import os
import operator

def main():
    src_dir = "features"
    time_dirs = [d for d in os.listdir(src_dir) if d.startswith("2015")]
    for time_dir in time_dirs:
        print "processing folder: {0}".format(time_dir)

        features_dir = os.path.join("features", time_dir)

        all_words_list = None
        with open(os.path.join(features_dir, "all_words.json"), 'r') as f:
            for idx, line in enumerate(f):
                all_words_list = json.loads(line)
                break

        len_all_words = len(all_words_list)
        first_ns = [
            len_all_words
        ]

        for first_n in first_ns:
            all_words = dict()
            export_data = []

            for idx, word in enumerate(all_words_list):
                if idx >= first_n:
                    break
                all_words[word[0]] = word[1]

            with open(os.path.join(features_dir, "all_hashtags.json"), 'r') as f:
                for idx, line in enumerate(f):
                    hashtag = json.loads(line)
                    num_post = int(hashtag["num_post"])
                    if num_post <= 3:
                        continue

                    hashtag_text = hashtag["hashtag"]
                    hashtag_words = hashtag["words"]

                    # Remove words that are not in feature words list
                    tmp_list = list(set(hashtag_words.keys()) - set(all_words.keys()))
                    for tmp_word in tmp_list:
                        hashtag_words.pop(tmp_word, None)
                    # Add feature words that the target hashtag did not have
                    tmp_list = list(set(all_words.keys()) - set(hashtag_words.keys()))
                    for tmp_word in tmp_list:
                        hashtag_words[tmp_word] = 0

                    export_data.append([hashtag_text, hashtag_words])

            all_words_keys = all_words.keys()
            all_words_keys.sort()

            with open(os.path.join(features_dir, "features_hashtags_with_words_{0:d}_list.json".format(first_n)), 'w') as output:
                output.write("{0}\n".format(
                        json.dumps(
                            {'hashtags': all_words_keys}
                        )
                    )
                )

            with open(os.path.join(features_dir, "features_hashtags_with_words_{0:d}.json".format(first_n)), 'w') as output:
                for data in export_data:
                    features = []
                    for word_key in all_words_keys:
                        features.append(data[1][word_key])
                    output.write("{0}\n".format(
                            json.dumps(
                                {'hashtag': data[0], 'features': features}
                            )
                        )
                    )

            print "the number of hashtags: {0:d}, unigram features: {1:d}".format(len(export_data), first_n)

if __name__ == '__main__':
    main()
