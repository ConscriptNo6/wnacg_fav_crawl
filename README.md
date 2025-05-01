## [绅士漫画](wnacg.com)收藏夹爬虫

绅士漫画的收藏夹没有查重功能，索性直接将收藏夹中所有漫画的信息爬取下来，在数据库或表格等中实现查重等功能。

### 使用
1.实例化一个爬虫对象，传入账号、密码、代理端口(不使用代理可不填)
```python
ded = fav_crawl.wnacg_dedu('account', 'password', 'proxy_port')
```
2.登录
```python
ded.login()
```
3.获取收藏夹内所有漫画的信息，并转换成Pandas DataFrame格式
```python
df = ded.get_manga_info() 
```
4.保存到本地文件
```python
# 保存到SQLite数据库
sv1 = save2file.Save2DB('./example.db', dataframe)
sv1.save()

# 保存为JSON格式的文件
sv2 = save2file.Save2Json('./example.json', dataframe)
sv2.save()

# 保存为CSV格式的文件
sv3 = save2file.Save2CSV('./example.csv', dataframe)
sv3.save()
```
### 实例
```python
import crawl
import save2file

ded = crawl.wnacg_dedu('yajuusenpai', '114514', '10808')
ded.login()
df = ded.get_manga_info() 

sv = save2file.Save2DB('./example.db', df)
sv.save()
```
