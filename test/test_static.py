import unittest
import os
from gmbp_quant.static import get_library_root


class TestStatic(unittest.TestCase):
    def test_library_root(self):
        self.assertEqual(os.path.basename(get_library_root()), 'gmbp_quant')
    #
#


if __name__ == '__main__':
    unittest.main()
#
