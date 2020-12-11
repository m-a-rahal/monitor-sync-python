import threading

class Monitor(object):
    def __init__(self, lock = threading.Lock()):
        self._lock = lock # monitor's lock (mandatory)
        #-----------------------------------------------------------------------
        '''when you inherit from this class, you can simply init your 'Condition' object like this :
        self.cond = self.Condition()
        '''

    def Condition(self):
        ''' returns a condition bound to this monitor's lock 
        see doc of threading.Condition : 'https://docs.python.org/3/library/threading.html#condition-objects' '''
        return threading.Condition(self._lock)