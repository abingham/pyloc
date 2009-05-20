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

from .logger import logger, handler
from .util import loc

def parse_args():
    parser = OptionParser(usage='%prog [options] [root1 root2 . . .]')
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', help='increase logging output')
    return (parser.parse_args(),parser)

def main():
    ((options, args), parser) = parse_args()

    if len(args) == 0:
        return

    if options.verbose:
        handler.setLevel(logging.DEBUG)

    values = []
    for target in args:
        if not os.path.exists(target):
            logger.error('file or directory not found: %s' % target)
        else:
            values.append((target, loc(target)))

    # sum up all categories
    sums = {}
    for tgt,vals in values:
        for k,v in vals.items():
            try:
                sums[k] += v
            except KeyError:
                sums[k] = v
    values.append(('TOTAL', sums))

    keys = sums.keys()
    keys.remove('total')
    keys.remove('minimum')
    keys = ['total', 'minimum'] + keys

    max_dir_len = max([len(x[0]) for x in values])
    
    max_lens = {}
    for k in keys:
        max_lens[k] = max([len(str(x[1][k])) for x in values])
        max_lens[k] = max([max_lens[k], len(k)])

    io = StringIO()

    io.write('%-*s' % (max_dir_len, 'directory'))
    for k in keys:
        io.write(' %*s' % (max_lens[k], k))
    io.write('\n')

    io.write('%*s' % (max_dir_len, '-' * max_dir_len))
    for k in keys:
        io.write(' %*s' % (max_lens[k], '-' * len(k)))
    io.write('\n')

    for dir, vals in values:
        io.write('%-*s' % (max_dir_len, dir))

        for k in keys:
            try:
                io.write(' %*s' % (max_lens[k], vals[k]))
            except KeyError:
                io.write(' %*s' % (max_lens[k], ''))
        io.write('\n')

    print io.getvalue()

if __name__ == '__main__':
    main()
