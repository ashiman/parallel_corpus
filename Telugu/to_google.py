import time

import codecs
import requests


def google_translate(text, target_lang='hi'):
    url = 'https://www.googleapis.com/language/translate/v2'
    params = {'q': text, 'target': target_lang, 'key': "AIzaSyBjrPLQ6xJhk7Qyok9UsOgF9Kxm-2lKBtY"}
    response = requests.get(url=url, params=params).json()
    translation = response.get('data').get('translations')[0].get('translatedText')
    return translation


# totaltime = 0
# count = 0
# for line in codecs.open("./input_files/test_set.txt", encoding="utf-8"):
# count += 1
# timetaken = 0
text = "District Rural Development Agency"
starttime = time.time()
result = google_translate(text, 'te')
# timetaken = time.time() - starttime
# totaltime += timetaken
print result