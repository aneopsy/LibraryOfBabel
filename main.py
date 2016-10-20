import os
import sys
import argparse

from library_of_babel import LoB
from book import Book

__author__ = 'AneoPsy'
__version__ = 0.1


def _cli_opts():
    '''
    Parse command line options.
    @returns the arguments
    '''
    mepath = unicode(os.path.abspath(sys.argv[0]))
    mebase = '%s' % (os.path.basename(mepath))

    description = '''
        Implements encryption/decryption that is compatible with openssl
        AES-256 CBC mode.
        '''
    desc = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=mebase,
                                     formatter_class=desc,
                                     description=description,
                                     )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--checkout',
                       action='store',
                       help='Get a page')
    group.add_argument('-s', '--search',
                       action='store',
                       help='Search a page')
    group.add_argument('-b', '--browse',
                        action='store',
                        help='Browse')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s v' + str(__version__) +
                                " by " + __author__)

    args = parser.parse_args()
    return args


def _runcheckout(args):
    LoB().printPage(args.checkout)


def _runsearch(args):
    search_str = LoB().text_prep(args.search)
    key_str = LoB().search(LoB().text_prep(search_str))
    LoB().printPage(key_str)


def _runbrowse(args):
    book = Book()
    book.new(args.browse)

    while True:
        book.printPage()
        cmd = raw_input('> ')
        if '>' in cmd:
            book.next()
        elif '<' in cmd:
            book.prev()


def main():
    args = _cli_opts()
    if args.checkout:
        _runcheckout(args)
    elif args.search:
        _runsearch(args)
    elif args.browse:
        _runbrowse(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit...')
