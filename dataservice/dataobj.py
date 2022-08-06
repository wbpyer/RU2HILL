"""
Basic data structure used for general trading function in the trading platform.
"""
import time
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseData:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    gateway_name: str


@dataclass
class BarData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """

    symbol: str
    # exchange: Exchange
    datetime: datetime

    # interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_interest: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    # def __post_init__(self) -> None:
    #     """"""
    #     self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"


