import Queue
from runner.NextPriorityGenerator import NextPriorityGenerator
from runner.RunExecutionException import RunExecutionException
from runner.NoSuchTaskException import NoSuchTaskException

class Runner:
    """ A task runner.
    
    This class is responsible for handling the queue and organising the running of tasks.
    
    """
    
    def __init__(self):
        """ Initialise the runner. """
        
        self.queue = Queue.PriorityQueue()
        self.tasks = {}
        self.nextPriorityGenerator = NextPriorityGenerator()
        self.running = False
        self.stopRunning = False
        
    def start(self):
        """ Start running jobs. """
        self.running = True
        self.runNextJob()
        
    def runNextJob(self):
        """ Internal helper for running the next job. """
        
        # If the stop flag has been set, stop execution
        if self.stopRunning:
            self.finished()
            return
        
        # Try and get a task and run it
        try:
            taskset = self.queue.get(True, 2)
            task = self.tasks[taskset[1]]
            task.run(self)
        except Queue.Empty as e:
            self.finished()
            return
        except Exception as e:
            raise RunExecutionException(e)
        
        # If we haven't returned up to here, we can try another job
        self.runNextJob()
        
    def stop(self):
        """ Stop running jobs.
        
        This stops jobs from running after the currently executing one has finished.
        
        """
        self.stopRunning = True
        
    def finished(self):
        """ Internal function called when the jobs are finished. """
        self.running = False
        # TODO: Finish implementation
        
    def enqueue(self, task, priority=1000000):
        """ Queues a task.
        
        This task will be run after all of the other ones currently in the queue.
        
        Returns an identifier for this task, which can be used to reference it (e.g.
        to cancel, abort, or get the status of it) later.
        
        """
        self.tasks[task.identifier.id] = task
        self.queue.put((priority, task.identifier.id))
        return task.identifier
    
    def simultaneously(self, tasks):
        """ Queues a tuple of tasks to be run simultaneously.
        
        The execution of the two (or more) simultaneous tasks is assumed to be non-dependent
        on one another - they can safely be run in an arbitrary order and concurrently
        without causing any issues. Watch out for race conditions.
        
        """
        # TODO: Implement
        raise Exception("Not currently implemented")
    
    def enqueueNext(self, task):
        """ Queues the task to run next.
        
        The task will be run after the currently executing one, if any, has finished.
        
        """
        # TODO: This currently doesn't work properly, takes account of data as well as numbers. Need own priority queue implementation
        self.enqueue(task, self.nextPriorityGenerator.getNextPriority())
    
    def run(self, task):
        """ Runs a task immediately.
        
        The task skips the entire queue, even if a task is currently running, and is run
        immediately.
        
        """
        # TODO: Implement
        raise Exception("Not currently implemented")
    
    def dequeue(self, taskReference):
        """ Dequeues a task.
        
        If the task has not been run, it is removed and will not be executed. If it
        has already been run, raises an AlreadyRunException.
        
        """
        # TODO: Implement
        raise Exception("Not currently implemented")
    
    def result(self, taskReference):
        """ Gets the result of a task.
        
        If the task has not yet run, returns None. Otherwise, returns whatever the
        result of running the task was.
        
        """
        # TODO: Implement
        raise Exception("Not currently implemented")
    
    def get(self, taskReference):
        """ Returns the task object given its reference. """
        if taskReference.id in self.tasks:
            return self.tasks[taskReference.id]
        raise NoSuchTaskException()
