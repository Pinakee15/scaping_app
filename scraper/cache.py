from abc import ABC, abstractmethod
import redis
import json
from typing import Optional

class CacheInterface(ABC):
    @abstractmethod
    def get_price(self, product_title: str) -> Optional[float]:
        pass

    @abstractmethod
    def set_price(self, product_title: str, product_price: float):
        pass

class RedisCache(CacheInterface):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_price(self, product_title: str) -> Optional[float]:
        price = self.client.get(product_title)
        return float(price) if price else None

    def set_price(self, product_title: str, product_price: float):
        self.client.set(product_title, product_price)

