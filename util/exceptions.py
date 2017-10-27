"""
Generalize exceptions to CDA
"""


class CDAException(Exception):
    """Base exception for all CDA throws"""
    msg = None

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def message(self):
        return str(self)

    def __str__(self):
        msg = self.msg.format(**self.kwargs)
        return msg

    __unicode__ = __str__
    __repr__ = __str__


class InvalidOrderBook(CDAException):
    """
    Raised when invalid update is passed to OrderBook
    """
    msg = 'Unrecognizable book update format: {bad_book}'

