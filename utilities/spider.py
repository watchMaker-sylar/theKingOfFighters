import requests
from bs4 import BeautifulSoup

import time
import base64
import os

def downloadGif(page, gif_urls):
    makeDirAndCheck(page)
    for name, url in gif_urls.items():
        resp = requests.get(url)
        name = name.replace("\"","")
        file = open(name,"wb")
        file.write(resp.content)
        file.close()

    os.chdir("..")

def makeDirAndCheck(page):
    page = str(page+1)
    dirs = os.listdir(".")
    if page in dirs:
        os.chdir(page)
        files = os.listdir(".")
        for file in files:
            os.remove(file)
        os.chdir("..")
        os.rmdir(page)
    os.mkdir(page)
    os.chdir(page)
# 总页数
pages = 107
# 总gif数量
# 20和106是因为前106页全是20张gif,15是因为最后一页,即107页只有15张gif图
gif_amount = 20 * 106 + 15
# 当前已经处理的gif数
current_gif = 0


for page in range(pages):
    # 下载的url
    url = "https://www.aigei.com/view/73798.html?page={}"
    url = url.format(page + 1)

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"html.parser")

    imgs = soup.find_all("img")
    gif_urls = {}
    for imgTag in imgs:
        attrs = imgTag.attrs
        if (attrs.get('data-original')):
            #因为数据源的下载url使用了base64加密,因此需要在此对其做转换
            byt = base64.b64decode(attrs.get('data-original'))
            download_url = byt.decode('utf-8')
            #获取该gif名字
            parent = imgTag.parent
            parent_item_id = parent['itemid']
            parent_item_name = "".join(parent.next_sibling.next_sibling['title'].split()) + parent_item_id + ".gif"
            parent_item_name = parent_item_name.replace("/","-")
            download_name = parent_item_name
            gif_urls[download_name] = download_url

    # 下载已解析的url
    downloadGif(page,gif_urls) 
    
    print("已经拉取完第" , page + 1 , "页.")
    current_gif += len(gif_urls)
    print(current_gif / gif_amount * 100, "%的gif图片已经拉取.")

    time.sleep(10)
print("恭喜!已经拉取完毕所有数据,开始处理图片序列吧!")
