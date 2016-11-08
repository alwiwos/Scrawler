
# -*- coding:utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from Scrawler.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = "Scrawler"
    download_delay = 0.1
    allowed_domains = ["meizitu.com"]
    start_urls = (
         #'http://www.meizitu.com/a/xinggan.html',
        # 'http://www.meizitu.com/a/list_1_1.html',
        #'http://www.meizitu.com/a/sifang.html',

        'http://www.meizitu.com/a/qingchun.html',
    )

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath('//h3/a/@href').extract():
      #  for link in sel.xpath('//*[@id="wp-item"]/div/h3/a/@href').extract():
      #      print 'okok  ok ok ok ok o k'
            request = scrapy.Request(link, headers={'User-Agent': "your agent string"}, callback=self.parse_item)
            yield request  # 返回请求
        # 获取页码集合
        pages = sel.xpath('//*[@id="wp_page_numbers"]/ul/li/a/@href').extract()
       # print('pages: %s' % pages)  # 打印页码
        if len(pages) > 2:  # 如果页码集合>2
            page_link = pages[-2]  # 图片连接=读取页码集合的倒数第二个页码
            page_link = page_link.replace('/a/', '')  # 图片连接=page_link（a替换成空）
            request = scrapy.Request('http://www.meizitu.com/a/%s' % page_link, headers={'User-Agent': "your agent string"}, callback=self.parse)
            yield request  # 返回请求

    def parse_item(self, response):
        # l=用ItemLoader载入MeizituItem()
        l = ItemLoader(item=MeizituItem(), response=response)
        # 名字
  #      l.add_xpath('name', '//h2/a/text()')
        # 标签
  #      l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        # 图片连接
        l.add_xpath('image_urls', "//div[@id='picture']/p/img/@src", Identity())
        # url
        l.add_value('url', response.url)

        return l.load_item()



