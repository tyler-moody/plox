import tempfile
import unittest

from input import TestInputter
from main import Application as Main
from output import TestOutputter


class MainTest(unittest.TestCase):
    def test_prompt(self) -> None:
        inputter = TestInputter(['print 5;'])
        outputter = TestOutputter()
        Main(do_printing=False, inputter=inputter, outputter=outputter).run_prompt()
        self.assertEqual(outputter.previous, '5.0')

    def test_file(self) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write('print 5;'.encode())
            f.seek(0)
            outputter = TestOutputter()
            Main(do_printing=False, outputter=outputter).run_file(filename=f.name)

            self.assertEqual(outputter.message, '5.0')
