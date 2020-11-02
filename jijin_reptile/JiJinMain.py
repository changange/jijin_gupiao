from jijin_reptile import SqlConnect as conn

import requests
import re
import time
import math
from pprint import pprint
from bs4 import BeautifulSoup as bs
import lxml

class TTJijin:
    def __init__(self):
        self.sql = conn.Mysql()
        self.now_time = time.strftime("%Y-%m-%d", time.localtime())

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Connection': 'keep - alive',
            'Host': 'fund.eastmoney.com',
            # 'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Cookie': 'em_hq_fls=js; intellpositionL=1522.39px; qgqp_b_id=26adb366b9ce54a3af72b184e86c1c6f; HAList=a-sh-600519-%u8D35%u5DDE%u8305%u53F0%2Ca-sh-600016-%u6C11%u751F%u94F6%u884C%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600570-%u6052%u751F%u7535%u5B50; intellpositionT=1355px; st_si=77026338903329; st_asi=delete; EMFUND0=09-17%2012%3A50%3A15@%23%24%u534E%u5B9D%u9999%u6E2F%u4E2D%u5C0F%28QDII-LOF%29A@%23%24501021; EMFUND1=09-17%2012%3A50%3A48@%23%24%u957F%u4FE1%u533B%u7597%u4FDD%u5065%u6DF7%u5408%28LOF%29@%23%24163001; EMFUND2=09-18%2013%3A54%3A51@%23%24%u5408%u7166%u667A%u8FDC%u91D1%u878D%u79D1%u6280%u6307%u6570%28LOF%29A@%23%24168701; EMFUND3=09-18%2014%3A05%3A56@%23%24%u535A%u65F6%u5929%u9890%u503A%u5238A@%23%24050023; EMFUND4=09-18%2014%3A14%3A09@%23%24%u91D1%u9E70%u533B%u7597%u5065%u5EB7%u4EA7%u4E1AA@%23%24004040; EMFUND5=10-16%2019%3A59%3A22@%23%24%u957F%u57CE%u6210%u957F%u5148%u950B%u6DF7%u5408A@%23%24010049; EMFUND6=10-17%2012%3A22%3A55@%23%24%u957F%u57CE%u533B%u7597%u4FDD%u5065%u6DF7%u5408@%23%24000339; EMFUND7=10-19%2021%3A21%3A10@%23%24%u62DB%u5546%u4E2D%u8BC1%u7164%u70AD%u7B49%u6743%u6307%u6570%u5206%u7EA7@%23%24161724; EMFUND8=10-22%2010%3A54%3A32@%23%24%u5E73%u5B89%u76C8%u4E30%u4E09%u4E2A%u6708%u6301%u6709%u6DF7%u5408%28FOF%29A@%23%24008461; EMFUND9=10-23 10:20:20@#$%u534E%u5B89%u4E2D%u8BC1%u94F6%u884C%u6307%u6570%u5206%u7EA7@%23%24160418; ASP.NET_SessionId=rwp3r5a43hvw00e5wj1feht4; st_pvi=45150682729837; st_sp=2020-09-16%2015%3A53%3A30; st_inirUrl=http%3A%2F%2F1234567.com.cn%2F; st_sn=2; st_psi=20201027145415798-0-1504809228'
            }

    #   打开基金列表
    def openJijinList(self):

        for i in range(1,100):
            #   基金类型
            jijin_tpye = 'FOF'

            res_list = []       # 基本信息
            res_com = []        #   属于哪个公司
            res_tpu = []        #   基金信息表
            res_shou = []       #   基金收益哦表
            sess = requests.Session()
            res = sess.get(f"http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=fof&rs=&gs=0&sc=zzf&st=desc&sd=2019-10-19&ed=2020-10-19&qdii=&tabSubtype=,,,,,&pi={i}&pn=100&dx=1&v=0.4260028191070855", headers=self.headers)
            res.encoding = res.apparent_encoding
            res_josn = res.text.split('[')[1]
            res_josn = res_josn.split(']')[0]
            res_josn = res_josn.replace(' ', '')
            res_josn = res_josn.replace('"', '')
            res = res_josn.split(',')

            for j in range(int(len(res)/25)):
                x=j*25
                y=(j+1)*25
                fenge = res[x:y]
                res_list.append(fenge)

            # print(res_list)
            if len(res_list) == 0:
                print('基金爬取已完成')
                return False

            #   属于哪个公司
            for j in range(len(res_list)):
                # print(res_list[j][0])
                res_ji = sess.get(f"http://fund.eastmoney.com/{res_list[j][0]}.html")
                res_ji.encoding = res_ji.apparent_encoding

                p = re.compile(r'\d{8}.html">(.*?)</a></td><td><a class')
                text = p.findall(res_ji.text)
                res_com.append(text)

            #   把基本信息和所属公司结合起来
            for z in range(len(res_list)):
                res_list[z].append(res_com[z][0])

            #   数据转换成元祖     基金list表
            for x in range(len(res_list)):
                tuple = (res_list[x][0],res_list[x][1],jijin_tpye,res_list[x][16],res_list[x][-1])
                res_tpu.append(tuple)
            print(res_tpu)
            try:
                #   插入数据库
                self.sql_conn = self.sql.connectMysql()
                sql_string = 'INSERT INTO jijin_list VALUES (%s,%s,%s,%s,%s)'
                self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_tpu)
            except Exception as e:
                print(e)

            #   数据转成元祖      基金历史收益表
            for y in range(len(res_list)):
                tuple_shou = (res_list[y][0],res_list[y][1],res_list[y][14],res_list[y][8],res_list[y][9],res_list[y][10],res_list[y][11],res_list[y][12],res_list[y][13],res_list[y][15],self.now_time)
                res_shou.append(tuple_shou)
            # print(res_shou)
            try:
                #   插入数据库
                self.sql_conn = self.sql.connectMysql()
                sql_string = 'INSERT INTO jijin_change_profit VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_shou)
            except Exception as e:
                pass



    #   基金管理人的变更
    def jijinMangeChange(self):
        self.sql_conn = self.sql.connectMysql()
        select_count = 'SELECT COUNT(*) FROM `jijin_list`'
        self.sql_select_res = self.sql.selectData(self.sql_conn, select_count)

        for i in range(math.ceil(self.sql_select_res[0][0]/100)):
            res_list = []
            x = i*100
            self.sql_conn = self.sql.connectMysql()
            select_count_con = f'SELECT jijin_id,jijin_name FROM jijin_list LIMIT {x},100'
            sql_select_res = self.sql.selectData(self.sql_conn, select_count_con)

            for j in sql_select_res:
                sess = requests.Session()
                res = sess.get(f"http://fund.eastmoney.com/{j[0]}.html", headers=self.headers)  # http://fund.eastmoney.com/160814.html
                res.encoding = res.apparent_encoding
                # pprint(res.text)

                soup = bs(res.text,'lxml')
                res_one = soup.find_all('tr')
                for i in res_one:
                    # print(i)
                    p = re.compile(r'manager/\d{8}.html">(.*?)</a>')
                    text = p.findall(str(i))
                    if len(text) !=0:
                        text = ','.join(text)
                        # print(text)

                    p_2 = re.compile(r'<td class="td01">(\d{0,4}-\d{0,2}-\d{0,2}.*?)</td>')
                    text_2 = p_2.findall(str(i))
                    if len(text_2) != 0:
                        text_2 = text_2
                        # print(text_2)

                    p_3 = re.compile(r'</td> <td class="td03">(.*?)</td>')
                    text_3 = p_3.findall(str(i))
                    if len(text_3) != 0:
                        text_3 = text_3
                        # print(text_3)

                    p_4 = re.compile(r'ui-color-red">(\d{1,}\..*%)</td></tr>')
                    text_4 = p_4.findall(str(i))
                    if len(text_4) != 0:
                        text_4 = text_4
                        # print(text_4)

                    if len(text) !=0 and len(text_2) != 0 and len(text_3) != 0 and len(text_4) != 0:
                        tup = (j[0], j[1],text, text_2[0], text_3[0], text_4[0],self.now_time)
                        res_list.append(tup)

            print(res_list)
            try:
                #   插入数据库
                self.sql_conn = self.sql.connectMysql()
                sql_string = 'INSERT INTO jijin_change_manage VALUES (%s,%s,%s,%s,%s,%s,%s)'
                self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_list)
            except Exception as e:
                pass



    #   基金的规模
    def jijinGuMo(self):
        self.sql_conn = self.sql.connectMysql()
        select_count = 'SELECT COUNT(*) FROM `jijin_list`'
        self.sql_select_res = self.sql.selectData(self.sql_conn, select_count)

        for i in range(math.ceil(self.sql_select_res[0][0] / 100)):
            res_list = []
            x = i * 100
            self.sql_conn = self.sql.connectMysql()
            select_count_con = f'SELECT jijin_id,jijin_name FROM jijin_list LIMIT {x},100'
            sql_select_res = self.sql.selectData(self.sql_conn, select_count_con)

            for j in sql_select_res:
                sess = requests.Session()
                res = sess.get(f"http://fund.eastmoney.com/{j[0]}.html", headers=self.headers)  # http://fund.eastmoney.com/588090.html
                res.encoding = res.apparent_encoding

                p = re.compile(r'基金规模</a>：(.*?)（')
                text = p.findall(res.text)

                p1 = re.compile(r'元（(.*?)）')
                text_1 = p1.findall(res.text)

                tup = (j[0],j[1],text[0],text_1[0])
                # print(tup)
                res_list.append(tup)
            print(res_list)

            try:
                #   插入数据库
                self.sql_conn = self.sql.connectMysql()
                sql_string = 'INSERT INTO jijin_change_scale VALUES (%s,%s,%s,%s)'
                self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_list)
            except Exception as e:
                print(e)



    #   基金分红
    def getJijineFenhong(self):
        self.sql_conn = self.sql.connectMysql()
        select_count = 'SELECT COUNT(*) FROM `jijin_list`'
        self.sql_select_res = self.sql.selectData(self.sql_conn, select_count)

        for i in range(math.ceil(self.sql_select_res[0][0] / 100)):
            x = i * 100
            self.sql_conn = self.sql.connectMysql()
            select_count_con = f'SELECT jijin_id,jijin_name FROM jijin_list LIMIT {x},100'
            sql_select_res = self.sql.selectData(self.sql_conn, select_count_con)

            for j in sql_select_res:
                res_tt = []

                xjfe = []
                sess = requests.Session()
                res = sess.get(f"http://fund.eastmoney.com/{j[0]}.html",
                               headers=self.headers)  # fund.eastmoney.com/160418.html
                res.encoding = res.apparent_encoding
                soup = bs(res.text, 'lxml')
                res_list = soup.find_all('li',id='position_bonus')

                res_sou = str(list(res_list)[0])
                p = re.compile(r'left;padding:2px;">(.*?)<span class="ui-color-red')
                text = p.findall(res_sou)
                # print(text)

                if len(text) == 0:
                    continue

                for xj in text:
                    if '份额' in xj:
                        xjfe.append('拆分')
                    if '现金' in xj:
                        xjfe.append('分红')
                # print(xjfe)

                res_sou = str(list(res_list)[0])
                p = re.compile(r'ui-color-red">(.*?)</span>')
                text_1 = p.findall(res_sou)
                # print(text_1)

                res_sou = str(list(res_list)[0])
                p = re.compile(r'</span>(.*?)</td></tr>')
                text_2 = p.findall(res_sou)
                # print(text_2)

                res_sou = str(list(res_list)[0])
                p = re.compile(r'padding:2px;">(\d{4}-\d{2}-\d{2})</td>')
                text_3 = p.findall(res_sou)
                # print(text_3)

                for c in range(len(text)):
                    res_inster = (j[0],j[1],xjfe[c],text_1[c],str(text_3[c]))
                    print(res_inster)
                    res_tt.append(res_inster)

                try:
                    #   插入数据库
                    self.sql_conn = self.sql.connectMysql()
                    sql_string = 'INSERT INTO jijin_fenhong VALUES (%s,%s,%s,%s,%s)'
                    self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_tt)
                except Exception as e:
                    print(e)





    #   基金的股票持仓信息
    def getJijinGupiaoCicang(self):
        self.sql_conn = self.sql.connectMysql()
        select_count = 'SELECT COUNT(*) FROM `jijin_list`'
        self.sql_select_res = self.sql.selectData(self.sql_conn, select_count)

        for i in range(math.ceil(self.sql_select_res[0][0] / 100)):
            x = i * 100
            self.sql_conn = self.sql.connectMysql()
            select_count_con = f'SELECT jijin_id,jijin_name FROM jijin_list LIMIT {x},100'
            sql_select_res = self.sql.selectData(self.sql_conn, select_count_con)

            for j in sql_select_res:
                res_list = []
                sess = requests.Session()
                res = sess.get(
                    f"http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={j[0]}&topline=100&year=2017&month=&rt=0.09047235666220055",
                    headers=self.headers)
                res.encoding = res.apparent_encoding
                # print(res.text)

                #   GP代码
                p = re.compile(r'\w{2}\d{6}.html\'>(.*?)</a>')
                text = p.findall(res.text)
                # print(len(text))

                #   占比
                p = re.compile(r'class=\'tor\'>(\d{1,}\.\d{1,}%{1}?)</td>')
                text_Z = p.findall(res.text)
                # print(len(text_Z))

                #   数量
                p = re.compile(r'\d{1}%</td><td class=\'tor\'>(\d{0,5},{0,1}\d{1,}\.{0,1}\d{1,})</td>')
                text_n = p.findall(res.text)
                # print(len(text_n))

                if len(text) == 0:
                    continue

                print("--------------")

                try:
                    for ji in range(int(len(text)/2)):
                        g_res = text[ji*2:ji*2+2]

                        res_tup = (j[0],j[1],g_res[0],g_res[1],text_Z[ji],text_n[ji],f'2017')
                        res_list.append(res_tup)
                    print(res_list)
                except Exception as e:
                    print(e)
                    continue


                try:
                    #   插入数据库
                    self.sql_conn = self.sql.connectMysql()
                    sql_string = 'INSERT INTO jijin_gupiao_chicang_2017_100 VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    self.sql_inster = self.sql.insertData(self.sql_conn, sql_string, res_list)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    t = TTJijin()
    t.getJijinGupiaoCicang()
    # print(math.ceil(5.4))