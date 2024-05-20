import pymysql
import setting

# Mysql connection

class SQL_Function:
    def __init__(self):
        pass
    
    def connect(self):
        conn = pymysql.connect(
            host = setting.MYSQL_HOST, 
            db = setting.MYSQL_DB, 
            user = setting.MYSQL_USERNAME,
            password = setting.MYSQL_PASSWORD, charset='utf8', use_unicode=True)
        cursor = conn.cursor()
        return conn,cursor
        
    def sql_select(self,sql) -> tuple():
        conn,cursor = self.connect()
        cursor.execute(sql)
        datas = cursor.fetchall()
        conn.close()
        cursor.close()
        return datas
    
    def sql_update(self,sql) -> bool():
        conn,cursor = self.connect()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    def sql_delete(self,sql) -> bool():
        conn,cursor = self.connect()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        cursor.close()
        return True                
