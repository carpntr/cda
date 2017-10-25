import arctic
import datetime
from arctic import Arctic
import pytz
from datetime import datetime as dt
import time

db = Arctic('localhost')
lib = db['binance.testbook']

for i in range(10):
    df = lib.read('ETHBTC', columns=['bid1', 'bid2', 'bid3', 'ask1', 'ask2', 'ask3'])
    print(df)
    time.sleep(4)