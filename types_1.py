import abc
from typing import Literal, Optional

Merchant = Literal['coles', 'woolies', 'iga']


class Product(abc.ABC):
    merchant: Merchant

    @property
    @abc.abstractmethod
    def display_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def price(self) -> Optional[float]:
        pass

    @property
    @abc.abstractmethod
    def is_on_special(self) -> Optional[bool]:
        pass

    @property
    @abc.abstractmethod
    def link(self) -> str:
        pass

    def __lt__(self, other: 'Product'):
        # n.b. all that's required for sorted()/.sort()
        return (self.price or 1e6) < (other.price or 1e6)  # default to big number when no price available


ProductOffers = dict[str, list[Product]]  # {'product_name': [Product, ...]}