# import nltk
import time
import json
import re,string



# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
#
# data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
# stopWords = set(stopwords.words('english'))
# words = word_tokenize(data)
# wordsFiltered = []
#
# for w in words:
#     if w not in stopWords:
#         wordsFiltered.append(w)
#
# print(wordsFiltered)

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


if __name__ == '__main__':
    logfile = open("C:/Users/midul/Documents/Twitter_Data/eoi/data_live.json","r")
    loglines = follow(logfile)

    f = open("C:/Users/midul/Documents/Twitter_Data/eoi/data_live_temp.json", "w+")
    with open("C:/Users/midul/Documents/Twitter_Data/eoi/data_live.json") as f_in:
        lines = (line.rstrip() for line in f_in)  # All lines including the blank ones
        lines = (line for line in lines if line)  # Non-blank lines
        for line in lines:
            resp_dict = json.loads(line)
            if 'text' in resp_dict:
                line = resp_dict['text']
                ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", line).split())
                from nltk.tokenize import sent_tokenize, word_tokenize
                from nltk.corpus import stopwords

                data = line
                data = data.lower()
                stopWords = set(stopwords.words('english'))
                additional_stopwords = """, ! $ # & * : ) ( [ ] ; 👍"""
                #stopWords += additional_stopwords.split()
                words = word_tokenize(data)
                wordsFiltered = []
                for w in words:
                    if w not in stopWords:
                        wordsFiltered.append(w)
                #print(wordsFiltered)

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

                wordsFiltered = [e for e in wordsFiltered if e not in ("`", "[", "]", "(", ")", ";", "'", "*", ":", "’",
                     "“", ".", "…", "-", "a", "about", "above", "after",
                    "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because",
                    "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
                    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each",
                    "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
                    "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his",
                    "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
                    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
                    "off", "on", "once", "only", "or", "other", "ought", "our", "ours	ourselves", "out", "over", "own",
                    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
                    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
                    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
                    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
                    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
                    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
                    "you've", "your", "yours", "yourself", "yourselves")]
                #print(wordsFiltered)
                line = " ".join(wordsFiltered)
                line = ' '.join(unique_list(line.split()))

                line = line.replace(".", "")
                line = line.replace("…", "")
                line = line.replace(",", "")
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                wordsFiltered = line.split()
                print(wordsFiltered)
                print(line)  # "ns1:timeSeriesResponseType"




    #
    #     f.write(lines)
    # with open("C:/Users/midul/Documents/Twitter_Data/eoi/data_live.json") as fp:
    #     line = fp.readline()
    #     cnt = 1
    #     while line:
    #         resp_dict = json.loads(line)
    #         line = resp_dict['text']
    #         from nltk.tokenize import sent_tokenize, word_tokenize
    #         from nltk.corpus import stopwords
    #
    #         data = line
    #         stopWords = set(stopwords.words('english'))
    #         words = word_tokenize(data)
    #         wordsFiltered = []
    #
    #         for w in words:
    #             if w not in stopWords:
    #                 wordsFiltered.append(w)
    #
    #         line = " ".join(wordsFiltered)
    #         line = line.replace("\r", "-")
    #         line = line.replace("\n", "-")
    #         print(line)  # "ns1:timeSeriesResponseType"
    #         # print("Line {}: {}".format(cnt, line.strip()))
    #         # line = fp.readline()
    #         cnt += 1
    # for line in loglines:
    #     line_Test = line
    #     #print (line_Test)
    #     resp_dict = json.loads(line_Test)
    #     print(resp_dict['text'])  # "ns1:timeSeriesResponseType"
    #     #print(resp_dict['value']['queryInfo']['creationTime'])  # 1349724919000