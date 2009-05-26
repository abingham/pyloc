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
from .db import Results
from .logger import logger, handler
from .util import loc

usage = '''%prog [options] [root1 root2 . . .]

Built-in formatters:
 pyloc.format.by_langauge
 pyloc.pie_chart.by_language(category, title)
'''

def parse_args():
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', help='increase logging output')
    parser.add_option('-f', '--format', dest='format',
                      help='format function for output',
                      default='pyloc.format.by_language')
    parser.add_option('-a', '--args', dest='args',
                      default='',
                      help='arguments to pass to format function')
    parser.add_option('-d', '--dbname', dest='dbname',
                      default=None,
                      help='load/save results from/to a database file')
    return (parser.parse_args(),parser)

def main():
    ((options, args), parser) = parse_args()

    if len(args) == 0:
        return

    if options.verbose:
        handler.setLevel(logging.DEBUG)

    if options.dbname is None:
        rslt = Results()
    else:
        logger.info('loading/saving results from %s' % options.dbname)
        rslt = Results(options.dbname)

    loc(args, rslt)

    format_module = '.'.join(options.format.split('.')[:-1])
    format_command = '%s(rslt,%s)' % (options.format, options.args)

    logger.info('format module: %s' % format_module)
    logger.info('format function: %s' % format_command)

    exec('import %s' % format_module)
    exec(format_command)

    rslt.close()

if __name__ == '__main__':
    main()
