# coding=utf-8
from __future__ import unicode_literals
import os
import codecs
import tempfile
import traceback
import urllib
from bs4 import BeautifulSoup
from sentence_similarity import check

result = codecs.open("results.txt", 'a', 'utf-8')
result.write("ENGLISH" + "\t" + "NMT" + "\t" + "HINDI" + "\t" + "SCORE" + "\n")
failures = codecs.open("fail.txt", 'a', 'utf-8')


def data_extraction(url, file_path):
    # url = "https://gumla.nic.in/hi/tourist-place/%e0%a4%b9%e0%a4%be%e0%a4%aa%e0%a4%be%e0%a4%ae%e0%a5%81%e0%a4%a8%e0%a5%80/".encode(
    #     "utf-8")
    print file_path + "\t" + url

    # Hindi Text
    """ Hindi Text Extraction"""
    html = urllib.urlopen(url.encode("utf-8")).read()
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text_hin = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text_hin.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text_hin = '\n'.join(chunk for chunk in chunks if chunk)

    """ English Text Extraction """
    html = urllib.urlopen(file_path.encode("utf-8")).read()
    soup = BeautifulSoup(html, "lxml")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

        # get text
    text_eng = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text_eng.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text_eng = '\n'.join(chunk for chunk in chunks if chunk)

    # eng_page = codecs.open(file_path, 'r', "utf-8")

    # print(text)

    # fd, path = tempfile.mkstemp()
    try:
        eng_tempfile = tempfile.TemporaryFile()
        eng_tempfile.write(text_eng.encode("utf-8"))
        hindi_tempfile = tempfile.TemporaryFile()
        hindi_tempfile.write(text_hin.encode("utf-8"))
        check(hindi_tempfile, eng_tempfile, result, failures)
        hindi_tempfile.close()
        eng_tempfile.close()

    except Exception as e:
        print "some error"
        print traceback.print_exc()

    # f1 = codecs.open('hindi_new.txt', 'w', 'utf-8')
    # f1.write(text)


for file in os.listdir('/Users/reverie-pc/PycharmProjects/practice/parallel_corpus/MNRE/webpage/'):
    print "file ---> " + file
    links_mappings = {}

    # print "root --> " + root
    # print "dirs ---> " + str(dirs)
    # print "file ---> " + str(files)
    #if "english" in root:
    # district = root.split("/")[-2]
   # print "district --> " + district
    f = codecs.open("/Users/reverie-pc/PycharmProjects/practice/parallel_corpus/MNRE/hindi_links.txt")
    lines = f.readlines()
    for line in lines:
        # print line.strip().split(" ")
        eng_link = line.split(" ")[0].strip()
        hin_link = line.split(" ")[1].strip()
        links_mappings[eng_link] = hin_link
            # print line.strip()
    #print "files ---------> " + str(files)
    # for file in files:
    #     print "file ---> " + str(file)
    #     for f in file:
    #print "file ---> " +  f
    try :
        #print "file ------------------------------->  "  + str(file)
        # file_path =  f.replace("_","/")
        file_path =  "/Users/reverie-pc/PycharmProjects/practice/parallel_corpus/MNRE/webpage/" + file
        print "file path----> " +file_path
        eng_name = file
        eng_name = eng_name.replace(".html", "")
        eng_name = eng_name.replace("_" ,"/")
        print eng_name
        if eng_name in links_mappings.keys():
            url = links_mappings[eng_name]
            print "url ----> " + url
            data_extraction(url, file_path)
    except :
        print "directory error"
        print traceback.print_exc()
        continue
        # if ".htm" in file :
        # print "file name -->" + file
        #     with open(os.path.join(root, file), "r") as auto: