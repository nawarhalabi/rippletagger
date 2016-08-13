import unittest

from flake8.engine import get_style_guide

class TestFlake8Compliance(unittest.TestCase):
    def test_flake8(self):
        report = get_style_guide(parse_argv=True, paths=".").check_files()
        self.assertEquals(report.get_state()["total_errors"], 0)
