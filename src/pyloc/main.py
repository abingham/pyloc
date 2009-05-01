'''lines-of-code counter for python

pyloc scans a list of directory trees for python source files,
counting lines of code. For each tree, two counts are reported:

 * A line count include comments and blank lines
 * A line count with out comments and blank lines

Finally, sums of both counts are reported.

The meat of this code was shamelessly stolen from
http://code.activestate.com/recipes/527746/
'''

from optparse import OptionParser
import fnmatch, logging, os, os.path

from .logger import logger, handler
import pyloc

def walk(root='.', recurse=True):
    '''generate a files in a directory tree walk matching a pattern
    
    Walks a directory tree, generating the files it finds that match a
    provided pattern

    :param root: the root of the tree
    :param recurse: whether to recurse
    '''
    
    if os.path.isfile(root):
        yield root
    else:
        for path, subdirs, files in os.walk(root):
            for name in files:
                yield os.path.join(path, name)
            if not recurse:
                break

def loc(root='', recurse=True):
    '''count lines of code in a directory structure

    Generates two counts:

     * maximal size (source LOC) with blank lines and comments
     * minimal size (logical LOC) stripping same

    Sums all Python files in the specified folder.
    By default recurses through subfolders.

    :param root: the root of the tree to search
    :param recurse: whether to recurse
    '''
    count_mini, count_maxi = 0, 0
    for fspec in walk(root, recurse):
        for pattern, (type, func) in pyloc.lang_map.items():
            if fnmatch.fnmatch(fspec, pattern):
                logger.debug('%s TYPE=%s' % (fspec, type))
                mini,maxi = func(fspec)
                count_mini += mini
                count_maxi += maxi
                break
    return count_mini, count_maxi

def parse_args():
    parser = OptionParser(usage='%prog [options] [root1 root2 . . .]')
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', help='increase logging output')
    return (parser.parse_args(),parser)

def main():
    ((options, args), parser) = parse_args()

    if options.verbose:
        handler.setLevel(logging.DEBUG)

    values = []
    for target in args:
        if not os.path.exists(target):
            logger.error('file or directory not found: %s' % target)
        else:
            values.append((target, loc(target)))

    values.append(('TOTAL', 
                   (sum([x[1][0] for x in values]), 
                    sum([x[1][1] for x in values]))))
    max_dir_len = max([len(x[0]) for x in values])
    max_mini_len = max([len(str(x[1][0])) for x in values])
    max_maxi_len = max([len(str(x[1][1])) for x in values])

    for (dir, (mini, maxi)) in values:
        print '%-*s %*s %*s' % (max_dir_len, dir,
                               max_mini_len, mini,
                               max_maxi_len, maxi)

if __name__ == '__main__':
    main()
