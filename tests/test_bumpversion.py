from ludocommon import bumpBuild
import unittest

class BumpVersionTests(unittest.TestCase):
    def test_NullInputIsHandledCorrectly(self):
        res = bumpBuild(None)
        a,b = res.split('.')
        self.assertEqual(6,len(a))
        self.assertEqual(b,'0')
        self.assertTrue(a.isnumeric())
        self.assertTrue(b.isnumeric())

    
    def test_EmptyInputIsHandledCorrectly(self):
        res = bumpBuild('')
        a,b = res.split('.')
        self.assertEqual(6,len(a))
        self.assertEqual(b,'0')
        self.assertTrue(a.isnumeric())
        self.assertTrue(b.isnumeric())
    
    def test_Bumps_(self):
        res = bumpBuild('something.9')
        # 240422.10
        a,b = res.split('.')
        self.assertEqual(6,len(a))
        self.assertEqual(b,'10')
        self.assertTrue(a.isnumeric())
        self.assertTrue(b.isnumeric())