import requests
import crawler.throttle as throttle

class Download:
    def __init__(self, headers, proxies=None,delay=5,cache={}):
        self.headers = headers
        self.proxies = proxies
        self.cache=cache
        self.throttle = throttle.Throttle ( delay )

    def __call__(self, url, num_retries=3):#可以对外界屏蔽不必要的信息，保护自己
        try:#从内存中读取值，但由于程序结束后操作系统会自动清除内存，因此选择写入磁盘
            result=self.cache[url]#尝试文件，若不为空则调入内存并输出
            print(f"loaded from cache{url}")
            return result["html"]
        except Exception:
            print ( f"try to download {url}" )
            for i in range(num_retries):
                result=self.download(url)
                if result["code"]==200:
                    if self.cache:
                        self.cache[url]=result
                    return result["html"]

            print(f"download error status")
            if not result["code"] or 400 <= result["code"] < 500:
                return None

            print ( f"retry for {i + 2} times" )
    def download(self,url):
        self.throttle.wait ( url )

        result = {"html": None, "code": None}
        try:
            resp = requests.get ( url, headers=self.headers, proxies=self.proxies )
            result["html"] = resp.text
            result["code"] = resp.status_code
        except requests.RequestException as e:
            print ( f"download error {e}" )

        return result
