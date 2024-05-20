import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from sql_function import SQL_Function
from line_notify import Notify

class Crawler:
    def __init__(self):
        # 取得 comic_id 和 episode
        self.now = datetime.now()
        self.sql_function = SQL_Function()
        sql_function = SQL_Function()
        sql = "SELECT comics_id,episode FROM comics order by created_at desc"
        self.comics_ids = sql_function.sql_select(sql)
        self.headers = {
                    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'''
                }
        self.update_lists = list()
    
    def crawler(self) -> list():
        for comics_id in self.comics_ids:
            try:
                data = {
                    "comics_id":comics_id[0],
                    "episode":comics_id[1]
                }
                
                request = requests.get(f"https://m.manhuagui.com/comic/{data['comics_id']}/",headers=self.headers)
                soup = BeautifulSoup(request.text, 'html.parser')

                # title
                title_tag = soup.find_all("div", class_= "main-bar bar-bg1")
                piece_name = title_tag[0].string

                # episode
                cont_list = soup.find_all("div",class_="cont-list")[0].find_all("dl") #介紹列表
                update_episode = f"{cont_list[0].dd.string}"
                
                if data["episode"] == update_episode:
                    print(f"{comics_id} 已為最新集數")
                    time.sleep(5)
                    continue
                    
                # episode_update_time
                episode_update_time = f"{cont_list[1].dd.string}"
                
                # episode_url
                first_chatlist = soup.find_all("div",class_="chapter-list")
                episode_url = "https://m.manhuagui.com"+first_chatlist[0].a.get('href')
                self.update_lists.append([data['comics_id'],piece_name,update_episode,episode_url,episode_update_time])
                print(f"{comics_id} 已爬取!")
                time.sleep(5)
            except BaseException as e:
                print(f"{comics_id} 執行錯誤!" ,'錯誤原因：',e)
                time.sleep(5)
                continue
        
        return self.update_lists
    
    def update_comics(self,update_lists):
            # update sql episode
        for  update_list in update_lists:
            sql = f"""UPDATE comics SET name = '{update_list[1]}',
                    episode = '{update_list[2]}',
                    url = '{update_list[3]}',
                    is_run = 'N',
                    updated_at = '{self.now}' 
                    WHERE comics_id = '{update_list[0]}'"""
            self.sql_function.sql_update(sql)
            
if __name__ == "__main__":
    Crawler = Crawler()
    update_lists = Crawler.crawler()
    print(update_lists)