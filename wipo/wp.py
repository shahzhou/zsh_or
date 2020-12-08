import requests, json
from sites.wipo.get_qk import get_qk
import execjs
import base64



with open('qz.js', 'r', encoding='utf-8') as f:
    qz_js = f.read()


def get_qz(brand,qk):
    """获取qz参数, 传入商标名称和qk"""
    qi = '2-' + qk
    # key = {"p": {"search": {"sq": [{"te": brand, "fi": "BRAND"}], "fq": [{"fi": "SOURCE", "te": "USTM", "co": "OR"}]}, "start": 30},
    #        "type": "brand", "la": "en", "qi": qi, "queue": 1, "_": "9863"}

    key = {"p": {"search": {"sq": [{"te": brand, "fi": "BRAND"}], "fq": [{"fi": "SOURCE", "te": "USTM", "co": "OR"}]},
           "start": 0}, "s": {"dis": "flow"}, "type": "brand", "la": "en",
     "qi": qi, "queue": 1, "_": "9863"}
    key = json.dumps(key)
    con = execjs.compile(qz_js)
    value = con.call('get_qz', key)
    return value


def get_brand(qz):
    url = "https://www3.wipo.int/branddb/jsp/select.jsp"

    payload = "qz={}".format(qz)
    headers = {
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'Origin': "https://www3.wipo.int",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Referer': "https://www3.wipo.int/branddb/en/",
        'X-Requested-With': "XMLHttpRequest",
        'Cookie': "JSESSIONID=9A2B5878B8512D74D3448341CEE59F67.bswa2n; ABIW=balancer.cms41; _ga=GA1.3.2117463190.1571732541; _gid=GA1.3.375471501.1571732541; _ga=GA1.2.2117463190.1571732541; _gid=GA1.2.375471501.1571732541; wipo_language=en",
        'Connection': "keep-alive",
        'Cache-Control': "no-cache",
        'Host': "www3.wipo.int",
        'Content-Length': "263",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


if __name__ == '__main__':
    # qk = get_qk()
    qk = 'hd/jwA4Y5Ve98UJuIFjCO4+wzgudGAnxEV6LOacYBeQ='  # qk不一定每次都更新
    qz = get_qz('gucci', qk)
    # print(qz)
    get_brand(qz)
