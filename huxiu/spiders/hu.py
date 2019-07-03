# -*- coding: utf-8 -*-
import scrapy
import json
from lxml import etree
from huxiu.items import HuxiuItem


class HuSpider(scrapy.Spider):
    name = 'hu'
    allowed_domains = ['www.huxiu.com']
    start_urls = ['http://www.huxiu.com/index.php']
    print("虎嗅爬蟲開始.....................")
    pg = 1

    # def start_requests(self):
    #     params = {
    #         "huxiu_hash_code": "b46b6dad804d7d9362a29fe56a8e47a2",
    #         "page": "2",
    #
    #     }
    #     url = "https://www.huxiu.com/v2_action/article_list"
    #     yield scrapy.FormRequest(
    #         url,
    #         callback=self.parse,
    #         method="POST",
    #         formdata=params
    #     )

    def parse(self, response):
        print("yes in ")
        if self.pg == 1:
            # 第一頁用get
            # html_str = response.text
            # print(html_str)
            div_list = response.xpath("//div[@class='container']//div[@class='mod-info-flow']/div")
            print(len(div_list))
            for div in div_list:
                item = HuxiuItem()
                item["title"] = div.xpath(".//div[contains(@class,'mob-ctt')]/h2/a/text()").extract_first()
                item["article_url"] = "{}".format("https://www.huxiu.com") + div.xpath("./div/a/@href").extract_first()
                item["img"] = div.xpath("./div/a/img/@src").extract_first()
                item["img2"] = div.xpath("./div[2]/div/div/a/img/@src").extract_first()
                item["href2"] = "{}".format("https://www.huxiu.com") + div.xpath("./div[2]/div/div/a/@href").extract_first() if len(div.xpath("./div[2]/div/div/a/@href")) > 0 else None
                yield item
            self.pg += 1

        if self.pg > 1:
            # 下一頁
            params = {
                "huxiu_hash_code": "b46b6dad804d7d9362a29fe56a8e47a2",
                "page": "{}".format(self.pg),

            }
            # self.pg += 1
            # print(self.pg)
            url = "https://www.huxiu.com/v2_action/article_list"
            yield scrapy.FormRequest(
                url,
                callback=self.parse_nextpage,
                method="POST",
                formdata=params
            )

    def parse_nextpage(self, response):
        print("nextpage")
        json_dict = json.loads(response.body_as_unicode())
        # print(json_dict)
        data_str = json_dict["data"]
        # print(data_str)
        # print(type(data_str))
        if len(data_str) > 0:
            html_str = etree.HTML(data_str)
            div_list = html_str.xpath("//div[@class='mod-b mod-art']")
            for div in div_list:
                item = HuxiuItem()
                item["title"] = div.xpath(".//div[@class='mob-ctt']/h2/a/text()")[0]
                item["article_url"] = "{}".format("https://www.huxiu.com") + div.xpath(".//div[@class='mob-ctt']/h2/a/@href")[0]
                item["img"] = div.xpath(".//div[contains(@class,'mod-thumb')]//img/@data-original")[0] if len(div.xpath(".//div[contains(@class,'mod-thumb')]//img/@data-original")) > 0 else None
                item["img2"] = div.xpath(".//div[@class='mob-ctt']/div[@class='mob-author']/div/a/img/@src")[0]
                item["href2"] = "{}".format("https://www.huxiu.com") + div.xpath(".//div[@class='mob-ctt']/div[@class='mob-author']/a/@href")[0]
                # print(item)
                yield item
            self.pg += 1
            print(self.pg)
            # 測試用的,之後要mark====================
            if self.pg == 3:
                # return
                item = HuxiuItem()
                yield item
                print("虎嗅爬蟲結束.........")
                return
            # =======================================
            params = {
                "huxiu_hash_code": "b46b6dad804d7d9362a29fe56a8e47a2",
                "page": "{}".format(self.pg),

            }
            url = "https://www.huxiu.com/v2_action/article_list"
            yield scrapy.FormRequest(
                url,
                callback=self.parse_nextpage,
                method="POST",
                formdata=params
            )
        else:
            item = HuxiuItem()
            yield item
            print("虎嗅爬蟲結束.........")