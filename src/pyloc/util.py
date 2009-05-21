import fnmatch
import os, os.path

import pyloc

from .logger import logger,handler

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
    sums = {}
    for fspec in walk(root, recurse):
        for pattern, (type, func) in pyloc.lang_map.items():
            if fnmatch.fnmatch(fspec, pattern):
                logger.debug('%s TYPE=%s' % (fspec, type))
                for k,v in func(open(fspec, 'r')).items():
                    try:
                        sums[k] += v
                    except KeyError:
                        sums[k] = v
                break
    return sums
