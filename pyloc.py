'''lines-of-code counter for python

shamelessly stolen from http://code.activestate.com/recipes/527746/
'''

from optparse import OptionParser
import os
import fnmatch

def walk(root='.', recurse=True, pattern='*'):
    '''generate a files in a directory tree walk matching a pattern
    
    Walks a directory tree, generating the files it finds that match a
    provided pattern

    :param root: the root of the tree
    :param recurse: whether to recurse

    :param pattern: a regular expression pattern for matching against
                    filenames
    '''
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
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
    for fspec in walk(root, recurse, '*.py'):
        skip = False
        for line in open(fspec).readlines():
            count_maxi += 1
            
            line = line.strip()
            if line:
                if line.startswith('#'):
                    continue
                if line.startswith('"""'):
                    skip = not skip
                    continue
                if not skip:
                    count_mini += 1

    return count_mini, count_maxi

def parse_args():
    parser = OptionParser(usage='%prog [options] [dir1 dir2 . . .]')
    return (parser.parse_args(),parser)

def main():
    ((options, args), parser) = parse_args()

    values = [(dir, loc(dir)) for dir in args]
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
