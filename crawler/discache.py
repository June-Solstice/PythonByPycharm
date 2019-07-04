import hashlib
import os
import json




class DiskCache:
    def __init__(self,cache_dir="cache"):
        self.cache_dir=cache_dir

    def url_to_path(self,url):
        filename=hashlib.sha256(bytes(url,"utf-8")).hexdigest()
        return  os.path.join(self.cache_dir,filename)#找到存储文件的位置
#b=a[i]时__getitem__方法被调用
#a[i]=b时__setitem__方法被调用
    def __getitem__(self, url):#兼容之前内容，若存在读出文件内容,
        path=self.url_to_path(url)
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8")as f:
                return json.load(f)
        else:
            raise KeyError(f"{url} do not exist")

    def __setitem__(self,url,result):#将值写入文件
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        path=self.url_to_path(url)
        with open(path,"w",encoding="utf8")as f:
            json.dump(result,f)#将对象以序列形式写入文件


