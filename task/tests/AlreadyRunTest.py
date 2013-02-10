'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from task.Task import Task
from task.AlreadyRunException import AlreadyRunException

class Runner:
    
    def __init__(self, number):
        self.number = number
        
    def execute(self, runner):
        return self.number

class Test(unittest.TestCase):


    def testAlreadyRun(self):
        r = Runner(100)
        t = Task(r.execute)
        try:
            t.run(None)
        except:
            self.fail("Exception thrown where unexpected")
            
        try:
            t.run(None)
            self.fail("Did not cause any exceptions")
        except AlreadyRunException:
            pass
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAlreadyRun']
    unittest.main()