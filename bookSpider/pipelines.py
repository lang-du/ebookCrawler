# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from scrapy.exporters import JsonLinesItemExporter
import mysql.connector
from mysql.connector import errorcode


class BookspiderPipeline:
    def __init__(self):
        # 连接数据库book，数据表为chapter
        self.config = {
            'user': 'root',
            'password': '939500',
            'host': '127.0.0.1',
            'database': 'book',
            'raise_on_warnings': True
        }
        self.add_chapter = ("INSERT INTO chapter"
                       "(category, book_name, chapter_name, chapter_url, chapter_text)"
                       "VALUES(%(category)s, %(book_name)s, %(chapter_name)s, %(chapter_url)s, %(chapter_text)s)")

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()

    def process_item(self, item, spider):
        data_chapter = {'category': item['category'],
                        'book_name': item['bookName'],
                        'chapter_name': item['chapterName'],
                        'chapter_url': item['chapterUrl'],
                        'chapter_text': item['chapterText']}
        self.cursor.execute(self.add_chapter, data_chapter)
        self.cnx.commit()
        return item


