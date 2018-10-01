# coding=utf-8
import codecs
import csv
import pprint
import itertools
import traceback
from pprint import pprint

#
# f1 = codecs.open('updated_en_sun.txt', 'r', 'utf-8')
# f2 = codecs.open('updated_od_sun.txt', 'r', 'utf-8')
# f3 = codecs.open('cmp_sun.txt', 'w', 'utf-8')
# lines1 = f1.readlines()
# lines2 = f2.readlines()
tag_dict = {}


sentences = []


def check(hin_file, eng_file, result, fail):
    eng_dict = {}
    or_dict = {}
    print "received"
    hin_file.seek(0)
    eng_file.seek(0)
    # print file_hin.readlines()
    eng_lines = eng_file.readlines()
    # print "eng lines --> " + str(eng_lines)
    # eng_file = codecs.open("english_new.txt", 'r', 'utf-8')
    # hin_file = codecs.open("hindi_new.txt", 'r', 'utf-8')
    # eng_file = file_eng
    # hin_file = file_hin
    # result = codecs.open("results.txt", 'a', 'utf-8')
    lines2 = hin_file.readlines()
    # print "hin lines --> " + str(lines2)
    # result.write("ENGLISH" + "\t" + "NMT" + "\t" + "HINDI" + "\t" + "SCORE" + "\n")

    url = "http://184.105.189.239/translate/"
    lines1 = eng_lines
    score =""
    # for line in lines:
    #     if line.strip() in sentences:
    #         continue
    #     else:
    #         sentences.append(line.strip())
    #     # if len(line.split(" ")) < 6:
    #     #     print "short line ---> " + line.strip()
    #     #     continue
    #     alligned_dict = {}
    #     line = unicode(line, encoding="utf-8")
    #     payload = {}
    for line in lines1:
        try:
            values = []
            string = line.split("\t")[1]
            xpath = line.split("\t")[0]
            # parent = line.split("\t")[2].strip()
            if xpath in eng_dict.keys():
                if type(eng_dict[xpath]) is unicode:
                    values.append(eng_dict[xpath])
                    print "yes"
                else:
                    for val in eng_dict[xpath]:
                        # print " val " + val
                        values.append(val)
                # values.append(eng_dict[xpath])
                # values.append(string)
                values.append(string)
                eng_dict[xpath] = values

            else:
                # print " string " + string
                values.append(string)
                eng_dict[xpath] = values
        except:
            print traceback.print_exc()
            continue
    print pprint(eng_dict)

    for line in lines2:
        try:
            values = []
            string = line.split("\t")[1]
            xpath = line.split("\t")[0]
            # parent = line.split("\t")[2].strip()
            if xpath in or_dict.keys():
                if type(or_dict[xpath]) is unicode:
                    values.append(or_dict[xpath])
                    print "yes"
                else:
                    for val in or_dict[xpath]:
                        # print " val " + val
                        values.append(val)
                # values.append(eng_dict[xpath])
                # values.append(string)
                values.append(string)
                or_dict[xpath] = values

            else:
                # print " string " + string
                values.append(string)
                or_dict[xpath] = values
        except:
            print traceback.print_exc()
            continue
    print pprint(or_dict)

    for key in eng_dict.keys():
        if key in or_dict.keys():
            if len(eng_dict[key]) == len(or_dict[key]):
                print str(len(eng_dict[key])) + ":" + str(len(or_dict[key]))
                count = 0
                for e, o in itertools.izip_longest(eng_dict[key], or_dict[key]):
                    e = unicode(e, encoding="utf-8")
                    o = unicode(o, encoding="utf-8")
                    count = count + 1
                    if e is not None and o is not None:
                        print " type of file--> " + str(type(result))
                        print "type -- > " + str(type(e)) + str(type(o))

                        result.write(e.strip() + "\t" + o.strip() + "\n")
                print "value of count : " + str(count)
