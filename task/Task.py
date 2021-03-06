from threading import Thread, Lock
from task.CallbackExecutionException import CallbackExecutionException
from task.TaskIdentifier import TaskIdentifier
from task.AlreadyRunException import AlreadyRunException
import inspect

class Task:
    """ A generic task wrapper.
    
    This class is the standard wrapper around tasks that are submitted to be
    run by Hands.
    
    """
    
    def __init__(self, method, callback = None):
        """ Initialises the task.
        
        Provide the method to be run, and an optional completion callback.
        
        The first argument given to the callback is a boolean of whether or not it
        was successful. If it was successful, the second argument is the result of the
        task; if not successfuly, it is the error that was raised, if there was one.
        
        """
        
        # Internal state
        self.hasRun = False
        self.successful = None
        self.error = None
        self.thread = None
        self.result = None
        self.identifier = TaskIdentifier()
        self.lock = Lock()
        self.cancelled = False # No cancellation logic in the task itself
        
        # External references
        self.method = method
        self.callback = callback
        
    def run(self, runner):
        """ Run the task.
        
        This runs the task in another thread, returning the result and calling the callback.
        Note that this call blocks until the run is complete.
        
        """
        t = self.runAsync(runner)
        t.join()
        
        self.doCallback()
        
        if self.successful:
            return self.result
        else:
            raise self.error
    
    def runAsync(self, runner):
        """ Run the task asynchronously.
        
        This runs the task in another thread. Instead of returning the result, it returns
        the thread and you have to join() on that for to be completed. Once this is called
        this object is in its completed state.
        
        """
        
        def execute(task, runner):
            # Run the method
            try:
                args = inspect.getargspec(task.method)[0]
                if args[0] == "self":
                    args.pop()
                if len(args) < 1:
                    res = task.method()
                else:
                    res = task.method(runner)
                task.successful = True
                task.result = res
            except Exception as e:
                task.successful = False
                task.error = e
            finally:
                task.hasRun = True
        
        # Acquire the execution lock
        self.lock.acquire()
        
        # Start the thread
        self.thread = Thread(target=execute, args=(self, runner))
        self.thread.setDaemon(True)
        
        if self.hasRun:
            self.lock.release()
            raise AlreadyRunException()
        
        self.thread.start()
        self.lock.release()
        return self.thread

    def doCallback(self):
        """ Helper method which calls back, if provided. """
        if callable(self.callback):
            try:
                self.output = self.result if self.successful else self.error
                self.callback(self.successful, self.output)
            except Exception as e:
                raise CallbackExecutionException(e)

    def simultaneously(self, task):
        """ Add a task to this one, to be run simultaneously.
        
        The execution of the two (or more) simultaneous tasks is assumed to be non-dependent
        on one another - they can safely be run in an arbitrary order and concurrently
        without causing any issues. Watch out for race conditions.
        
        """
        # TODO: Implement
        pass
