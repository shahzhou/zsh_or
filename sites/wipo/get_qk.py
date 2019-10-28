import requests, re


def get_qk():
    """获取qk参数"""
    url = "https://www3.wipo.int/branddb/en/"

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Sec-Fetch-Site': "none",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': "JSESSIONID=9A2B5878B8512D74D3448341CEE59F67.bswa2n; ABIW=balancer.cms41; _ga=GA1.3.2117463190.1571732541; _gid=GA1.3.375471501.1571732541; _ga=GA1.2.2117463190.1571732541; _gid=GA1.2.375471501.1571732541; wipo_language=en",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)

    data = response.text
    qk = re.search(r'var qk = "(.*?)";', data, re.S).group(1)
    return qk


if __name__ == '__main__':
    print(get_qk())