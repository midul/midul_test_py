import nltk
import time
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re,sys,string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def unique_list(l):
    temp_unique_list = []
    [temp_unique_list.append(x) for x in l if x not in temp_unique_list]
    return temp_unique_list


if __name__ == '__main__':
    my_list = [""]
    my_list2 = [""]
    sid = SentimentIntensityAnalyzer()
    file_1 = str(sys.argv[1])
    file_2 = str(sys.argv[2])
    with open(file_1) as f_in:
        lines = (line.rstrip() for line in f_in)  # All lines including the blank ones
        #lines = (line for line in lines if line)  # Non-blank lines
        file_test = open(file_2, 'w')
        for line in lines:
            resp_dict = json.loads(line)
            if 'text' in resp_dict:
                line = resp_dict['text']
                ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", line).split())
                id = resp_dict['id']
                lati = resp_dict['latitude']
                longi = resp_dict['longitude']
                timestamp = resp_dict['timestamp']
                data = line
                data = data.lower()
                stopWords = stopwords.words('english')
                additional_stopwords = """, ! $ # & * : ) ( [ ] ; 👍 🎮 """
                stopWords += additional_stopwords.split()
                words = word_tokenize(data)
                wordsFiltered = []
                for w in words:
                    if w not in stopWords:
                        wordsFiltered.append(w)

                while "rt" in wordsFiltered:
                    index_RT = wordsFiltered.index("rt")
                    del wordsFiltered[index_RT:index_RT+4]
                while "@" in wordsFiltered:
                    index_RT = wordsFiltered.index("@")
                    del wordsFiltered[index_RT:index_RT+2]
                while "https" in wordsFiltered:
                    index_RT = wordsFiltered.index("https")
                    del wordsFiltered[index_RT:index_RT+3]
                while "#" in wordsFiltered:
                    index_RT = wordsFiltered.index("#")
                    del wordsFiltered[index_RT:index_RT+1]
                line = " ".join(wordsFiltered)
                line = ' '.join(unique_list(line.split()))

                line = line.replace(".", "")
                line = line.replace("…", "")
                line = line.replace(",", "")
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                wordsFiltered = line.split()
                ss = sid.polarity_scores(line)
                score = ss['compound'];
                if -0.3 < score < 0.3:
                    score = 0
                elif score > 0.3:
                    score = 1
                else:
                    score = -1

                line2 = str(id) + "," + str(score) + "," + str(lati) + "," + str(longi) + "," + str(timestamp)
                file_test.write(line2)
                file_test.write('\n')
                my_list2.append(line2)
                my_list.append(line)

    print(my_list2)

    file_test.close()
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sentences = [""]
    paragraph = ""
    from nltk import tokenize

    lines_list = tokenize.sent_tokenize(paragraph)
    sentences.extend(lines_list)
    tricky_sentences = [""]
    sentences.extend(my_list)
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print()