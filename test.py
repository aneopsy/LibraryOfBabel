import unittest
from library_of_babel import LoB


class LoBTest(unittest.TestCase):

    def test_a(self):
        self.lob = LoB()
        assert self.lob.stringToNumber('a') == 0, self.lob.stringToNumber('a')
        assert self.lob.stringToNumber('ba') == 29, self.lob.stringToNumber('ba')

    def test_b(self):
        self.lob = LoB()
        assert len(self.lob.getPage('asaskjkfsdf:2:2:2:33')) == self.lob.length_of_page, len(self.lob.getPage('asasrkrtjfsdf:2:2:2:33'))
        assert 'hello kitty' == self.lob.toText(int(self.lob.int2base(self.lob.stringToNumber('hello kitty'), 36), 36))

    def test_c(self):
        self.lob = LoB()
        assert self.lob.int2base(4, 36) == '4', self.lob.int2base(4, 36)
        assert self.lob.int2base(10, 36) == 'A', self.lob.int2base(10, 36)

    def test_d(self):
        self.lob = LoB()
        test_string = '.................................................'
        assert test_string in self.lob.getPage(self.lob.search(test_string))

    def test_e(self):
        self.lob = LoB()
        print('')
        self.lob.printPage('HELLO:0:0:0:0')

if __name__ == '__main__':
    unittest.main()
