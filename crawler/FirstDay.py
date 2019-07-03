import crawler.download as download
import re#正则表达式
import queue

from urllib import parse,robotparser#robotparser用来查看当前网站不允许的操作
from crawler.throttle import Throttle
import lxml.html as lxml

#_表示被丢弃
url="https://alexa.chinaz.com/Country/index_CN.html"
#下载自己需要的页面，然后遍历页面中包含的链接，并搜寻自己需要的消息并下载
#在遍历链接时由于页面会互相链接，因此使用集合存取链接，在搜索到新链接时首先检察是否存在于集合中，若无，则保存

def parse_robots(robots_url):#用来得到
    print(f"robots url{robots_url}")
    try:
        rp = robotparser.RobotFileParser ( robots_url )
        rp.read ()
        return rp
    except Exception as e:
        print(f"robots parse error")

def get_content(html=None):
    all=lxml.fromstring(html)
    for e in all.cssselect ( ".righttxt span" ):
        print ( e.text_content () )
        # print(dir(e))
        # exit(1)


def get_links(html):#得到所有需要的html链接
    web_link=lxml.fromstring(html)
    return map(lambda a:a.get("href"),web_link.cssselect("a"))


def link_crawler(start_url,link_regex,delay=5,useragent="wswp",robots_url_suffix="robots.txt",
                 max_depth=5,scrape_callback=None,num_retries=3):#创建一个队列并遍历
    set1={}
    crawler_queue=queue.Queue()
    crawler_queue.put(start_url)
    headers={"User-Agent":useragent}#注意，此处headers是一个字典，因此需要符合字典的特点
    D = download.Download ( headers, delay=delay )
    protocol,domain,*_=parse.urlsplit(start_url)
    robot_url=parse.urlunsplit((protocol,domain,robots_url_suffix,"",""))#使用元组存储需要连接的url
    rp=parse_robots(robot_url)


    while not crawler_queue.empty():
        url=crawler_queue.get()

        if rp and not rp.can_fetch(useragent,url):
            continue
        html = D ( url, num_retries )
        if not html:
            continue
        if scrape_callback:
            scrape_callback(html)
        depth=set1.get(url,0)
        if depth==max_depth:
            continue

        #Todo

        for link in get_links(html):
            if link and re.match(link_regex,link):
                abs_link=parse.urljoin(url,link)
                if abs_link not in set1:
                    crawler_queue.put ( abs_link )
                    set1[abs_link]=depth+1

if __name__ == "__main__":
    url = "https://alexa.chinaz.com/Country/index_CN.html"
    link_regex = r"index_CN_"
    link_crawler ( url, link_regex, 0, scrape_callback=get_content)






