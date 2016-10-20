from library_of_babel import LoB


class Book(object):
    def __init__(self):
        self.str_key = ''
        self.title = ''
        self.pages = list()

        self.hex_addr = 0
        self.wall = 0
        self.shelf = 0
        self.volume = 0
        self.page = 0

    def setTitle(self):
        self.title = LoB.getTitle(self.str_key)

    def loadPages(self):
        address = self.str_key.split(':')
        hex_addr = address[0]
        wall = address[1]
        shelf = address[2]
        volume = address[3].zfill(2)
        key_str = hex_addr + ':' + wall + ':' + shelf + ':' + volume + ':'
        for i in range(0, LoB.number_of_page + 1):
            key = key_str + str(i)
            self.pages.append(LoB().getPage(key))
            print(key)

    def infoBook(self):
        return self.hex_addr, self.wall, self.shelf, self.volume

    def printPage(self):
        return LoB().printPage(self.hex_addr + ':' + str(self.wall) + ':' +
                               str(self.shelf) + ':' + str(self.volume) + ':' +
                               str(self.page))

    def next(self):
        if self.page >= 410:
            self.page = 0
        else:
            self.page += 1

    def prev(self):
        if self.page == 0:
            self.page = LoB.number_of_page
        else:
            self.page -= 1

    def new(self, str_key):
        self.str_key = str_key
        address = self.str_key.split(':')
        self.hex_addr = address[0]
        self.wall = int(address[1])
        self.shelf = int(address[2])
        self.volume = int(address[3].zfill(2))
        if len(address) > 4:
            self.page = int(address[4].zfill(3))
        else:
            self.page = 0
        # self.loadPages()
