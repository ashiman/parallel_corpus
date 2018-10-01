import requests
from lxml import html
import codecs
import urllib
fw = codecs.open("updated_en_sun.txt", "a", "utf-8")

def cleanup_text(text):
    if not text.startswith("<") and not text.startswith(".") and not text.startswith("#") and not text.startswith("img.wp"):
        if "{" in text and ":" in text and ";" in text and "-" in text and "#" in text:
            pass
        else:
            return text
    else:
        return ""

# print page.text
# page = urllib.urlopen("od.htm").read()
page = urllib.urlopen("https://angul.nic.in/od/tourist-place/%E0%AC%B9%E0%AC%BF%E0%AC%99%E0%AD%8D%E0%AC%97%E0%AD%81%E0%AC%B3%E0%AC%BE-%E0%AC%A0%E0%AC%BE%E0%AC%95%E0%AD%81%E0%AC%B0%E0%AC%BE%E0%AC%A3%E0%AD%80/").read()
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
            clean_text = cleanup_text(text[0].strip())

            if clean_text is "" or clean_text is None:
                    continue

            if len(clean_text.split(" "))<4:
                print clean_text + "\t" + str(len(clean_text.split(" ")))
                continue

            # print xp + "\t" + clean_text
            fw.write(xp + "\t" + clean_text + "\n")
