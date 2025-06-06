import fav_crawl
import save2file
import duplicates

'''------------------必需------------------'''

# 实例化一个爬虫对象，并传入账号、密码、线程数、代理端口号
fc = fav_crawl.FavCrawl('yajuusenpai', '114514', threads=20, port='7897')
# 登录
fc.login()

# 获取所有收藏的漫画的信息
manga_info_df = fc.get_full_manga_info() 

'''------------------可选------------------'''

# 1.对收藏的漫画进行查重
md = duplicates.MangaDuplicate(manga_info_df)
result = md.duplicates()
print(result)

# 2.保存到SQLite文件
sv1 = save2file.Save2DB('./data_files/exemple.db', manga_info_df)
sv1.save()

# 3.保存到JSON文件
sv2 = save2file.Save2Json('./data_files/exemple.json', manga_info_df)
sv2.save()

# 4.保存到CSV文件
sv3 = save2file.Save2CSV('D:/Python Program/wnacg_fav_crawl/data_files/exemple.csv', manga_info_df)
sv3.save()
