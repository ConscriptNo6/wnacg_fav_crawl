# 保存到json文件时，斜杠前面都有一个反斜杠
import sqlite3

# 将数据保存到SQLite数据库中
class Save2DB:
    def __init__(self, db_path, manga_info):
        self.db_path = db_path
        self.manga_info = manga_info

        # 创建数据库连接
        self.db_connection = sqlite3.connect(self.db_path)

    # 将漫画数据保存到数据库中
    def save(self):
        try:
            self.manga_info.to_sql('manga', self.db_connection, if_exists='replace', index=False)
            self.db_connection.close()    
        except Exception as e:
            print(f"保存到SQLite数据库时出错：{e}")

# 将数据保存到Json文件中
class Save2Json:
    def __init__(self, file_path, manga_info):
        self.file_path = file_path
        self.manga_info = manga_info

    def save(self):
        try:
            self.manga_info.to_json(self.file_path, orient='records', force_ascii=False)
        except Exception as e:
            print(f"保存到JSON文件时出错：{e}")

# 将数据保存到CSV文件中
class Save2CSV:
    def __init__(self, file_path, manga_info):
        self.file_path = file_path
        self.manga_info = manga_info

    def save(self):
        try:
            self.manga_info.to_csv(self.file_path, index=False, encoding='utf-8-sig')
        except Exception as e:
            print(f"保存到CSV文件时出错：{e}")
