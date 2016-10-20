import string
import random
import sys


# 29 output letters: alphabet plus comma, space, and period
# alphanumeric in hex address (base self.number_of_an): 3260
# in wall: 4
# in shelf: 5
# in volumes: 32
# pages: 410
# letters per page: 3200
# titles have 25 char


class LoB(object):
    digs = 'abcdefghijklmnopqrstuvwxyz, .'
    an = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    number_of_wall = 4
    number_of_shelf = 5
    number_of_volume = 32
    number_of_page = 410
    number_of_line = 40
    number_of_digs = len(digs)
    number_of_an = len(an)

    length_of_title = 25
    length_of_line = 80
    length_of_page = length_of_line * number_of_line

    loc_mult = pow(30, length_of_page)
    title_mult = pow(30, length_of_title)

    color_red = '\033[93m'
    color_default = '\033[0m'

    def text_prep(cls, text):
        digs = set(cls.digs)
        prepared = ''
        for letter in text:
            if letter in digs:
                prepared += letter
            elif letter.lower() in digs:
                prepared += letter.lower()
            elif letter == '\n':
                prepared += ' '
        return prepared

    def printSearchPage(cls, key_str, search_str):
        page = cls.getTitle(key_str) + '\n'
        text = cls.getPage(key_str)
        for i in range(0, len(text), cls.length_of_line):
            page += text[i:i + cls.length_of_line] + '\n'
        return page

    def printPage(cls, key_str):
        page = cls.getTitle(key_str) + '\n'
        print(page)
        text = cls.getPage(key_str)
        for i in range(0, len(text), cls.length_of_line):
            print(text[i:i + cls.length_of_line])
            page += '\n' + text[i:i + cls.length_of_line]
        print('\n' + key_str)
        return page

    def filed(self, input_dict, text):
        if input_dict['--file'][0]:
            with open(input_dict['--file'][1], 'w') as file:
                file.writelines(text)
            print('\nFile ' + input_dict['--file'][1] + ' was writen')

    def search(self, search_str):
        wall = str(int(random.random() * self.number_of_wall))
        shelf = str(int(random.random() * self.number_of_shelf))
        volume = str(int(random.random() * self.number_of_volume)).zfill(2)
        page = str(int(random.random() * self.number_of_page)).zfill(3)
        loc_str = page + volume + shelf + wall
        loc_int = int(loc_str)
        hex_addr = ''
        depth = int(random.random()*(self.length_of_page - len(search_str)))
        front_padding = ''
        for x in xrange(depth):
            front_padding += self.digs[int(random.random() * len(self.digs))]
        back_padding = ''
        for x in xrange(self.length_of_page - (depth + len(search_str))):
            back_padding += self.digs[int(random.random() * len(self.digs))]
        search_str = front_padding + search_str + back_padding
        hex_addr = self.int2base(self.stringToNumber(search_str) + (loc_int * self.loc_mult), self.number_of_an)
        key_str = hex_addr + ':' + wall + ':' + shelf + ':' + volume + ':' + page
        page_text = self.getPage(key_str)
        assert page_text == search_str, '\npage text:\n'+page_text+'\nstrings:\n' + search_str
        return key_str

    def getTitle(self, address):
        addressArray = address.split(':')
        hex_addr = addressArray[0]
        wall = addressArray[1]
        shelf = addressArray[2]
        volume = addressArray[3].zfill(2)
        loc_int = int(volume + shelf + wall)
        key = int(hex_addr, self.number_of_an)
        key -= loc_int * self.title_mult
        str_an = self.int2base(key, self.number_of_an)
        result = self.toText(int(str_an, self.number_of_an))
        if len(result) < 25:
            random.seed(result)
            while len(result) < 25:
                result += self.digs[int(random.random()*len(self.digs))]
        elif len(result) > 25:
            result = result[-25:]
        return result

    def searchTitle(self, search_str):
        wall = str(int(random.random()*4))
        shelf = str(int(random.random()*5))
        volume = str(int(random.random()*32)).zfill(2)
        # the string made up of all of the location numbers
        loc_str = volume + shelf + wall
        loc_int = int(loc_str)
        # make integer
        hex_addr = ''
        search_str = search_str[:25].ljust(25)
        hex_addr = self.int2base(self.stringToNumber(search_str)+(loc_int * self.title_mult), self.number_of_an)
        # change to base self.number_of_an and add loc_int, then make string
        key_str = hex_addr + ':' + wall + ':' + shelf + ':' + volume
        assert search_str == self.getTitle(key_str)
        return key_str

    def getPage(self, address):
        hex_addr, wall, shelf, volume, page = address.split(':')
        volume = volume.zfill(2)
        page = page.zfill(3)
        loc_int = int(page + volume + shelf + wall)
        key = int(hex_addr, self.number_of_an)
        key -= loc_int * self.loc_mult
        str_an = self.int2base(key, self.number_of_an)
        result = self.toText(int(str_an, self.number_of_an))
        if len(result) < self.length_of_page:
            # adding pseudorandom chars
            random.seed(result)
            while len(result) < self.length_of_page:
                result += self.digs[int(random.random()*len(self.digs))]
        elif len(result) > self.length_of_page:
            result = result[-self.length_of_page:]
        return result

    def toText(self, x):
        if x < 0:
            sign = -1
        elif x == 0:
            return self.digs[0]
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(self.digs[x % 29])
            x /= 29
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)

    def stringToNumber(self, iString):
        result = 0
        for x in xrange(len(iString)):
            result += self.digs.index(iString[len(iString)-x-1])*pow(29, x)
        return result

    def int2base(self, x, base):
        if x < 0:
            sign = -1
        elif x == 0:
            return self.an[0]
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(self.an[x % base])
            x /= base
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)
