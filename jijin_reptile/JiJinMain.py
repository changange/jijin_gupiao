import requests
import json

class TTJijin:
    def __init__(self):
        pass

    #   打开基金列表
    def openJijinList(self):
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN, zh;q=0.9',
                   'Connection': 'keep - alive',
                   'Host': 'fund.eastmoney.com',
                   'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                   'Cookie':'em_hq_fls=js; intellpositionL=1079.19px; intellpositionT=855px'
                   }

        for i in range(1,100):
            res_list = []
            sess = requests.Session()
            res = sess.get(f"http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc&sd=2019-10-19&ed=2020-10-19&qdii=&tabSubtype=,,,,,&pi={i}&pn=100&dx=1&v=0.582145995831324", headers=headers)
            res.encoding = res.apparent_encoding
            res_josn = res.text.split('[')[1]
            res_josn = res_josn.split(']')[0]
            res_josn = res_josn.replace(' ', '')
            res_josn = res_josn.replace('"', '')
            res = res_josn.split(',')

            for j in range(100):
                x=j*25
                y=(j+1)*25
                fenge = res[x:y]
                res_list.append(fenge)

            print(res_list)



    #   基金的股票持仓信息
    def getJijinGupiaoCicang(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Connection': 'keep - alive',
            'Host': 'fundf10.eastmoney.com',
            'Referer': 'http://fundf10.eastmoney.com/ccmx_161724.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }

        sess = requests.Session()
        res = sess.get(
            "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=161724&topline=10&year=2020&month=6&rt=0.5436186295862171",
            headers=headers)
        res.encoding = res.apparent_encoding
        print(res.text)


if __name__ == '__main__':
    t = TTJijin()
    t.openJijinList()