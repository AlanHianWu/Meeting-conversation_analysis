import unittest, time, sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from source import dbp_spotlight as dbp


class TranscriptTest(unittest.TestCase):
    
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_dbp_nlp_acc(self):
    
        
        for i in self.drange(0, 1, 0.05):
            try:
                results = dbp.test(i)
                ents = []
                for ent in results.ents:
                    ents.append(ent.text)
                print(i, len(ents))
                
                # with open('ent.txt', 'a') as f:
                #     for e in ents:
                #         f.write(e+',')
                #     f.write('\n\n' + i + ' \n\n')

            except:
                pass
       
    
    @staticmethod
    def drange(start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step
        



if __name__ == '__main__':
 

    suite = unittest.TestLoader().loadTestsFromTestCase(TranscriptTest)
    unittest.TextTestRunner(verbosity=0).run(suite)