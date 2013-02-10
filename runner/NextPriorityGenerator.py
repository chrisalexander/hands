from threading import Lock

class NextPriorityGenerator:
    """ Generates a priority number for a job to run next.
    
    This encapsulates some thread-safe locking behaviour around a counter.
    The next job to run is determined by which has the highest priority number.
    To guarantee a "next" job is actually run next, the number must exceed all others
    in the stack. To do this we have an incrementor which provides continuously growing
    numbers. Due to the threaded nature of the queue execution we must make sure that
    grabbing this number is thread-safe when multiple concurrent jobs are running.
    
    """
    
    def __init__(self, start = 0):
        """ Initialise the generator. """
        
        self.next = start;
        self.lock = Lock()
        
    def getNextPriority(self):
        """ Returns the next thread priority level. """
        self.lock.acquire()
        self.next = self.next - 1
        nextval = self.next
        self.lock.release()
        return nextval