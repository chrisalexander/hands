'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from task.TaskIdentifier import TaskIdentifier


class Test(unittest.TestCase):


    def testRandomness(self):
        t1 = TaskIdentifier()
        t2 = TaskIdentifier()
        self.assertNotEqual(t1.id, t2.id, "The identifiers are equal")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRandomness']
    unittest.main()