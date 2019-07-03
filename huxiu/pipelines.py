# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class HuxiuPipeline(object):
    result_list = []
    result_dict = {}

    def process_item(self, item, spider):
        if len(item) != 0:
            # 這個轉換是重點,因為沒有轉換會有一個錯誤
            # TypeError: Object of type 'DoubanmovieItem' is not JSON serializable
            item = dict(item)
            self.result_list.append(item)
        else:
            print("最後結尾處理,比如寫入資料庫,文檔,當然也可以一筆一筆的寫入,不用等到最後...")
            self.result_dict["Result"] = self.result_list
            # print(self.result_dict)
            with open("huxiu虎嗅.json", "w",
                       encoding="utf-8") as f:
                 f.write(json.dumps(dict(self.result_dict), ensure_ascii=False, indent=2))

        return item

    def close_spider(self, spider):
        print(self.result_dict)
        print("it's over..也可以在這裡保存資料....")