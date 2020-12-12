import threading
import time
import os
import sys
import random
from datetime import datetime
random.seed(datetime.now())

def go_to_parent_dir():
    import sys, os
    sys.path.insert(1, os.path.join(sys.path[0], '..'))


def run_as_thread(func):
    ''' returns the thread to the function ! so you can gather them out in a list or something :3'''
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()
        return t
    return wrapper

class easy_dictionairy(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Car(object):
    states = easy_dictionairy( # defines car states (i used symbols to be able to visualize the cars in real time :] )
        outside  = '.',
        entering = '■',
        parking  = '░',
        exiting  = 'X'
    ) 
    
    def __init__(self, id):
        self.id = id
        self.state = Car.states.outside # a car starts outside

    def get_in(self):
        self.state = Car.states.entering
        sleep_for_cycles(5)

    def stay_in_park(self):
        self.state = Car.states.parking
        sleep_for_cycles(100)

    def get_out(self):
        self.state = Car.states.exiting
        sleep_for_cycles(5)
        self.state = Car.states.outside

    




help_str = '''
car state  | meaning
-----------+-----------------------------------------
  {}        | car is outside park
  {}        | car is getting in (from entrance door)
  {}        | car is inside park
  {}        | car is getting out (from exit door) 


'''.format(*Car.states.values())

logger_timestep = 0.02


def sleep_for_cycles(cyles):
        t = (random.random()*cyles + 2)*logger_timestep # min = 2*logger time step
        time.sleep(t)
        return t

def print_states(cars, park):
    t = 0
    print(help_str)
    print('                  --- cars ---                           --- occupied places + time ---')
    txt = ' '.join([chr(ord('A')+i) for i in range(len(cars))]) # print car names
    print(txt)
    while True:
        txt = ' '.join([car.state for car in cars] + ['\t {}\t\t\t\ttime-step = {}'.format(park.get_occupied_places(), t)])
        time.sleep(logger_timestep)
        yield print(txt)
        t += 1


@run_as_thread
def state_logger(cars, park, stop_func = lambda : False):
    print_state = print_states(cars, park)
    while True:
        next(print_state) # prints one state
        if stop_func(): # nice way to stop a thread from outside, inspired by:  https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
            break
    next(print_state) # prints one state
    next(print_state) # prints one state
