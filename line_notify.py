import setting
import requests
from sql_function import SQL_Function


class Notify:
    def __init__(self):
        sql = "SELECT name,episode,url,updated_at FROM comics WHERE is_run = 'N' "
        self.sql_function = SQL_Function()
        self.update_lists = self.sql_function.sql_select(sql)
        self.line_notify_token = setting.LINE_NOTIFY_TOKEN
        self.headers = {
            "Authorization": "Bearer " + self.line_notify_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
    def send_notify(self) -> bool():
        for update_list in self.update_lists:
            params = {"message":"\n" + "piece_name：" + 
                    update_list[0] + "\n" + 
                    "update_episode：" + update_list[1] + "\n" + 
                    "episode_update_time：" + str(update_list[3])
                    + "\n" + "episode_url：" + update_list[2]}
            r = requests.post("https://notify-api.line.me/api/notify",
                            headers=self.headers, params=params)
        return True
    
    
    
if __name__ == "__main__":
    notify = Notify()
    notify.send_notify()
    sql_function = SQL_Function()
    sql = "UPDATE comics SET is_run = 'Y'"
    sql_function.sql_update(sql)