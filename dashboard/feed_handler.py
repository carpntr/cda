import logging
from subprocess import Popen, PIPE
from exchanges.binance.client import SocketManager


# def start_feeds():
#     """Shell out to data collection process"""
#     binance_feed = Popen('python exchanges/binance/stream.py')
#     logging.info('Feeds started')
#     return binance_feed

