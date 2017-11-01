from exchanges.binance.client import SocketManager

default_tickers = ['WTCBTC', 'NEOBTC', 'ETHBTC','BCCBTC', 'EVXBTC', 'LTCBTC',
                   'QTUMBTC', 'STRATBTC', 'OMGBTC', 'IOTABTC']

if __name__ == "__main__":
    # Create binance socket manager and stream to mongo instance called demo.dashboard
    binance_data_stream = SocketManager(symbols=default_tickers,
                                        data_lib='demo.dashboard')
    binance_data_stream.stream_orderbook(write=True)