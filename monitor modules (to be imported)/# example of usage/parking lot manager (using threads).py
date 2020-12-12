#==================================================================================================
#=== Parking lot example ==================================================================================================
#==================================================================================================
'''
               drawing made with help of : http://asciiflow.com/ website


 cars                ╔═════════════════════════════╗
 waiting             ║ ┌-───-┐   ┌-───-┐   ┌-───-┐ ║
 outside             ║ │  C  │   │  D  │   │  E  │ ║
                   ══╝ └-───-┘   └-───-┘   └-───-┘ ╚══
┌-───-┐  ┌-───-┐  ┌-───-┐                           ┌-───-┐
│  A  │  │  B  │  │  X  │                           │  Y  │    (car Y is exiting park)
└-───-┘  └-───-┘  └-───-┘                           └-───-┘
  car              ══╗ ┌-───-┐                     ╔══
            entrance ║ │  F  │                     ║ exit
                     ║ └-───-┘                     ║
                     ╚═════════════════════════════╝

                          park with max capacity

RULES:
. at most, one car can go through a certain gate
. if the park is full, cars can't cross entrance gate and must wait outside
. while a car is entering form entrance, it's counted as occupying the park
. a car frees it's place in the park right after it quits exit gate
=====================================================================================
let's make a monitor to manage acess to the park
'''

from off_topic_code import Car, run_as_thread, state_logger_thread, go_to_parent_dir

go_to_parent_dir()    # go to parent dir (because the packages are in parent dir in this example)
from thread_monitor import Monitor

class Park(Monitor):
    def __init__(self, capacity):
        self.init_lock() # don't forget to init the lock
        self.free_places      = capacity # used to block cars if park is full
        self.outside          = self.Condition() # used to make acess to gates in mutual exlusion
        self.entrance_gate    = self.Entrance_gate(self)
        self.exit_gate        = self.Exit_gate(self)                                           ; self._occupied_places = 0 # (ignore this line) used for cmd logging

    
    ''' both gates have similar parts of code, so I gathered all of those in this class'''
    class Gate(Monitor):
        def __init__(self, parent):
            self.init_lock(lock = parent._lock) # this is  part of the park, so the same lock should be used for the park and the gates
            self.gate     = self.Condition()
            self.occupied = False
            self.parent   = parent

        def _acquire_gate(self): #not using lock here because this is hidden method (to avoid dead lock)
            if self.occupied:# if gate is occupied, wait near the gate
                self.gate.wait()
            self.occupied = True # now the gate is ours to cross

        def _release_gate(self): # not using lock here because this is hidden method (to avoid dead lock)
            self.occupied = False # free the gate 
            self.gate.notify() # notify a car waiting near the gate

    ''' for the gate, wel'll define __enter__ and __exit__ methods (see this tutorial for details: https://preshing.com/20110920/the-python-with-statement-by-example/)'''
    class Entrance_gate(Gate):
        def __enter__(self):
            park = self.parent # added this line for readability
            with self._lock:
                # wait outside if park is full
                if park.free_places <= 0:
                    park.outside.wait()
                park.free_places -= 1 # we're entering, so we should reserve our place NOW (if we delay this instruction, cars will enter even if park is full, try it!)
                self._acquire_gate()                                                           ; park._occupied_places += 1 # (ignore this line) used for cmd logging

        def __exit__(self, type, value, traceback):
            with self._lock:
                # free the gate and notify a car waiting near gate to enter
                self.occupied = False 
                self.gate.notify()


    class Exit_gate(Gate):
        def __enter__(self):
            with self._lock:
                self._acquire_gate()
            
        def __exit__(self, type, value, traceback):
            park = self.parent # added this line for readability
            with self._lock:
                self._release_gate()
                # we're out of the park now :), let's notify a car waiting outside to come in
                park.free_places += 1                                                         ; park._occupied_places -= 1 # (ignore this line) used for cmd logging
                park.outside.notify()
    
    # this next method is used for cmd logging (you can ignore this)
    def get_occupied_places(self):
        with self._lock:
            return self._occupied_places 


# to keep it simple here, I defined the 'Car' class in 'off_topic_code' folder
class Clean_car(Car):
    @run_as_thread # this is a 'decorator', used to run this method as a thread
    def visit_park(self, park):
        #-----------------------------------------------------------------------------------------------------------------------------------------
        with park.entrance_gate: # this will execute __enter__ and __exit__ methods
            self.get_in() # takes some time
        #-----------------------------------------------------------------------------------------------------------------------------------------
        self.stay_in_park() # takes a long time
        #-----------------------------------------------------------------------------------------------------------------------------------------
        with park.exit_gate:
            self.get_out() # takes some time
        #-----------------------------------------------------------------------------------------------------------------------------------------


#==================================================================================================
#=== main ==================================================================================================
#==================================================================================================

def main():
    #--- intance of Park monitor --------------------------------------------------------
    park_capacity = 10
    park = Park(park_capacity) 
    #------------------------------------------------------------------------------------
    num_cars = 26
    cars     = [Clean_car(i) for i in range(num_cars)] # cars array


    #--------- launch car threads -------------------------------------------------------
    stop_log = False
    threads  = []
    for i in range(num_cars):
        t = cars[i].visit_park(park)
        threads.append(t)

    #--------- launch command line logger -----------------------------------------------
    logger = state_logger_thread(cars, park, lambda : stop_log) 
    ''' the lambda function here helps lets us pass a local variable to the tread AND have it always updated! (reference pass)
            (inspired from: 'https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/') '''
    #--------- wait for threads to finish -----------------------------------------------
    for t in threads:
        t.join()
    stop_log = True
    logger.join()


if __name__ == '__main__':
    main()
