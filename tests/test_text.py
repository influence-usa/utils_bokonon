from text import extractNames
import unittest


class TestExtractNames(unittest.TestCase):

    def test_function(self):
        cases = [(["google"],"Google inc"),
                 
                 (["boys town usa", "girls and boys town usa"],
                  "Boys town usa (formerly girls and boys town usa)"),
                 
                 (["esm group"],"the livingston group llc (on behalf of esm group, inc.)"),
                 
                 (['international buddhism sangha association', 'master wan ko yee'],
                  "intl. buddhism sangha assn. (fka dr. david wu on behalf of master wan ko yee)"),
                 
        ]
        for a,b in cases:
            self.assertEqual(a,extractNames(b))
            
    
if __name__ == '__main__':
    unittest.main()
