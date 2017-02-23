# Step 2: tweet preprocessing #

import json
import os
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def main():
    # load stopwords list
    cachedStopWords = stopwords.words("english")
    stemmer = PorterStemmer()

    in_dir = "tweets"
    out_dir = "preprocessed_must_contain_location"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    filelist = os.listdir(in_dir)
    for filepath in filelist:
        if filepath.startswith("2015"):
            with open(filepath, 'r') as f:
                print "Process file {0}...".format(filepath)
                with open(os.path.join(out_dir, 'preprocessed.'+filepath), 'a') as output:
                    for idx, line in enumerate(f):
                        if (idx+1)%1000 == 0:
                            print "== Process record {0:d}...".format(idx+1)
                        tweet = json.loads(line)

                        if "created_at" not in tweet.keys() or \
                            "geo" not in tweet.keys() or \
                            tweet["geo"] == None:
                            continue

                        export_tweet_id = tweet["id"]
                        export_origin_string = tweet["text"]
                        export_time = tweet["created_at"]
                        export_geo = tweet["geo"]

                        pos = []
                        hashtags = []
                        for hashtag in tweet["entities"]["hashtags"]:
                            hashtags.append(hashtag["text"])
                            pos.append([hashtag["indices"][0], hashtag["indices"][1]])
                        for url in tweet["entities"]["urls"]:
                            pos.append([url["indices"][0], url["indices"][1]])
                        for user_mention in tweet["entities"]["user_mentions"]:
                            pos.append([user_mention["indices"][0], user_mention["indices"][1]])
                        for symbol in tweet["entities"]["symbols"]:
                            pos.append([symbol["indices"][0], symbol["indices"][1]])

                        export_hashtags = hashtags

                        pos.sort()

                        # filter hashtags, urls, mentions, symbols
                        tmp_text = tweet["text"]
                        for i in range(len(pos)):
                            tmp_text_1 = tmp_text[0:pos[i][0]]
                            tmp_text_2 = tmp_text[pos[i][1]:]
                            tmp_text = tmp_text_1 + " "*(pos[i][1]-pos[i][0]) + tmp_text_2

                        # filter chars except words and numbers
                        tmp_text = re.sub(r'[^\w]', ' ', tmp_text)

                        # filter stopwords and perform Porter stemmer
                        tmp_text = ' '.join([stemmer.stem(word) for word in tmp_text.split() if word not in cachedStopWords])

                        # lowercase
                        export_string = tmp_text.lower()

                        # export filtered content
                        output.write("{0}\n".format(
                                json.dumps({'created_time': export_time, 'geo': export_geo,
                                    'hashtags': export_hashtags, 'filtered_text': export_string,
                                    'original_id': export_tweet_id, 'original_text': export_origin_string,
                                    }
                                )
                            )
                        )


if __name__ == '__main__':
    main()
