import requests
from lxml import html
import codecs
import urllib
fw = codecs.open("te.txt", "a", "utf-8")

def cleanup_text(text):
    if not text.startswith("<") and not text.startswith(".") and not text.startswith("#") and not text.startswith("img.wp"):
        if "{" in text and ";" in text and "-" in text and "#" in text:
            print "here ---------->"
            pass
        else:
            return text
    else:
        return ""

# print page.text
# page = urllib.urlopen("od.htm").read()
page = urllib.urlopen("https://eastgodavari.nic.in/te/%E0%B0%A4%E0%B1%80%E0%B0%B0%E0%B1%8D%E0%B0%A5%E0%B0%AF%E0%B0%BE%E0%B0%A4%E0%B1%8D%E0%B0%B0-%E0%B0%AA%E0%B0%B0%E0%B1%8D%E0%B0%AF%E0%B0%BE%E0%B0%9F%E0%B0%95-%E0%B0%B0%E0%B0%82%E0%B0%97%E0%B0%82/").read()
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
        text = root.xpath(xp + "/text()")
        if text:
            clean_text = cleanup_text(text[0].strip())

            if clean_text is "" or clean_text is None:
                    continue

            if len(clean_text.split(" "))<4:
                print clean_text + "\t" + str(len(clean_text.split(" ")))
                continue

            # print xp + "\t" + clean_text
            print clean_text
            fw.write(xp + "\t" + clean_text + "\n")
