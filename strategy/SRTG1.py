




# 1min 涨幅超过3个点，。就是符合这个模型。这个量化规则其实很简单。

# 每个线程只处理一个stock ,3000,  不用考虑空，平仓是在早上开盘时候进行的。一开盘就清仓不管赚赔，全部清仓。


class pdata():
    low = 1
    high = 2
    time= 3
    pct  = 3.2
    code = '000009'


l = [pdata(),pdata()]



class strg1():
    def __init__(self, stock):
        self.stock = stock

    def calc(self):
        if self.stock.pct >= 3 :
            queue.put("buy"+ self.stock.code)






if __name__ == '__main__':

    for stoc in l:
        strg1(stoc).calc()