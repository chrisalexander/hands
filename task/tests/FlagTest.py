'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from task.Task import Task

result = False
def runFunction(runner):
    global result
    result = True
    return result
    
def errorFunction(runner):
    global runFunction
    runFunction(runner)
    raise Exception("Failed")

class Test(unittest.TestCase):


    def testRunFlag(self):
        global runFunction, result
        t = Task(runFunction)
        t.run(None)
        self.assertTrue(result, "Function not called")
        self.assertTrue(t.hasRun, "Run flag not set")
    
    def testSuccessfulFlagTrue(self):
        global runFunction, result
        t = Task(runFunction)
        t.run(None)
        self.assertTrue(result, "Function not called")
        self.assertTrue(t.successful, "Run flag not set")
    
    def testSuccessfulFlagFalse(self):
        global errorFunction, result
        t = Task(errorFunction)
        try:
            t.run(None)
            self.fail("Exception not raised")
        except:
            pass
        self.assertTrue(result, "Function not called")
        self.assertFalse(t.successful, "Run flag not set")
    
    def testErrorFieldUnset(self):
        global runFunction, result
        t = Task(runFunction)
        t.run(None)
        self.assertTrue(result, "Function not called")
        self.assertEqual(None, t.error, "Error field set")
    
    def testErrorFieldSet(self):
        global errorFunction, result
        t = Task(errorFunction)
        try:
            t.run(None)
            self.fail("Exception not raised")
        except:
            pass
        self.assertTrue(result, "Function not called")
        self.assertEqual("Failed", "%s" % t.error, "Error field not set")
    
    def testResultFieldSet(self):
        global runFunction, result
        t = Task(runFunction)
        t.run(None)
        self.assertTrue(result, "Function not called")
        self.assertEqual(True, t.result, "Result field not set")
    
    def testResultFieldUnset(self):
        global errorFunction, result
        t = Task(errorFunction)
        try:
            t.run(None)
            self.fail("Exception not raised")
        except:
            pass
        self.assertTrue(result, "Function not called")
        self.assertEqual(None, t.result, "Result field set")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRunFlag']
    unittest.main()