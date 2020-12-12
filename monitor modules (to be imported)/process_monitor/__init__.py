import multiprocessing

class Monitor(object):
    ''' Monitor class for thread sychronization,
        protected with a multiprocessing.Lock() by default

    when you inherit from this class:
    . in you __init__, you should set up the monitor's _lock like this:
        - self._init_lock() #auto generated lock
      or with your lock:
        - self._init_lock(lock = you_lock)


    . you can simply init your 'Condition' object like this :
        self.cond = self.Condition()

    '''

    def __init__(self, lock = multiprocessing.Lock()):
        ''' initializes the _lock, multiprocessing.Lock() is used by default '''
        self._lock = lock
        

    def Condition(self):
        ''' returns a condition bound to this monitor's lock'''
        return multiprocessing.Condition(self._lock)

    init_lock = __init__