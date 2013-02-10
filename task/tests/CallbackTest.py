'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from random import Random
from task.Task import Task
from task.CallbackExecutionException import CallbackExecutionException

class SuccessfulCallback:
    
    def __init__(self, number):
        self.number = number
        
    def execute(self, runner):
        return self.number
    
    def callback(self, successful, result):
        self.successful = successful
        self.result = result
        return True
    
class FailCallback(SuccessfulCallback):
    
    def callback(self, successful, result):
        raise Exception("Failure! %i" % self.number)

class Test(unittest.TestCase):
    
    
    def testCallbackSuccess(self):
        r = Random()
        n = r.randint(1, 999)
        c = SuccessfulCallback(n)
        t = Task(c.execute, c.callback)
        try:
            t.run(None)
            self.assertEqual(n, t.result, "The result and generated random number must be equal")
            self.assertEqual(n, c.result, "The callback-stored result and random number must be equal")
            self.assertTrue(c.successful, "The callback must set the successful flag")
        except Exception as e:
            self.fail("Threw exception: %s" % e)
    
    def testCallbackFail(self):
        r = Random()
        n = r.randint(1, 999)
        c = FailCallback(n)
        t = Task(c.execute, c.callback)
        try:
            t.run(None)
            self.fail("The expected exception was not thrown")
        except CallbackExecutionException as e:
            self.assertEqual("Failure! %i" % n, "%s" % e, "Exception message not correct")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCallbackSuccess']
    unittest.main()