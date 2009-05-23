'''lines-of-code counter for python

pyloc scans a list of directory trees for python source files,
counting lines of code. For each tree, two counts are reported:

 * A line count include comments and blank lines
 * A line count with out comments and blank lines

Finally, sums of both counts are reported.

The meat of this code was shamelessly stolen from
http://code.activestate.com/recipes/527746/
'''

from cStringIO import StringIO
from optparse import OptionParser
import fnmatch, logging, os.path

import pyloc.format
from .logger import logger, handler
from .util import loc



def parse_args():
    parser = OptionParser(usage='%prog [options] [root1 root2 . . .]')
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', help='increase logging output')
    parser.add_option('-f', '--format', dest='format',
                      help='format function for output',
                      default='pyloc.format.by_language')
    return (parser.parse_args(),parser)

def main():
    ((options, args), parser) = parse_args()

    if len(args) == 0:
        return

    if options.verbose:
        handler.setLevel(logging.DEBUG)

    rslt = loc(args)

    exec('%s(rslt)' % options.format)

if __name__ == '__main__':
    main()
