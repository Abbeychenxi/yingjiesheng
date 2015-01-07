__author__ = 'Abbey'

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from xiaozhao.items import XiaozhaoItem
from scrapy.selector import Selector
import re
import datetime
import time
from scrapy.http import Request
import sqlite3
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import logging
from scrapy.log import ScrapyFileLogObserver
import HTMLParser

class Yjs(CrawlSpider):
    name = "yjs"
    allowed_domains = ['yingjiesheng.com']

    # start_urls = ['http://www.yingjiesheng.com/beijing-morejob-1.html',
    #               'http://www.yingjiesheng.com/shanghai-morejob-1.html',
    #               'http://www.yingjiesheng.com/guangzhou-morejob-1.html',
    #               'http://www.yingjiesheng.com/tianjin-morejob-1.html',
    #               'http://www.yingjiesheng.com/nanjing-morejob-1.html',
    #               'http://www.yingjiesheng.com/shenzhen-morejob-1.html',
    #               'http://www.yingjiesheng.com/jinanjob/list_1.html',
    #               'http://www.yingjiesheng.com/wuhan-morejob-1.html',
    #               'http://www.yingjiesheng.com/chengdu-morejob-1.html',
    #               'http://www.yingjiesheng.com/dalianjob/list_1.html',
    #               'http://www.yingjiesheng.com/hangzhoujob/list_1.html',
    #               'http://www.yingjiesheng.com/chongqingjob/list_1.html',
    #               'http://www.yingjiesheng.com/qingdaojob/list_1.html',
    #               'http://www.yingjiesheng.com/fuzhoujob/list_1.html',
    #               'http://www.yingjiesheng.com/xianjob/list_1.html',
    #               'http://www.yingjiesheng.com/shandongjob/list_1.html',
    #               'http://www.yingjiesheng.com/jiangsujob/list_1.html',
    #               'http://www.yingjiesheng.com/guangdongjob/list_1.html',
    #               'http://www.yingjiesheng.com/liaoningjob/list_1.html',
    #               'http://www.yingjiesheng.com/hubeijob/list_1.html',
    #               'http://www.yingjiesheng.com/sichuanjob/list_1.html',
    #               'http://www.yingjiesheng.com/hebeijob/list_1.html',
    #               'http://www.yingjiesheng.com/zhejiangjob/list_1.html',
    #               'http://www.yingjiesheng.com/yunnanjob/list_1.html',
    #               'http://www.yingjiesheng.com/jilinjob/list_1.html',
    #               'http://www.yingjiesheng.com/fujianjob/list_1.html',
    #               'http://www.yingjiesheng.com/guizhoujob/list_1.html',
    #               'http://www.yingjiesheng.com/shanxijob/list_1.html',
    #               'http://www.yingjiesheng.com/henanjob/list_1.html',
    #               'http://www.yingjiesheng.com/guangxijob/list_1.html',
    #               'http://www.yingjiesheng.com/shanxijob/list_1.html',
    #               'http://www.yingjiesheng.com/hunanjob/list_1.html',
    #               'http://www.yingjiesheng.com/hainanjob/list_1.html',
    #               'http://www.yingjiesheng.com/heilongjiangjob/list_1.html',
    #               'http://www.yingjiesheng.com/neimenggujob/list_1.html',
    #               'http://www.yingjiesheng.com/gansuningxiaqinghaijob/list_1.html',
    #               'http://www.yingjiesheng.com/xinjiangxizangjob/list_1.html',
    #               'http://www.yingjiesheng.com/anhuijob/list_1.html',
    #               'http://www.yingjiesheng.com/jiangxijob/list_1.html'
    #               ]
    start_urls = [
        "http://www.yingjiesheng.com/beijing-morejob-1.html"
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        logFile = open('debug.log', 'w')
        log_observer = ScrapyFileLogObserver(logFile, level=logging.INFO)
        log_observer.start()
        self.cx, self.cu = self.sqlite()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def sqlite(self):
        cx = sqlite3.connect('./link.db')
        cu = cx.cursor()
        cu.execute('create table if NOT EXISTS links (url text PRIMARY key)')
        return cx, cu

    def spider_closed(self, spider):
        self.cx.close()

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath('//tr[@class="tr_list"] | //tr[@class="bg_0"] | tr[@class="bg_1"]')
        for tr in trs:
            link = tr.xpath('td[@class="item1"]/a/@href').extract()
            if link:
                link_str = link[0]
                if link_str[0] == 'h':
                    pass
                else:
                    link_str = 'http://www.yingjiesheng.com/' + link_str
            date = tr.xpath('td[@class="date center"]/text() | td[@class="date cen"]/text()').extract()
            if date:
                date_str = date[0]
                date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                time_time = int(time.mktime(date_time.timetuple()))
                date_now = datetime.date.today()
                now_time = int(time.mktime(date_now.timetuple()))
                if now_time - time_time <= 1 * 24 * 60 * 60:
                    sql = 'select * from links where url="' + link_str + '"'
                    self.cu.execute(sql)
                    url = self.cu.fetchone()
                    if url:
                        pass
                    else:
                        sql = 'insert into links values ("' + link_str + '")'
                        self.cu.execute(sql)
                        self.cx.commit()
                        yield Request(link_str, callback=self.parse_page)
                else:
                    continue
        url = response.url
        if url in self.start_urls:
            index = url.index('1')
            pre = url[0: index]
            end = url[index+1:]
            for i in range(2, 6):
                nextPage = pre + str(i) + end
                yield Request(nextPage, callback=self.parse)
            indexOfLine = url.index('-')
            yield Request('www.yingjiesheng.com/' + url[0: indexOfLine] + '/')

    def re_yingjiesheng(self):
        pattern_yingjiesheng = re.compile(r'\W+[yY]{0,1}\W*ing\W*[jJ]{0,1}\W*i{0,1}e{0,1}\W*[sS]{0,1}\W*h{0,1}e{0,1}n{0,1}g{0,1}')
        return pattern_yingjiesheng

    def parse_page(self, response):
        sel = Selector(response)
        item = XiaozhaoItem()
        item['link'] = [response.url]
        div = sel.xpath('//div[@class="mleft"] | //div[@class="com_mleft"]')
        # item['title'] = div.xpath('h1/text() | div[@class="com"]/h2/a/text()').extract()
        title_t = div.xpath('h1/text() | div[@class="com"]/h2/a/text()').extract()
        if title_t:
            title = title_t[0]
            if title.find('[') >= 0:
                front = title.index('[')
                try:
                    end = title.index(']')
                    item['title'] = [title[end+1:]]
                    citys = title[front+1:end].split('|')
                except ValueError:
                    item['title'] = title_t
            else:
                item['title'] = title_t
        else:
            item['title'] = []
        div_info = div.xpath('div[@class="info clearfix"]')
        lis = div_info.xpath('ol')
        for index, li in enumerate(lis.xpath('li')):
            if index == 0:
                item['releaseTime'] = li.xpath('u/text()').extract()
            elif index == 1:
                item['workPlace'] = li.xpath('u/text()').extract()
            elif index == 2:
                item['positionType'] = li.xpath('u/text()').extract()
            elif index == 3:
                item['source'] = li.xpath('u/text()').extract()
            elif index == 4:
                item['position'] = li.xpath('u/text()').extract()
        professionalLabel = div.xpath('div[@style="margin-top:10px; overflow:hidden"]/a/text()').extract()
        if professionalLabel:
            item['professionalLabel'] = professionalLabel
        else:
            item['professionalLabel'] = []
        info = sel.xpath('//div[@class="jobIntro"] | //div[@class="job_list"]')
        try:
            if not item['position']:
                item['position'] = info.xpath('h1/a/text()').extract()
        except KeyError:
            pass
        for index, li in enumerate(info.xpath('ul/li')):
            if index == 0:
                item['workPlace'] = li.xpath('span/text() | span/a/text()').extract()
            elif index == 1:
                item['validDate'] = li.xpath('span/text()').extract()
            elif index == 2:
                item['hiringNumber'] = li.xpath('span/text()').extract()
            elif index == 3:
                item['positionType'] = li.xpath('text()').extract()
        # description = info.xpath('.//a[not[re:test(@href, "http://bbs.yingjiesheng.com/\.+")]]/text() | .//p/text() | .//div/text() | .//span/text() | .//td/text() | text() | .//br | .//strong/text() | .//li/text() | .//th/text() | .//h2/text() | .//font/text()').extract()
        # item['description'] = description
        description = self.handle_description(info)
        pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
        pattern_yingjiesheng = self.re_yingjiesheng()
        for i, index in enumerate(description):
            match = pattern.search(index)
            if match:
                item['email'] = [match.group()]
            match_yingjiesheng = pattern_yingjiesheng.search(index.lower())
            if match_yingjiesheng:
                description[i] = u''
        item['description'] = description
            # if index == u'<br>':
            #     if i > 0 and description[i-1]:
            #         if description[i-1][-1] != u'\n':
            #             description[i] = u'\n'
            #         else:
            #             description[i] = u''
            #     else:
            #         description[i] = u''
        try:
            if citys:
                place_work = u''
                for place in item['workPlace']:
                    place_work += place
                    place_work += u' '
                for city in citys:
                    if city not in place_work:
                        place_work += city
                        place_work += u' '
                item['workPlace'] = [place_work]
        except NameError:
            pass
        return item

    def handle_description(self, info):
        description = info.extract()
        parse_res = []
        parse = InfoParser(parse_res)
        try:
            parse.feed(description[0])
            parse_res = parse.outRes()
        except IndexError:
            parse_res = []
        return parse_res

class InfoParser(HTMLParser.HTMLParser):
    def __init__(self, parse_res):
        HTMLParser.HTMLParser.__init__(self)
        self.parse_res = parse_res
        self.table = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in (u'tbody', u'td', u'tr'):
            if tag.lower() == u'tbody':
                self.table.append(u'tbody')
                self.parse_res.append(u'<table>\n')
            if self.table and (tag.lower() == 'tbody' or tag.lower() == 'tr'):
                self.parse_res.append(u'<%s>\n' % tag)
            elif self.table and tag.lower() == u'td':
                self.parse_res.append(u'<%s>' % tag)
        elif tag == u'br':
            self.parse_res.append(u'\n')


    def handle_endtag(self, tag):
        if tag.lower() in (u'tbody', u'td', u'tr'):
            if self.table:
                self.parse_res.append(u'</%s>\n' % tag)
            if tag.lower() == u'tbody':
                self.table.pop()
                self.parse_res.append(u'</table>')


    def handle_data(self, data):
        if re.match(u'\u672c\u7ad9\u63d0\u9192:\u5982\u4f55\u8bc6\u522b\u865a\u5047\u62db\u8058\u4fe1\u606f\uff1f\u6c42\u804c\u5fc5\u770b\uff0c\u5207\u52ff\u53d7\u9a97\u4e0a\u5f53\uff01', data) or re.match(u'\u5982\u4f55\u5199\u4e00\u4efd\u7b80\u5355\u3001\u76f4\u63a5\u3001\u9ad8\u6548\u7684\u6c42\u804c\u4fe1\uff1f', data):
            pass
        else:
            if data:
                if data[-1] == u'\n':
                    data = data.strip()
                    data += u'\n'
                else:
                    data = data.strip()
                if data.strip():
                    self.parse_res.append('<p>%s</p>' % data)
                else:
                    self.parse_res.append(data)

    def handle_entityref(self, name):
        self.parse_res.append(u'&%s;' % name)

    def handle_charref(self, name):
        self.parse_res.append(u'&#%s;' % name)

    def outRes(self):
        return self.parse_res