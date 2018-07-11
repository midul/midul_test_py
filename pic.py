words = word_tokenize(data)
                wordsFiltered = []
                for w in words:
                    if w not in stopWords:
                        wordsFiltered.append(w)
