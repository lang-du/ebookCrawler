import sys

sys.path.append('..')
import scrapy
from bookSpider.items import ChapterItem
import mysql.connector
from mysql.connector import errorcode


class BookSpider(scrapy.Spider):
    name = "bookspider"
    start_urls = ["http://www.xbiquge.la/xiaoshuodaquan/"]

    def __init__(self):
        # 连接数据库book，数据表为chapter
        config = {
            'user': 'root',
            'password': '939500',
            'host': '127.0.0.1',
            'database': 'book',
            'raise_on_warnings': True
        }
        self.query = ("select chapter_url from chapter "
                      '''where chapter_url="%s"''')

        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    # 解析小说大全页面
    def parse(self, response):
        book_urls = response.css('div[class="novellist"] li a::attr(href)').getall()
        for book_url in book_urls:
            request = scrapy.Request(book_url, callback=self.parse_book)
            yield request

    # 解析单本小说界面
    def parse_book(self, response):
        chapter_urls = response.css('#list dd a::attr(href)').getall()  # 获取一本小说所有的章节url列表
        for chapter_url in chapter_urls:
            if self.is_chapter_url_exists(response.urljoin(chapter_url)):
                continue
            yield response.follow(chapter_url, callback=self.parse_chapter)

    # 解析小说章节页面
    def parse_chapter(self, response):
        category = response.css('div[class="con_top"] a::text')[1].get()
        bookName = response.css('div[class="con_top"] a::text')[2].get()
        chapterName = response.css('div[class="bookname"] h1::text').get()
        chapterUrl = response.url
        text_list = response.css('#content::text').getall()
        text = chapterName + '\n'
        for txt in text_list:
            txt.strip('\r')
            txt.strip('\xa0')
            text = text + txt
        item = ChapterItem()
        item['category'] = category
        item['bookName'] = bookName
        item['chapterName'] = chapterName
        item['chapterUrl'] = chapterUrl
        item['chapterText'] = text
        yield item

    # 判断数据库中是否已有该数据
    def is_chapter_url_exists(self, url):
        self.cursor.execute(self.query % url)
        for urls in self.cursor:
            print(urls, "   数据已存在！---------------------")
            return True
        return False

    def __del__(self):
        self.cursor.close()
        self.cnx.close()
