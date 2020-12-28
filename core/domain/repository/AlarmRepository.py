from typing import List, Optional

from common.models import Alarm


class AlarmRepository:
    def __init__(self, session):
        self._session = session

    def create(self,  coin_id: str, detail_text: str) -> Alarm:
        alarm = Alarm(
            coin_id=coin_id, 
            detail_text=detail_text
        )
        self._session.add(alarm)
        self._session.commit()
        return alarm
