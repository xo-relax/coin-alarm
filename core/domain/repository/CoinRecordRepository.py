from typing import List, Optional
from datetime import datetime
from common.models import CoinRecord


class CoinRecordRepository:
    def __init__(self, session):
        self._session = session

    def create_or_update(self, coin_id: int, trade_price: float) -> CoinRecord:
        coin_record = self._session.query(CoinRecord) \
            .filter_by(coin_id=coin_id) \
            .first()
        if coin_record:
            coin_record.trade_price = trade_price
            coin_record.last_updated_at = datetime.now()
            self._session.commit()
        else:
            coin_record = CoinRecord(
                coin_id=coin_id,
                trade_price=trade_price
                )
            self._session.add(coin_record)
            self._session.commit()
        return coin_record


    def get_price_by_coin_id(self, coin_id: int) -> Optional[CoinRecord]:
        coin_record = self._session.query(CoinRecord) \
            .filter_by(coin_id=coin_id) \
            .first()
        return coin_record
