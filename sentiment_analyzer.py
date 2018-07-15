import json
import re
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator


# identify the list of unique words in line
def unique_list(l):
    temp_unique_list = []
    [temp_unique_list.append(x) for x in l if x not in temp_unique_list]
    return temp_unique_list


if __name__ == '__main__':
    sid = SentimentIntensityAnalyzer()
    translator = Translator()
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    file_test = open(output_file, 'w')
    f_in = open(input_file)
    # input file should have non blank lines
    lines = (line.rstrip() for line in f_in)
    for line in lines:
        resp_dict = json.loads(line)
        if 'text' in resp_dict:
            line = resp_dict['text']
            temp_unique_id = resp_dict['id']
            latitude = resp_dict['latitude']
            longitude = resp_dict['longitude']
            timestamp = resp_dict['timestamp']
            line = line.lower()
            stopWords = stopwords.words('english')
            additional_stopwords = """, ! $ # & * : ) ( [ ] ; 👍 🎮 ` . ' """
            stopWords += additional_stopwords.split()
            words = word_tokenize(line)
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
            line = ' '.join(unique_list(wordsFiltered))
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            # vader sentiment analyzer
            ss = sid.polarity_scores(line)
            # converting to absolute values
            score = ss['compound']
            if -0.3 < score < 0.3:
                score = 0
            elif score > 0.3:
                score = 1
            else:
                score = -1
            line = str(temp_unique_id) + "," + str(score) + "," + str(latitude) + \
                    "," + str(longitude) + "," + str(timestamp)
            file_test.write(line)
            file_test.write('\n')

    file_test.close()
    f_in.close()