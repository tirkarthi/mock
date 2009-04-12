from __future__ import with_statement

from testcase import TestCase

from mock import Mock, patch, patch_object, sentinel

something  = sentinel.Something
something_else  = sentinel.SomethingElse


class WithTest(TestCase):
    def testWithStatement(self):
        with patch('tests.withtest.something', sentinel.Something2):
            self.assertEquals(something, sentinel.Something2, "unpatched")        
        self.assertEquals(something, sentinel.Something)
        
    def testWithStatementException(self):
        try:
            with patch('tests.withtest.something', sentinel.Something2):
                self.assertEquals(something, sentinel.Something2, "unpatched")   
                raise Exception('pow')
        except Exception:
            pass
        else:
            self.fail("patch swallowed exception")
        self.assertEquals(something, sentinel.Something)


    def testWithStatementAs(self):
        with patch('tests.withtest.something') as mock_something:
            self.assertEquals(something, mock_something, "unpatched")        
            self.assertTrue(isinstance(mock_something, Mock), "patching wrong type")
        self.assertEquals(something, sentinel.Something)


    def testPatchObjectWithStatementAs(self):
        mock = Mock()
        original = mock.something
        with patch_object(mock, 'something') as mock_something:
            self.assertNotEquals(mock.something, original, "unpatched")        
        self.assertEquals(mock.something, original)


    def testWithStatementNested(self):
        from contextlib import nested
        with nested(patch('tests.withtest.something'), 
                    patch('tests.withtest.something_else')) as (mock_something, mock_something_else):
            self.assertEquals(something, mock_something, "unpatched")
            self.assertEquals(something_else, mock_something_else, "unpatched")
        self.assertEquals(something, sentinel.Something)
        self.assertEquals(something_else, sentinel.SomethingElse)


    def testWithStatementSpecified(self):
        with patch('tests.withtest.something', sentinel.Patched) as mock_something:
            self.assertEquals(something, mock_something, "unpatched")        
            self.assertEquals(mock_something, sentinel.Patched, "wrong patch")        
        self.assertEquals(something, sentinel.Something)



if __name__ == '__main__':
    RunTests(PatchTest)