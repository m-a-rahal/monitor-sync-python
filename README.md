# Introduction

Monitors make synchronization so easy and less prone to bugs. Sadly, I couldn't find any implementation for them in python on the internet (at least not in the first google search page 😝).  
turns out, not only is it possible, but it's really simple and so powerful !  
  
So, in this tutorial, I'll show a way I found to easily implement and use them  
hope you find it useful

# Monitor class

this is the main class, we'll just inherit from it to make life easier:

```python
import threading

class Monitor(object):
    def __init__(self, lock = threading.Lock()):
        ''' initializes the _lock, threading.Lock() is used by default '''
        self._lock = lock


    def Condition(self):
        ''' returns a condition bound to this monitor's lock'''
        return threading.Condition(self._lock)

    init_lock = __init__
```

## How to define a monitor

```python
class My_Monitor_Class(Monitor):
    def __init__(self):
        self.init_lock()

# or pass your own lock

class My_Monitor_Class(Monitor):
    def __init__(self, lock):
        self.init_lock(lock)
```

simple, we just inherit form the `Monitor` class, just don't forget call `self.init_lock()`

## Monitor 'Condition' objects

```python
class My_Monitor_Class(Monitor):
    def __init__(self):
        self.init_lock(lock)
        cond1 = self.Condition()
```

this creates a 'Condition' object bound to this monitor's lock

conditions are objects that implement the famous `wait()` and `notify()` methods_(see their doc: _<https://docs.python.org/3/library/threading.html#condition-objects>_)_

## Monitor methods

to add a method, you should protect the a method using the monitor's lock

```python
class My_Monitor_Class(Monitor):
    def method(self):
        with self._lock:
            # your code here
```

### Caution ⚠

if you want to define **private methods** that are only called inside a monitor, you should either:

1- use the monitor with an `RLock` _(see this helpful link about R-Locks: _<https://stackoverflow.com/questions/16567958/when-and-how-to-use-pythons-rlock>_)_

2- define these methods as hidden, and don't use lock in them

```python
class My_Monitor_Class(Monitor):
    def _method(self): #leading underscore (_) to indicate it's a private method
        # your code here
```

3- or maybe other solutions … you can get creative

# Entrance and Exit protocols

usually, monitors provide 'entrance' and 'exit' protocols to entering a critical section.

**Example:**

```python
monitor.enter_protocol()
<critical section>
monitor.exit_protocol()
```

in this case, it's really more useful to define the entrance and exit protocol methods as follows:

```python
class monitor(Monitor):
    def __enter__(self):
        with self._lock:
            # enter_protocol code here

    def __exit__(self, type, value, traceback):
        with self._lock:
            # exit_protocol code here
```

now, the syntax becomes simpler and safer !

```python
with monitor:
    <critical section>
```

the 'with' keyword ensures the **exit** method is ALWAYS called, no matter what (exception, return, break, … etc). So use this whenever you have the chance to. After all, the purpose of monitors is to make the code simpler and less prone to bugs

# That's it

you can also check the folder `# example of usage` to see how to apply

these concepts in more details

_Thanks for reading :)_

