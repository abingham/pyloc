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

def process_file(fspec, results, root):
    for pattern, (type, func) in pyloc.lang_map.items():
        if fnmatch.fnmatch(fspec, pattern):
            logger.info('%s TYPE=%s PATTERN=%s' % (fspec, type, pattern))
            
            try:
                results.add_result(fspec, root, type, 
                                   func(open(fspec, 'r')))
            except IOError:
                logger.warning('IOError on %s' % fspec)
                pass
            
            return True
    return False

def loc_(results, root='', recurse=True):
    '''count lines of code in a directory structure

    Sums all Python files in the specified folder.
    By default recurses through subfolders.

    :param root: the root of the tree to search
    :param recurse: whether to recurse
    '''

    for fspec in walk(root, recurse):
        if not process_file(fspec, results, root):
            logger.info('No matching pattern for %s. Lines not counted.' % fspec)

def loc(targets, 
        results,
        recurse=True):
    for tgt in targets:
        loc_(results, tgt, recurse)
