import unittest
from random import Random
from task.Task import Task

class RunContext:
    
    def __init__(self, number):
        self.number = number
        
    def execute(self, runner):
        return self.number

class NoArgsJob:
    def __init__(self):
        self.run = False
    def do(self):
        self.run = True

class Test(unittest.TestCase):


    def testRunContext(self):
        r = Random()
        n = r.randint(1, 999)
        c = RunContext(n)
        t = Task(c.execute)
        t.run(None)
        self.assertEqual(n, t.result, "The result and generated random number must be equal")

    def testNoArgsJob(self):
        # Tests that a job which isn't expecting args still works
        j = NoArgsJob()
        t = Task(j.do)
        t.run(None)
        self.assertTrue(j.run)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRunContext']
    unittest.main()