import datetime, threading, time, traceback, os
from upbitpy import Upbitpy
from common.models import Session
from domain.repository.CoinRepository import CoinRepository
from domain.repository.CoinRecordRepository import CoinRecordRepository
from domain.repository.AlarmRepository import AlarmRepository
from domain.service.SlackService import SlackService

class CoreWorker:
    def __init__(self, timer=60, ratio_threshold=0.1):
        self._ratio_threshold = ratio_threshold
        self._timer = timer
        self._temp_alarm_candidates = {}


    def run(self):
        while True:
            try:
                self._check()
            except Exception:
                ex = traceback.format_exc()
                print(ex)
            finally:
                time.sleep(self._timer)

    def _check(self):
        print(datetime.datetime.now())
        try:
            db_session = Session()
            coin_repository = CoinRepository(db_session)
            coin_record_repository = CoinRecordRepository(db_session)
            alarm_repository = AlarmRepository(db_session)
            slack_service = SlackService()
            upbit = Upbitpy()

            # 모든 market 얻어오기
            all_market = upbit.get_market_all()

            # market 분류
            market_table = { 'KRW': [] }
            for m in all_market:
                for key in market_table.keys():
                    if m['market'].startswith(key):
                        market_table[key].append(m['market'])

            # 마켓 별 가격을 가져와 출력
            for key in market_table.keys():
                tickers = upbit.get_ticker(market_table[key])
                for it in tickers:
                    if it['market'].startswith('KRW'):
                        coin_name = it['market'].replace('KRW-', '')
                        coin = coin_repository.find_by_coin_name(coin_name)
                        if not coin:
                            coin = coin_repository.create(coin_name)

                        coin_record = coin_record_repository.get_price_by_coin_id(coin.id)
                        

                        if coin_record:
                            prev_trade_price = coin_record.trade_price
                            current_trade_price = it['trade_price']
                            increase_ratio = current_trade_price / prev_trade_price - 1
                            if increase_ratio > self._ratio_threshold:
                                print(coin.coin_name, increase_ratio, 'INCREASE!')
                                if self._temp_alarm_candidates.get(coin_name) != 1:
                                    self._temp_alarm_candidates[coin_name] = 1
                                else:
                                    detail_text = '[{}] 2회 연속 {}초마다 {}% 이상 가격 상승'.format(
                                        coin_name,
                                        int(self._timer),
                                        (self._ratio_threshold * 100))
                                    print(detail_text)
                                    alarm_repository.create(
                                        coin_id=coin.id, 
                                        detail_text=detail_text
                                    )
                                    slack_service.post_to_slack(detail_text)                                
                            else:
                                self._temp_alarm_candidates[coin_name] = 0

                        coin_record_repository.create_or_update(
                            coin_id=coin.id,
                            trade_price=it['trade_price']
                        )

        except Exception:
            traceback.print_exc()
        finally:
            db_session.close()


        

       



if __name__ == '__main__':
    core_worker = CoreWorker(
        timer=60,
        ratio_threshold=0.1)
    core_worker.run()
