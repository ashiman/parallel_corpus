# coding=utf-8

from __future__ import unicode_literals
import json
import traceback
import numpy
import requests

import codecs

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
        if line.strip() in sentences:
            continue
        else:
            sentences.append(line.strip())
        # if len(line.split(" ")) < 6:
        #     print "short line ---> " + line.strip()
        #     continue
        alligned_dict = {}
        line = unicode(line, encoding="utf-8")
        payload = {}

        # line = unicode(line, encoding="utf-8")
        payload = {}

        try:
            payload = {"data": [line.strip().encode("utf-8")],
                       "src": "en",
                       "tgt": "hi",
                       "n_best": 1,
                       "mask_terms ": [],
                       "mask": True,
                       "segment_after": 0,
                       "debug": True
                       }

            headers = {
                'Content-Type': "application/json",
                'Cache-Control': "no-cache",
                'Postman-Token': "d2a6a05e-b69e-4fa5-86f2-41efca7f07be"
            }

            response = requests.request("POST", url, json=payload, headers=headers)
            text1 = response.text
            # print text1["result"]
            data = json.loads(response.text, encoding="utf-8")
            hindi_string = data["result"][0][0]
            # reference = [word_tokenize(hindi_string)]
            # print "refe " + str(reference)

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
                    if len(wordsA) / len(wordsB) >= 1.5 or len(wordsB) / len(wordsA) >= 1.5:
                        score = 0
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
            if maximum > 0.6:
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
