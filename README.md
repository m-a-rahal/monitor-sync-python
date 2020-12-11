
# Introduction
In this turorial, i'll show you how you can use 'monitors' for threading synchronization,
beleive it or not, it's rather easy, and it seems (to me at least) that it's more powerful than in other languages

# Monitor class 

''' this is the main class we'll be usinng, we'll inherit from it to make life easier '''
import threading

class Monitor(object):
    def __init__(self, lock = threading.Lock()):
        self._lock = lock # monitor's lock

    def Condition(self):
        ''' returns a condition bound to this monitor's lock. See doc of threading.Condition : 'https://docs.python.org/3/library/threading.html#condition-objects' '''
        return threading.Condition(self._lock)


#--- how to define a monitor --------------------------------------------------------------------------------------------------

class Monit_Class(Monitor):
    def __init__(self):
        super().__init__()

# simple, just don't forget call super().__init__()

#--- now let's add some conditions --------------------------------------------------------------------------------------------------

class Monit_Class(Monitor):
    def __init__(self):
        super().__init__()
        cond1 = self.Condition()

''' voila! this creates a 'Condition' object bound to this monitor's lock 
coditions are objects that implement the famous 'wait()' and 'notify()' methods
'''

#--- let's add some methods --------------------------------------------------------------------------------------------------
# to add a method, you should protect the a method using the lock
class Monit_Class(Monitor):
    def method(self):
        with self._lock:
            pass # your code here

#--- caustion! --------------------------------------------------------------------------------------------------
''' if you want to define internal methods that are called inside a monitor (from other methods)
    you might want to either:
    1) use the monitor with a RLock:'''
monitor = Monit_Class(threading.RLock())

''' 2) or define these methods as hidden, and don't use lock in them'''
class Monit_Class(Monitor):
    def _method(self):
        pass
''' 3) other solution? you can get creative, just be careful with it'''

#==================================================================================================
#===  entrance and exit protocols ==================================================================================================
#==================================================================================================

# usually, monitors provide 'entrance' and 'exit' protocols to entering a critical section
# Example:
    
monitor.enter_protocol()
<critical section>
monitor.exit_protocol()

# in this case, it`s really more useful to define the entrance and exit protocol methods as such:
class monitor():
    def __enter__(self):
        with self._lock:
            pass
        
    def __exit__(self, type, value, traceback):
        with self._lock:
            pass

# now, the syntax before simpler and safer !
    with monitor: 
        <critical section>
''' the 'with' keyword ensures the __exit__ method is 
    ALWAYS called, no matter what (exception, return, break, ... etc)
    so use this whenever you have the chance to
    after all, monitors purpose is making the code simpler and less prone to bugs
'''
