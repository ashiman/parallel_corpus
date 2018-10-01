import codecs
import hashlib

from lxml import html
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')
Type = sys.getfilesystemencoding()


class MySpider(CrawlSpider):
    name = 'crawlspider'
    start_urls = ['https://barabanki.nic.in/']
    allowed_domains = ['barabanki.nic.in']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = dict()
        item['url'] = response.url
        item['title'] = response.meta['link_text']
        # extracting basic body
        item['body'] = '\n'.join(response.xpath('//text()').extract())
        # or better just save whole source
        item['source'] = response.body
        url = response.url
        # if url.startswith('https://barabanki.nic.in/') and not url.startswith('https://barabanki.nic.in/hi'):
        print "url --->" + url
        link = response.xpath('//*[@id="accessibilityMenu"]/li[5]/div/ul/li[2]/a//@href').extract()
        if "http" not in link[0]:
            link = response.xpath('//*[@id="accessibilityMenu"]/li[6]/div/ul/li[2]/a//@href').extract()
        url = url.replace("/", "_")
        f = '/Users/reverie-pc/Desktop/webpages/barabanki/hindi_links.txt'
        with codecs.open(f, 'a', 'utf-8') as f1:
            f1.write(url.strip() + "\t" + link[0].strip() + '\n')
            # print "link ---->>>"
        # for l in link:
        #     print l
        # page = requests.get(link[0])
        # tree = html.fromstring(page.content)
        # url = url.replace("/", "_")
        # try:
        #     body = tree.xpath('//text()')
        #     print "hindi ---->>>>>" + body
        #     filename = "/Users/reverie-pc/Desktop/webpages/barabanki/hindi/" + url + ".html"
        #     with codecs.open(filename, 'wb', 'utf-8') as f:
        #         f.write(body)
        # except:
        #     print " xpath not found"

        if '/hi' not in response.url:
            filename = "/Users/reverie-pc/Desktop/webpages/barabanki/english/" + url + ".html"
            # filename = "/Users/reverie-pc/Desktop/webpages/barabanki/" + hashlib.md5(response.url).hexdigest() + ".html"
            with codecs.open(filename, 'wb', 'utf-8') as f:
                f.write(response.body)
        return item
