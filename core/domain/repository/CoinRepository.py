from typing import List, Optional

from common.models import Coin


class CoinRepository:
    def __init__(self, session):
        self._session = session

    def create(self,  coin_name: str) -> Coin:
        coin = Coin(coin_name=coin_name)
        self._session.add(coin)
        self._session.commit()
        return coin 

    def find_by_coin_name(self, coin_name: str) -> Optional[Coin]:
        coin = self._session.query(Coin) \
            .filter_by(coin_name=coin_name) \
            .first()
        return coin