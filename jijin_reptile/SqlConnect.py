import pymysql
import math

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
        # insert = cur[0].executemany(sql,sql_data)
        for i in range(len(sql_data)):
            try:
                insert = cur[0].execute(sql,sql_data[i])
            except Exception as e:
                print(e)

        cur[0].close()
        cur[1].commit()
        print(f'插入数据完成')

    ##  数据库查询
    def selectData(self,cur, sql):
        try:
            cur[0].execute(sql)
            results = cur[0].fetchall()
        except Exception as e:
            print(e)

        cur[1].close()
        return results


if __name__ == '__main__':
    mysql = Mysql()
    cour = mysql.connectMysql()
    # mysql.insertData(cour,'INSERT INTO jijin_change_manage VALUES (%s,%s,%s,%s,%s,%s,%s)', [(9,1,1,1,1,1,1)])
    mysql.selectData(cour, 'SELECT jijin_id,jijin_name FROM jijin_list LIMIT 0,100')
