# 保存到json文件时，斜杠前面都有一个反斜杠
import sqlite3
import os
import sys

class SaveData:
    def __init__(self, file_path, manga_info):
        
        self.manga_info = manga_info

        # 检查传入的路径是否存在
        absolute_path = os.path.abspath(file_path)
        dir_path = os.path.dirname(absolute_path)
        if not os.path.exists(dir_path):
            print(f'- Error：传入的路径"{absolute_path}"不存在，请检查')
            sys.exit(1)
        else:
            self.file_path = absolute_path

    def save(self):
        raise NotImplementedError("- Error：子类需要实现这个方法")

# 将数据保存到SQLite数据库中
class Save2DB(SaveData):
    def __init__(self, db_path, manga_info):
        super().__init__(db_path, manga_info)

        # 创建数据库连接
        self.db_connection = sqlite3.connect(self.file_path)

    # 将漫画数据保存到数据库中
    def save(self):
        try:

            self.manga_info.to_sql('manga', self.db_connection, if_exists='replace', index=False)
            self.db_connection.close()    
            print(f'+ 已保存到"{self.file_path}"')
        except Exception as e:
            print(f"- Error：保存到SQLite数据库时出错：{e}")

# 将数据保存到Json文件中
class Save2Json(SaveData):
    def save(self):
        try:
            self.manga_info.to_json(self.file_path, orient='records', force_ascii=False)
            print(f'+ 已保存到"{self.file_path}"')
        except Exception as e:
            print(f"- Error：保存到JSON文件时出错：{e}")

# 将数据保存到CSV文件中
class Save2CSV(SaveData):
    def save(self):
        try:
            self.manga_info.to_csv(self.file_path, index=False, encoding='utf-8-sig')
            print(f'+ 已保存到"{self.file_path}"')
        except Exception as e:
            print(f"- Error：保存到CSV文件时出错：{e}")
