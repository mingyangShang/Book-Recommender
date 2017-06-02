# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from DoubanSpider.DoubanSpider.items import DoubanBookItem
from scrapy import log
class book_spider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["book.douban.com"]
    start_urls = (
        'https://book.douban.com/tag/%E4%B8%9C%E9%87%8E%E5%9C%AD%E5%90%BE',
    )
    def parse(self, response):
        sel = Selector(response)
        # 获取 图书列表中每个图书单页链接 //*[@id="subject_list"]/ul/li/div[2]/h2/a
        for link in sel.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/@href').extract():
            request = scrapy.Request(link, callback=self.parse_item)
            yield request
        #获取下一页连接  测试阶段不进行翻页
        #next_page = sel.xpath('//link[@rel="next"]/@href').extract()
        #log.msg(next_page, level=log.INFO)
        #if len(next_page) > 0:
        #    yield scrapy.Request("https://book.douban.com"+next_page[0], callback=self.parse)
    def parse_item(self, response):
        sel = Selector(response=response)
        item=DoubanBookItem()
        #//*[@id="wrapper"]/h1/span
        item["name"] = sel.xpath("//div[@id='wrapper']/h1/span/text()").extract()[0].strip()
        #//*[@id="interest_sectl"]/div/div[2]/strong
        score= sel.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()").extract()
        item["score"] = score[0].strip() if len(score)>0 else ""
        item["link"] = response.url
        # 豆瓣书籍有时并不完整，会出现找不至值的情况
        try:
            contents = sel.xpath("//div[@id='link-report']//div[@class='intro']")[-1].xpath(".//p//text()").extract()
            item["content_description"] = "\n".join(content for content in contents)
        except:
            item["content_description"] = ""
        try:
            profiles = sel.xpath("//div[@class='related_info']//div[@class='indent ']//div[@class='intro']")[-1].xpath(".//p//text()").extract()
            item["author_profile"] = "\n".join(profile for profile in profiles)
        except:
            item["author_profile"] = ""
        # 获取 书籍信息列表
        datas = response.xpath("//div[@id='info']//text()").extract()
        datas = [data.strip() for data in datas] #去除多余换行与空白
        datas = [data for data in datas if data != ""] #去除空项
        for data in datas:
            if u"作者" in data:
                if u":" in data:
                    item["author"] = datas[datas.index(data)+1]
                elif u":" not in data:
                    item["author"] = datas[datas.index(data)+2]
            elif u"出版社:" in data:
                item["press"] = datas[datas.index(data)+1]
            elif u"出版年:" in data:
                item["date"] = datas[datas.index(data)+1]
            elif u"页数:" in data:
                item["page"] = datas[datas.index(data)+1]
            elif u"定价:" in data:
                item["price"] = datas[datas.index(data)+1]
            elif u"ISBN:" in data:
                item["ISBN"] = datas[datas.index(data)+1]
        print item
        return item