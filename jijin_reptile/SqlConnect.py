import pymysql

class Mysql:
    def __init__(self):
        pass

    ##  数据库连接
    def connectMysql(self):
        conn = pymysql.connect('172.16.1.100', user='root', passwd='320517gca',db='jijin_gupiao')
        cursor = conn.cursor()
        return [cursor,conn]

    ##  数据库插入数据
    def insertData(self,cur, sql, sql_data):
        insert = cur[0].executemany(sql,sql_data)
        cur[0].close()
        cur[1].commit()
        print(f'插入：{insert} 行的数据')



if __name__ == '__main__':
    mysql = Mysql()
    cour = mysql.connectMysql()
    mysql.insertData(cour,'INSERT INTO jijin_change_manage VALUES (%s,%s,%s,%s,%s,%s,%s)', [(7,1,1,1,1,1,1)])