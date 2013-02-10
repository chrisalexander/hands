'''
Created on 10 Feb 2013

@author: dev
'''
import unittest
from runner.NextPriorityGenerator import NextPriorityGenerator
from random import Random
from time import sleep
from threading import Thread
from time import time

class Test(unittest.TestCase):


    def testBasicUsage(self):
        r = Random()
        n = r.randint(0, 10000)
        npg = NextPriorityGenerator(n)
        self.assertEqual(n, npg.getNextPriority(), "First result not valid")
        for i in range(1, 10):
            self.assertEqual(1000000-i, npg.getNextPriority(), "%sth result not valid" % i)

    def testThreadedUsage(self):
        r = Random()
        n = r.randint(0, 10000)
        npg = NextPriorityGenerator(n)
        self.assertEqual(n, npg.getNextPriority(), "First result not valid")
        
        results = {}
        threads = []

        def storeResult():
            sleep(r.random())
            p = npg.getNextPriority()
            results[p] = time()
            
        # Start up a load of threads    
        for i in range(1, 10):
            t = Thread(target=storeResult)
            t.setDaemon(True)
            t.start()
            threads.append(t)
        
        # Wait for all the threads to be done
        for t in threads:
            t.join(2)
        
        # Check all the results are right
        prev = None
        for i in range(1, 10):
            j = 1000000 - i
            self.assertTrue(j in results, "Results array does not have correct key")
            if prev is not None:
                self.assertTrue(results[j] > prev)
            prev = results[j]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBasicUsage']
    unittest.main()