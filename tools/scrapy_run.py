import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils import log
from sites.unit.middlewares import InitHeadersMiddleware


def run_spider(spider, settings={}, args=[]):
    log.DEFAULT_LOGGING['loggers']['scrapy']['level'] = settings.get('LOG_LEVEL', 'WARNING')

    # 如无配置，默认关闭log
    if settings.get('LOG_ENABLED', None) is None:
        settings['LOG_ENABLED'] = False
    settings['TELNETCONSOLE_ENABLED'] = False

    if not settings.get('RETRY_TIMES', None):
        settings['RETRY_TIMES'] = 5

    if not settings.get('DOWNLOADER_MIDDLEWARES', None):  #中间件
        settings['DOWNLOADER_MIDDLEWARES'] = {}

    if not settings.get('ITEM_PIPELINES', None):  #管道
        settings['ITEM_PIPELINES'] = {}

    add_init_header_middleware = True  # 添加初始请求头部header
    for middleware_class in settings['DOWNLOADER_MIDDLEWARES']:
        if middleware_class is InitHeadersMiddleware:
            add_init_header_middleware = False
    if add_init_header_middleware:
        settings['DOWNLOADER_MIDDLEWARES'][InitHeadersMiddleware] = 199

    for pipeline in settings['ITEM_PIPELINES'].keys():
        if not isinstance(pipeline, str):
            pipelines_path = '.'.join([pipeline.__module__, pipeline.__name__])
            settings['ITEM_PIPELINES'][pipelines_path] = settings['ITEM_PIPELINES'][pipeline]
            settings['ITEM_PIPELINES'].pop(pipeline)

    for middleware in settings['DOWNLOADER_MIDDLEWARES'].keys():
        if not isinstance(middleware, str):
            middleware_path = '.'.join([middleware.__module__, middleware.__name__])
            settings['DOWNLOADER_MIDDLEWARES'][middleware_path] = settings['DOWNLOADER_MIDDLEWARES'][middleware]
            settings['DOWNLOADER_MIDDLEWARES'].pop(middleware)

    if not settings.get('EXTENSIONS', None):
        settings['EXTENSIONS'] = {}

    for extension in settings['EXTENSIONS'].keys():
        if not isinstance(extension, str):
            extension_path = '.'.join([extension.__module__, extension.__name__])
            settings['EXTENSIONS'][extension_path] = settings['EXTENSIONS'][extension]
            settings['EXTENSIONS'].pop(extension)

    process = CrawlerProcess(settings)  # 传入自己的配置setting
    process.crawl(spider, *args)
    process.start()


def scrapy_retry_request(request, max_retry, **kwargs):
    request = request.copy()
    retry_no = request.meta.get('retry_no', 0)
    if retry_no <= max_retry:
        request.dont_filter = True
        request.meta['retry_no'] = retry_no + 1
        request.meta['proxy'] = None
        request.priority += 1
        return request
    else:
        if kwargs.get('redis', None):
            try:
                request.meta['proxy'] = None
                kwargs['redis'].rpush('failed_max_retry', request.meta)
            except:
                pass
        return None