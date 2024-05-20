from crawler import Crawler
from line_notify import Notify
from datetime import datetime
from sql_function import SQL_Function

if __name__ == "__main__":
    Crawler = Crawler()
    update_lists = Crawler.crawler()
    Crawler.update_comics(update_lists)
    notify = Notify()
    notify.send_notify()
    sql_function = SQL_Function()
    sql = "UPDATE comics SET is_run = 'Y'"
    sql_function.sql_update(sql)


