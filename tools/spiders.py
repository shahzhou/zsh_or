from types import GeneratorType

from scrapy.exceptions import DontCloseSpider
from scrapy import signals, Spider, Request, FormRequest
from scrapy.utils.trackref import live_refs

import logging


class RedisSpider(Spider):

    MAX_REQUEST_QUEUE_FACTOR = 15

    def next_requests(self):
        pass

    def setup_idle(self, crawler=None):
        if crawler is None:
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.response_received, signal=signals.response_received)  # 该信号绑定一个方法

    def schedule_next_request(self, num=1):
        add_request_count = 0
        while add_request_count < num:
            try:
                result = self.next_requests()
                if isinstance(result, GeneratorType):
                    result = list(result)
                if not result:
                    break
            except Exception as e:
                self.logger.error(e)
                break
            else:
                if not isinstance(result, list):
                    result = [result]

                for req in result:
                    add_request_count += 1
                    if isinstance(req, Request):
                        self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):  # 信号触发方法 当spider进入空闲状态时发送该信号  即requests正在等待被下载，requests被调度， items正在item pipeline中处理
        """在 spider_idle 处理器中调度某些请求来避免spider被关闭。一直触发schedule_next_request方法，不关闭spider"""
        if self.crawler.crawling:
            self.schedule_next_request()   # 这里调用schedule_next_requests() 来从redis中生成新的请求,一直取任务 生产request对象
            raise DontCloseSpider  # 抛出不要关闭爬虫的DontCloseSpider异常，保证爬虫活着

    def response_received(self):  # 当引擎从downloader获取一个新的response时发送该信号， 触发该方法， 保证并发数生效
        total_concurrency = self.crawler.engine.downloader.total_concurrency
        if len(live_refs[Request]) < total_concurrency * self.MAX_REQUEST_QUEUE_FACTOR:
            if self.crawler.crawling:
                self.schedule_next_request(num=total_concurrency)  # 设置的并发数在这里生效

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):  # 是Scrapy用来创建爬虫的类方法。
        """from_crawler用于实例化某个对象（中间件，模块），常常出现在对象的初始化，负责提供crawler.settings"""
        obj = super(RedisSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_idle(crawler)
        return obj

    def get_memory_status(self):
        return len(self.crawler.engine.slot.scheduler), len(live_refs[Request])
