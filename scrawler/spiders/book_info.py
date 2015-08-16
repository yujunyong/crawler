# -*- coding: utf-8 -*-

import scrapy
from scrawler.items import BookInfoItem
from scrawler.util.text import strip

class BookInfoSpider(scrapy.Spider):
    name = 'book_info'

    def __init__(self, *args, **kwargs):
        super(BookInfoSpider, self).__init__(*args, **kwargs)

        for key in kwargs:
            if key == 'search_text':
                self.start_urls = ['http://book.douban.com/subject_search?search_text=%s&cat=1001' % kwargs[key]]

    def parse(self, response):
        for href in response.css('.subject-item .info h2 a::attr(href)'):
            detail_url = response.urljoin(href.extract())
            yield scrapy.Request(detail_url, callback=self.parse_book_info)

    def parse_book_info(self, response):
        # 提取页面上的信息
        author = ', '.join(response.css('#info a::text').extract())
        fields = [strip(item) for item in response.css('#info::text').extract() if '\n' not in item]
        evaluate = strip(response.css('#interest_sectl .ll.rating_num::text').extract()[0])

        intro = response.css('.related_info .indent span.all .intro')
        content_desc = '\n'.join(strip(intro[0].css('p').extract()))
        author_desc = '\n'.join(strip(intro[1].css('p').extract()))

        self.logger.debug("evaluate: %s, author: %s, publisher: %s, publish_year: %s, "
                          "page: %s, price: %s, binding: %s, isbn: %s",
                          evaluate, author, fields[0], fields[1], fields[2], fields[3], fields[4], fields[5])
        self.logger.debug("content_desc: %s ......", content_desc[:10])
        self.logger.debug("author_desc: %s ......", author_desc[:10])

        # 将信息存入item
        book_info_item = BookInfoItem()
        book_info_item['evaluate'] = evaluate
        book_info_item['author'] = author
        book_info_item['publisher'] = fields[0]
        book_info_item['publish_year'] = fields[1]
        book_info_item['page'] = fields[2]
        book_info_item['price'] = fields[3]
        book_info_item['isbn'] = fields[5]
        book_info_item['content_desc'] = content_desc
        book_info_item['author_desc'] = author_desc

        book_info_item['douban_url'] = response.url

        yield book_info_item

