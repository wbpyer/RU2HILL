



def save_data(data):

    with open("stock_data_%s.csv", "a+", encoding='utf-8') as f:
        f.write("code,name,price,changepercent,change,volume,amount,amplitude,turnoverrate,pe,volumerate,high,low,open,close,pb\n")
        for i in data:
            Code = i["f12"]
            Name = i["f14"]
            Close = i['f2']
            ChangePercent = i["f3"]
            Change = i['f4']
            Volume = i['f5']
            Amount = i['f6']
            Amplitude = i['f7']
            TurnoverRate = i['f8']
            PERation = i['f9']
            VolumeRate = i['f10']
            Hign = i['f15']
            Low = i['f16']
            Open = i['f17']
            PreviousClose = i['f18']
            PB = i['f22']
            row = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                Code,Name,Close,ChangePercent,Change,Volume,Amount,Amplitude,
                TurnoverRate,PERation,VolumeRate,Hign,Low,Open,PreviousClose,PB)
            f.write(row)
            f.write('\n')


def take_dongfang():
    import requests
    import json

    for i in range(1, 3):
        print("抓取网页%s" % str(i))
        url = "http://48.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402508937289440778_1658838703304&pn=%s&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305" % str(i)
        res = requests.get(url)
        result = res.text.split("jQuery112402508937289440778_1658838703304")[1].split("(")[1].split(");")[0]
        result_json = json.loads(result)
        stock_data = result_json['data']['diff']
        for i in stock_data:
            print(i["f12"],i["f2"])
        return stock_data
        # save_data(stock_data, )
        #每次拉时候都会去拉到最新的数据，也就是说时间上来看就是你设置多长时间，就是多长时间拉一次。

if __name__ == '__main__':
    for i in take_dongfang():
        print(i)
    import datetime
    print(datetime.datetime.now())