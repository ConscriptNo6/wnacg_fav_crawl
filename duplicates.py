class MangaDuplicate:
    def __init__(self, manga_info_df):
        self.manga_info_df = manga_info_df

    def duplicates(self):
        # 标记所有重复行
        is_duplicate = self.manga_info_df.duplicated(['id'], keep=False)
        duplicates_df = self.manga_info_df[is_duplicate]

        # 按传入的subset列排序
        sorted_df = duplicates_df.sort_values(by=['id'])
        
        return sorted_df
