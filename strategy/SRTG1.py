
import abc

from engine import BacktestEngine, Event, EVENT_TRADE

class Strategy():
    @abc.abstractmethod
    def calc(self, event):
        pass


class Buyallin(Strategy):
    def calc(self, event):
        print(event.data.symbol)

        if event.data.close_price < 3:
            print("test")
            e.put(Event(type="test"))

def excute(event):
    print("buy11111")





if __name__ == '__main__':
   e = BacktestEngine()
   e.register(EVENT_TRADE, Buyallin().calc)
   e.register("test", excute)
   print(e._handlers)
   e.start()