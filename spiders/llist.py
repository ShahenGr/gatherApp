# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from list.items import *

class LlistSpider(scrapy.Spider):
    name = "llist"
    allowed_domains = ["list.am"]
    starting_number = 1
    start_urls = (
            'https://www.list.am/en/category/60?_a4=%s' % starting_number,
    )

    def start_requests(self):
        for i in range(self.starting_number, 8):
            yield Request(url = 'https://www.list.am/en/category/60?_a4=%s' % i, callback=self.parse)

    def parse(self, response):
        item = ListItem()
        items = []
        date = response.xpath('//div/div[@class="dl"]/table/tr/td[@class="headerd"]/text()').extract()
        data = response.xpath('//div/div[@class="dl"]/table/tr/td[@class="headerd"]/following::tr')[0].extract()
        half = data.find('href')
        im = data.find('img')
        p = data.find('"p">')
        t = data.find('>', data.find('t">') + 3) + 1
        path = 'list.am' + data[half + 6:data.find('>', half) - 1]
        if im != -1:
            img = data[im + 11:data.find('>', im) - 1]
        else:
            img = None
        if p != -1:
            price = data[p + 4:data.find('<', p)]
        else:
            price = None
        print '*' * 15
        print self.starting_number
        item['rooms'] = self.starting_number
        self.starting_number += 1
        print '*' * 15
        item['date'] = date
        #print 'Date = ',
        #for i in date:
            #print i,
        #print
        #print data
        item['link'] = path
        #print 'Path = ', path
        item['img'] = img
        #print 'Img = ', img
        item['price'] = price
        #print 'Price = ', price
        item['about'] = data[t:data.find('<', t)]
        #print 'Data = ', data[t:data.find('<', t)]
        item['web'] = 'list.am'
        items.append(item)

        return items
