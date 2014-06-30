from text import extractNames
import unittest


cases = [(["google"],"Google inc"),
         
         (["boys town usa", "girls and boys town usa"],
          "Boys town usa (formerly girls and boys town usa)"),
         
         (["esm group"],"the livingston group llc (on behalf of esm group, inc.)"),
         
         (['international buddhism sangha association', 'master wan ko yee'],
          "Intl. Buddhism Sangha Assn. (FKA Dr. David Wu on behalf of Master Wan Ko Yee)"),

         (["dca", "dredging contractors of america"],"DREDGING CONTRACTORS OF AMERICA (DCA)"), #DCA
         (["hart", "housing action resource trust"],"housing action resource trust (\"hart\")"), #DCA         

         (["orange broadband holding"],"orange broadband holding company")  #dba
]

class TestExtractNames(unittest.TestCase):

    def test_function(self):
        for a,b in cases:
            self.assertEqual(a,extractNames(b))
            
    
if __name__ == '__main__':
    unittest.main()
