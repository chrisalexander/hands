from runner import Runner

class Hands:
    """ The main Hands interface.
    
    This class can be instanciated to create a Hands queue and all of the features
    that go with it.
    
    """
    
    def __init__(self):
        """ Initialise Hands. """
        
        # TODO: Runner should run in a separate thread
        self.runner = Runner();