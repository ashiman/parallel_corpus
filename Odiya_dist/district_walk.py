# coding=utf-8


import os
import codecs
import tempfile
import traceback
import urllib
from bs4 import BeautifulSoup
from final_result import check
import lxml
from lxml import html


results = codecs.open("results.txt", 'a', 'utf-8')
results.write("ENGLISH" + "\t" + "NMT" + "\t" + "HINDI" + "\t" + "SCORE" + "\n")
failures = codecs.open("fails.txt", 'w', 'utf-8')


def cleanup_text(text):
    if not text.startswith("<") and not text.startswith(".") and not text.startswith("#") and not text.startswith("img.wp"):
        if "{" in text and ":" in text and ";" in text and "-" in text and "#" in text:
            pass
        else:
            return text
    else:
        return ""


def data_extraction(url, file_path):
    try:
        clean_text_od = ""
        clean_text_en = ""
        en = []
        od = []
        # url = "https://gumla.nic.in/hi/tourist-place/%e0%a4%b9%e0%a4%be%e0%a4%aa%e0%a4%be%e0%a4%ae%e0%a5%81%e0%a4%a8%e0%a5%80/".encode(
        #     "utf-8")
        print file_path + "\t" + url

        # Hindi Text
        """ Hindi Text Extraction"""
        page = urllib.urlopen(url.encode("utf-8")).read()
        # page = requests.get("od.htm")
        root = lxml.html.fromstring(page)
        tree = root.getroottree()
        # print "tree --> " + str(tree)
        result = root.xpath('//*')
        # print "result --> " +str(result)
        for r in result:
            # print(tree.getpath(r))
            xp = tree.getpath(r)
            child = r.getchildren()
            # print xp
            if "/script" not in xp:
                # print root.xpath(xp)[0].element
                text = root.xpath(xp + "//text()")
                if text:
                    clean_text_od = cleanup_text(text[0].strip())

                    if clean_text_od is "" or clean_text_od is None:
                        continue

                    if len(clean_text_od.split(" ")) < 4:
                        # print clean_text_od + "\t" + str(len(clean_text_od.split(" ")))
                        continue
                    od.append(xp + "\t" + clean_text_od)
                    # print type(od[0])
                    # print xp + "\t" + clean_text_od
                    # fw.write(xp + "\t" + clean_text_od + "\n")

        """ English Text Extraction """
        page = urllib.urlopen(file_path.encode("utf-8")).read()
        # page = requests.get("od.htm")
        root = html.fromstring(page)
        tree = root.getroottree()
        # print "tree --> " + str(tree)
        result = root.xpath('//*')
        # print "result --> " +str(result)
        for r in result:
            # print(tree.getpath(r))
            xp = tree.getpath(r)
            child = r.getchildren()
            # print xp
            if "/script" not in xp:
                # print root.xpath(xp)[0].element
                text = root.xpath(xp + "//text()")
                if text:
                    clean_text_en = cleanup_text(text[0].strip())

                    if clean_text_en is "" or clean_text_en is None:
                        continue

                    if len(clean_text_en.split(" ")) < 4:
                        # print clean_text_en + "\t" + str(len(clean_text_en.split(" ")))
                        continue
                    en.append(xp + "\t" + clean_text_en)
                    # print xp + "\t" + clean_text_en
                    # fw.write(xp + "\t" + clean_text_en + "\n")
        # print en
        # eng_page = codecs.open(file_path, 'r', "utf-8")

        # print(text)

        # fd, path = tempfile.mkstemp()
        try:
            eng_tempfile = tempfile.TemporaryFile()
            for e in en:
                try:
                    # print type(e)
                    # print e
                    eng_tempfile.write(e.strip() + "\n")
                except:
                    print "fatta  " + e
                    continue
            # eng_tempfile.seek(0)
            lines = eng_tempfile.readlines()
            print " lines of temp eng -- >" + str(lines)
            hindi_tempfile = tempfile.TemporaryFile()
            for o in od:
                try:

                    # print "odiya- " + o
                    hindi_tempfile.write(o.encode("utf-8") + "\n")
                except:
                    print "od fatta " + o
                    print traceback.print_exc()
                    continue
            print "in direc"
            check(hindi_tempfile, eng_tempfile, results, failures)
            hindi_tempfile.close()
            eng_tempfile.close()

        except Exception as e :
            print "some error"
            print traceback.print_exc()
    except:
        print "function wala"
        print traceback.print_exc()


    # f1 = codecs.open('hindi_new.txt', 'w', 'utf-8')
    # f1.write(text)


for root, dirs, files in os.walk('/Users/reverie-pc/PycharmProjects/practice/parallel_corpus/Odiya_dist'):
    links_mappings = {}
    print "root --> " + root
    print "dirs ---> " + str(dirs)
    # print "file ---> " + str(files)
    if "english" in root:
        district = root.split("/")[-2]
        print "district --> " + district
        f = codecs.open("/Users/reverie-pc/PycharmProjects/practice/parallel_corpus/Odiya_dist/" + district + "/hindi_links.txt")
        lines = f.readlines()
        for line in lines:
            eng_link = line.split(" ")[0].strip()
            hin_link = line.split(" ")[1].strip()
            links_mappings[eng_link] = hin_link
            # print line.strip()

        for file in files:
            try:
                # print "file ---> " +root + "/" + file
                print "1"
                file_path = root + "/" + file
                print "2"
                eng_name = file
                print "3"
                eng_name = eng_name.replace(".html", "")
                print "4"
                # print eng_name
                if eng_name in links_mappings.keys():
                    print "5"
                    url = links_mappings[eng_name]
                    print "6"
                    print url + ": " + file_path
                    data_extraction(url, file_path)

                    print "7"
            except:
                print "english file error ---> "
                print traceback.print_exc()
                continue


            # if ".htm" in file :
            # print "file name -->" + file
            #     with open(os.path.join(root, file), "r") as auto:
