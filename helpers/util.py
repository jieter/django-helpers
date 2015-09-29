class Wrapper(object):
    '''
    Wrapper proxies all attribute requests to the wrapped class
    But allows adding extra fuctionality
    '''
    def __init__(self, wrapped):
        object.__setattr__(self, 'inner', wrapped)

    def __getattr__(self, attr):
        return getattr(self.inner, attr)

    def __setattr__(self, attr, value):
        setattr(self.inner, attr, value)
