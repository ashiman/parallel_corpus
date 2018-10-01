# coding=utf-8

from __future__ import unicode_literals
import json
import tempfile
import traceback
import urllib

import numpy
import requests


sentences = []


def check(hin_file, eng_file, result, fail):
    print "received"
    hin_file.seek(0)
    eng_file.seek(0)
    # print file_hin.readlines()
    eng_lines = eng_file.readlines()
    print "eng lines --> " + str(eng_lines)
    # eng_file = codecs.open("english_new.txt", 'r', 'utf-8')
    # hin_file = codecs.open("hindi_new.txt", 'r', 'utf-8')
    # eng_file = file_eng
    # hin_file = file_hin
    # result = codecs.open("results.txt", 'a', 'utf-8')
    hin_lines = hin_file.readlines()
    print "hin lines --> " + str(hin_lines)
    # result.write("ENGLISH" + "\t" + "NMT" + "\t" + "HINDI" + "\t" + "SCORE" + "\n")

    url = "http://184.105.189.239/translate/"
    lines = eng_lines
    score = ""
    for line in lines:
        try:
            line = unicode(line, encoding="utf-8")
            if line.strip() in sentences:
                continue
            else:
                sentences.append(line.strip())
            # if len(line.strip().split(" ")) < 6:
            #     print "short line ---> " + line.strip()
            #     continue
            alligned_dict = {}
        except:
            print "this line is creating problem ----> " + line.strip()
            fail.write(line.strip() + "\n")
            continue

        try:

            url = 'https://www.googleapis.com/language/translate/v2'
            params = {'q': line.strip(), 'target': "te", 'key': "AIzaSyBjrPLQ6xJhk7Qyok9UsOgF9Kxm-2lKBtY"}
            proxies = {'http': 'http://reverie_7812:reverie123@209.205.212.34:1200',
                       'https': 'http://reverie_7812:reverie123@209.205.212.34:1200'}
            response = requests.get(url=url, params=params, proxies=proxies).json()
            hindi_string = response.get('data').get('translations')[0].get('translatedText')

            for l in hin_lines:
                # print type(l)
                try:
                    l = unicode(l, encoding="utf-8")
                    # print "here"
                    # candidate = word_tokenize(l.strip())
                    # print "candi " + str(candidate)
                    # print type(reference)
                    # print type(candidate)
                    # if len(reference[0]) > 5 and len(candidate) > 4 :

                    # vector1 = text_to_vector(hindi_string.strip())
                    # vector2 = text_to_vector(l.strip())

                    # score = get_cosine(vector1, vector2)

                    # score = bleu_score(reference, candidate)
                    wordsA = hindi_string.strip().split(" ")
                    wordsB = l.strip().split(" ")
                    # print "length"
                    # print float(len(wordsA))/float(len(wordsB))

                    if float(len(wordsA)) / float(len(wordsB)) >= 1.5 or float(len(wordsB)) / float(len(wordsA)) >= 1.5:
                        score = 0
                        print "length"
                        # print float(len(wordsA))/float(len(wordsB))
                        alligned_dict[score] = {line.strip(): l.strip()}
                        continue
                    else:
                        vocab = set(wordsA)
                        vocab = vocab.union(set(wordsB))
                        vocab = list(vocab)
                        # print vocab
                        vA = numpy.zeros(len(vocab), dtype=float)
                        vB = numpy.zeros(len(vocab), dtype=float)

                        for w in wordsA:
                            i = vocab.index(w)
                            vA[i] += 1
                        # print vA

                        for w in wordsB:
                            i = vocab.index(w)
                            vB[i] += 1
                        # print vB

                        score = numpy.dot(vA, vB) / (numpy.sqrt(numpy.dot(vA, vA)) * numpy.sqrt(numpy.dot(vB, vB)))
                        alligned_dict[score] = {line.strip(): l.strip()}
                        # result.write(line.strip() + "\t" + hindi_string + "\t" + l.strip() + "\t" + str(score) + "\n")

                except:
                    continue

            keys = alligned_dict.keys()
            maximum = max(keys)
            if maximum > 0.2:
                print "maximum" + "\t" + str(maximum)
                string = alligned_dict[maximum][line.strip()]
                # print "----->> " + line.strip() + string
                # print "------>>  " + str(alligned_dict[maximum])
                result.write(line.strip() + "\t" + hindi_string + "\t" + string + "\t" + str(maximum) + "\n")
            # print "------>>  " + str(alligned_dict)

            # print data["result"][0][0]

        except Exception as e:
            print "ERROR -------- >>>>>>> " + line.strip()
            fail.write(line.strip() + "\n")
            print traceback.print_exc()
            continue


