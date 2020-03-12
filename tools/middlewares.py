import random


iphone_user_agent_list = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432 NewsArticle/6.4.2.11 JsSdk/2.0 NetType/WIFI (News 6.4.2 11.000000)',
        'Dalvik/2.1.0 (Linux; U; Android 7.1.1; OS105 Build/NMF26X) NewsArticle/6.6.2 okhttp/3.7.0.6',
        'News 6.6.2 rv:6.6.2.10 (iPhone; iOS 10.2; zh_CN) Cronet',
        'Dalvik/2.1.0 (Linux; U; Android 7.1.2; K3Note Build/NJH47F) NewsArticle/6.6.5 okhttp/3.7.0.6',
        'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Lenovo X3c50 Build/MMB29M) NewsArticle/6.6.5 cronet/58.0.2991.0',
        'Dalvik/2.1.0 (Linux; U; Android 7.0; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10) NewsArticle/6.6.5 okhttp/3.7.0.6',
        'Dalvik/2.1.0 (Linux; U; Android 8.0.0; LON-AL00 Build/HUAWEILON-AL00) NewsArticle/6.6.5 okhttp/3.7.0.6',
        'News 6.6.2 rv:6.6.2.10 (iPhone; iPhone OS 9.3.2; zh_CN) Cronet',
        'Dalvik/2.1.0 (Linux; U; Android 7.1.1; OS105 Build/NMF26X) NewsArticle/6.3.0 cronet/58.0.2991.0',

       ]
pc_user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24"
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]


class InitHeadersMiddleware(object):
    def __init__(self):
        self.ua = pc_user_agent_list

    def get_default_headers(self):
        return {
            'User-Agent': random.choice(self.ua),
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
            'Accept-Encoding': 'gzip, deflate'
        }

    def process_request(self, request, spider):
        default_headers = self.get_default_headers()
        rh_keys = [k.lower() for k in request.headers.keys()]

        for k, v in default_headers.items():
            if k.lower().encode() not in rh_keys:
                request.headers[k] = v


class MobileHeadersMiddleware(InitHeadersMiddleware):
    def __init__(self):
        self.ua = iphone_user_agent_list



