'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from runner.Runner import Runner
from task.Task import Task
from task.TaskIdentifier import TaskIdentifier

class BasicJob:
    def __init__(self):
        self.run = False
    def do(self, runner):
        self.run = True

executionOrder = []

class IdentifiedJob:
    def __init__(self, i):
        self.i = i
        self.run = False
    def do(self, runner):
        self.run = True
        global executionOrder
        executionOrder.append(self.i)

class EnqueueJob:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.run = False
    def do(self, runner):
        self.run = True
        
        global executionOrder
        executionOrder.append(self.i)
        
        job = IdentifiedJob(self.j)
        task = Task(job.do)
        runner.enqueueNext(task)

class Test(unittest.TestCase):


    def testBasicJobRun(self):
        r = Runner()
        j = BasicJob()
        t = Task(j.do)
        ref = r.enqueue(t)
        
        # Check the job has not been run until start is called
        task = r.get(ref)
        self.assertFalse(task.hasRun) 
        
        r.start()
        
        # Check the job has been run and the runner has been finished
        self.assertTrue(j.run, "Job has not been run")
        self.assertFalse(r.running, "Runner has not finished")
        
    def testTaskNotFound(self):
        r = Runner()
        ref = TaskIdentifier()
        try:
            r.get(ref)
            self.fail("Exception not thrown")
        except:
            pass
        
    def testEnqueueNext(self):
        r = Runner()
        
        for i in range(0, 5):
            if i == 2:
                # This one will enqueue another one after it
                j = EnqueueJob(i, 100)
                f = j.do
            else:
                j = IdentifiedJob(i)
                f = j.do
            r.enqueue(Task(f))
        
        r.start()
        
        global executionOrder
        self.assertEqual([0, 1, 2, 100, 3, 4], executionOrder, "Execution order not correct")
    
    def testStop(self):
        r = Runner()
        j = BasicJob()
        t = Task(j.do)
        ref = r.enqueue(t)
        
        # Check the job has not been run
        task = r.get(ref)
        self.assertFalse(task.hasRun) 
        
        r.stop()
        r.start()
        
        # Check the job has still not been run and the runner has been finished
        self.assertFalse(j.run, "Job has not been run")
        self.assertFalse(r.running, "Runner has not finished")
        
    def testCancel(self):
        r = Runner()
        j = BasicJob()
        t = Task(j.do)
        ref = r.enqueue(t)
        
        r.dequeue(ref)
        
        # Check the job has not been run
        task = r.get(ref)
        self.assertFalse(task.hasRun) 
        
        r.start()
        
        # Check the job has still not been run and the runner has been finished
        self.assertFalse(j.run, "Job has not been run")
        self.assertFalse(r.running, "Runner has not finished")
        
    def testCancelAlreadyRun(self):
        r = Runner()
        j = BasicJob()
        t = Task(j.do)
        ref = r.enqueue(t)
        
        # Check the job has not been run
        task = r.get(ref)
        self.assertFalse(task.hasRun) 
        
        r.start()
        
        # Check the job has been run and the runner has been finished
        self.assertTrue(j.run, "Job has not been run")
        self.assertFalse(r.running, "Runner has not finished")
        
        try:
            r.dequeue(ref)
            self.fail("Dequeue should throw exception")
        except:
            pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBasicJobRun']
    unittest.main()