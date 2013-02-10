from random import Random
import hashlib
import time

class TaskIdentifier:
    
    def __init__(self):
        """ Initialises the identifier.
        
        Generates a random string for the identification of a given task.
        
        """
        r = Random();
        r.seed(r.randint(0, 1000000000))
        h = hashlib.sha384()
        h.update("%i" % r.randint(0, 1000000000))
        h.update("%d" % time.time())
        self.id = h.hexdigest()