import unittest

from containers import *


class Serial(unittest.TestCase):
    def test_deser_overview(self):
        o = Overview("a","b",1,2,[])
        b = o.to_bjson()
        self.assertEqual(b, b'{"server_username": "a", "client_username": "b", "space_KB_total": 1, "space_KB_free": 2, "files": []}')
        o2 = Overview.from_bjson(b)
        self.assertEqual(o, o2)

    def test_deser_fileinfo(self):
        f = FileInfo("h", 12)
        b = f.to_bjson()
        f2 = FileInfo.from_bjson(b)
        self.assertEqual(f,f2)

    def test_deser_corrupt(self):
        b = b"{}"
        f = FileInfo.from_bjson(b)
        self.assertIsNone(f)


if __name__ == '__main__':
    unittest.main()
