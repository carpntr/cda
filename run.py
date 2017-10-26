from exchanges.binance.client import SocketManager

default_tickers = ['ETHBTC', 'BNBBTC', 'BQXBTC', 'LTCBTC']

if __name__ == "__main__":
    # Create binance socket manager and stream to mongodb called demo.dashboard
    binance_data_stream = SocketManager(symbols=default_tickers,
                                        data_lib='demo.dashboard')
    binance_data_stream.stream_orderbook(write=True)