import arctic
from arctic import Arctic
import pytz
from pprint import pprint
from datetime import datetime as dt

est = pytz.timezone('US/Eastern')

# Connect to mongo
def initialize_db():
    db = Arctic('localhost')
    # db.delete_library('binance.orderbook')
    libs = db.list_libraries()
    if 'binance.orderbook' not in libs:
        print('No binance orderbook tickstore -- creating one')
        db.initialize_library('binance.orderbook',lib_type=arctic.TICK_STORE)
    return db


to_convert = {'bids': {'0.00022113': '51.00000000',
                       '0.00022084': '425.00000000',
                       '0.00022083': '1042.00000000',
                       '0.00022081': '728.00000000',
                       '0.00022080': '3755.00000000',
                       '0.00022001': '102.00000000',
                       '0.00022000': '35.00000000',
                       '0.00021780': '774.00000000',
                       '0.00021760': '87.00000000',
                       '0.00021512': '4648.00000000'
                       },
              'asks': {'0.00022296': '990.00000000',
                       '0.00022300': '172.00000000',
                       '0.00022401': '126.00000000',
                       '0.00022500': '100.00000000',
                       '0.00022571': '844.00000000',
                       '0.00022578': '126.00000000',
                       '0.00022670': '5.00000000',
                       '0.00022680': '7.00000000',
                       '0.00022685': '194.00000000',
                       '0.00022728': '87.00000000'
                       },
              'id': 12206256,
              'timestamp': 1508962755251
              }

import random
def format_book(d):
    a = {}
    a['index'] = dt.fromtimestamp((d['timestamp'] + random.randint(0,100))/1000.0, tz=est)
    a['depth_id'] = d['id']
    for n, bid in enumerate(d['bids'].items()):
        a[f'bid{n}'] = bid[0]
        a[f'bid{n}_ammt'] = bid[1]
    for n, ask in enumerate(d['asks'].items()):
        a[f'ask{n}'] = ask[0]
        a[f'ask{n}_ammt'] = ask[1]
    return [a]

db = initialize_db()

lib = db['binance.orderbook']
#lib.write('BNBBTC', format_book(to_convert))

print(lib.read('BNBBTC', columns=['bid1','bid2','bid3','ask1','ask2','ask3']))