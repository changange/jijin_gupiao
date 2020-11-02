from jijin_reptile import SqlConnect as conn

import requests
import re
import time

class TTGuPiao:
    def __init__(self):
        self.sql = conn.Mysql()

    #   打开股票列表
    def openGuPiaoList(self):
        now_time = time.strftime("%Y-%m-%d", time.localtime())

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Connection': 'keep - alive',
            'Host': 'fund.eastmoney.com',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Cookie': 'em_hq_fls=js; intellpositionL=1079.19px; intellpositionT=855px'
            }

        for i in range(1, 100):
            gp_type = '科创板'
            res_g = []

            sess = requests.Session()
            res = sess.get(
                f"http://push2.eastmoney.com/api/qt/clist/get?pn={i}&pz=100&po=0&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid=f12&fid0=f4001&fields=f2,f3,f12,f13,f14,f62,f184,f225,f165,f263,f109,f175,f264,f160,f100,f124,f265&fs=m:1+t:23+f:!2&rt=53441769&cb=jQuery183039452473458091974_1603246664724&_=1603253096766",
                headers=headers)
            res.encoding = res.apparent_encoding

            # if '"data":null' in res.text:
            #     print('股票已爬取完成')
            #     return False

            res_josn = res.text.split('diff":[{')[1]
            res_josn = res_josn.split('}]}})')[0]

            res_list = res_josn.split('},{')

            for z in range(len(res_list)):
                res_x = res_list[z].split(',')
                x1 = res_x[2].split(':"')[1]
                x1 = x1.split('"')[0]

                x2 = res_x[4].split(':"')[1]
                x2 = x2.split('"')[0]

                x3 = res_x[6].split(':"')[1]
                x3 = x3.split('"')[0]

                y = (x1, x2, x3, gp_type)

                res_g.append(y)
            print(res_g)
            self.sql_conn = self.sql.connectMysql()
            sql_string = 'INSERT INTO gupiao_list VALUES (%s,%s,%s,%s)'
            self.sql_inster = self.sql.insertData(self.sql_conn, sql_string,res_g)


if __name__ == '__main__':
    tt = TTGuPiao()
    tt.openGuPiaoList()