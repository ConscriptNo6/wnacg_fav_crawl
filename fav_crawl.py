import requests
import sys
from lxml import etree
import re
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

class FavCrawl:
    def __init__(self, account, password, threads=10, port=None,):
        self.headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
            }
        self.form_data = {
            "normal": "1",
            "login_name": account,
            "login_pass": password,
            }
        self.proxies = {
            'http': f'http://127.0.0.1:{port}',
            'https': f'http://127.0.0.1:{port}',
            } if port else None # 如果不传入端口则不使用代理
        self.num_of_threads = threads
        self.session = requests.Session()

    # 登录
    def login(self):
        print('* 登录中...')
        
        # 登录url
        # login_url = 'https://wnacg.com/users-login.html'
        # 检查登录状态url
        check_url = 'https://wnacg.com/users-check_login.html'

        # 登录请求可有可无
        # login_result = self.session.post(login_url, self.form_data, headers = self.headers, proxies = self.proxies)
        # 发起登录状态检查请求，可以同时完成登录和检查
        check_result = self.session.post(check_url, self.form_data, headers = self.headers, proxies = self.proxies)
 
        # 根据返回的布尔值判断是否登录成功
        check_result_json = json.loads(check_result.text)
        if check_result_json['ret']:
            print('+ 登录成功')
        else:
            print('- Error：登录失败，请检查账号或密码是否输入正确')
            sys.exit(1)

    # 网页解析
    def page_parse(self, url):
        response = self.session.get(url, headers = self.headers, proxies = self.proxies)
        root_element = etree.HTML(response.text)
        return root_element
    
    # 获取每一页中所有漫画的信息
    def get_manga_info_from_page(self, page):
        # 创建一个空列表用于存储所有漫画的信息
        fulldata_list = []
        
        print(f'+ 正在抓取第{page}页', end='\r', flush=True)

        page_result = self.page_parse('https://wnacg.com/users-users_fav-page-%s-c-0.html'%page)
        manga_parse = page_result.xpath('//div[@class="asTB"]')
        for i in range(len(manga_parse)): # 若最后一页漫画不足则会报错，需要获取最后一页的漫画数量
            
            try:
                # 剥离漫画的各项信息
                manga_thumb_url = manga_parse[i].xpath('//div[@class="asTB"]/div[1]/div/img/@src')[0] # 漫画封面略缩图url
                manga_name = manga_parse[i].xpath('.//p[@class="l_title"]/a/text()')[0] # 漫画名称                
                manga_category = manga_parse[i].xpath('.//div[2]/p[1]/a/text()')[0] # 所在收藏夹
                manga_addtime = str(manga_parse[i].xpath('.//div[2]/p[1]/span/text()')[0]) # 漫画添加时间，返回值是xpath元素
                manga_url = 'https://wnacg.com' + manga_parse[i].xpath('.//p[@class="l_title"]/a/@href')[0] # 漫画url
                manga_id = re.search(r'[0-9]{1,7}',manga_url).group() # 漫画的id，返回值是字符串                 
                manga_location = f'第{page}页，第{i + 1}个' # 漫画在收藏夹中的位置
            except Exception as e:
                print('- Error：出现错误，可能是原网页的html结构发生变化')
                print(e)
            
            # 将漫画的信息封装成字典并存储到metadata_list中
            manga_info = {'thumb_url': manga_thumb_url, 'id': manga_id, 'name': manga_name, 'category': manga_category, 'add_time': manga_addtime, 'url': manga_url, 'location': manga_location}
            fulldata_list.append(manga_info)
    
        return fulldata_list

    # 获取收藏夹所有漫画的信息
    def get_full_manga_info(self):
        fulldata_list = []

        # 请求收藏夹页面
        fav_page = self.page_parse('https://wnacg.com/users-users_fav.html')

        # 寻找最后一页页码
        last_page = fav_page.xpath('//div[@class="f_left paginator"]/a[5]/text()')
        total_pages = int(last_page[0])

        with ThreadPoolExecutor(max_workers=self.num_of_threads) as executor:
            results = executor.map(self.get_manga_info_from_page, range(1, total_pages + 1))
            
            for result in results:
                fulldata_list.extend(result)

        print(f"+ 共抓取到{total_pages}页，{len(fulldata_list)}个漫画")

        # 将漫画信息转换成Pandas DataFrame并返回
        return pd.DataFrame(fulldata_list)
