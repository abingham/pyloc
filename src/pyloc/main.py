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

def format_by_language(rslt):
    categories = rslt.categories()
    types = rslt.types()

    rows = [pyloc.format.SEPARATOR]
    sum_row = {}
    for filetype in types:
        fields = rslt.counts_by_type(filetype)
        fields['type'] = filetype
        rows.append(fields)
        for cat,count in fields.items():
            try:
                sum_row[cat] += count
            except KeyError:
                sum_row[cat] = count

    sum_row['type'] = 'SUM'
    rows.append(pyloc.format.SEPARATOR)
    rows.append(sum_row)

    categories = ['type'] + categories

    pyloc.format.print_table(categories, rows)

def format_by_language_(values):
    '''print out results on a per-language basis
    
    :param values: { filename -> (root, filetype, { catg -> count } ) }
    '''
    field_sizes = { 'file type' : len('file type') }
    headings = ['file type']

    # convert values to {filetype -> {catg -> count} }
    type_sums = {}
    for value in values.values():
        lang = value[1]
        counts = value[2]
        counts['file count'] = 1

        try:
            for cat,count in counts.items():
                type_sums[lang][cat] += count
        except KeyError:
            type_sums[lang] = counts
    values = type_sums

    sums = {}
    categories = set()
    for filetype, counts in values.items():
        field_sizes['file type'] = max(field_sizes['file type'],
                                       len(filetype))
        for cat,count in counts.items():
            categories.add(cat)
            try:
                field_sizes[cat] = max(field_sizes[cat],
                                       len(cat),
                                       len(str(count)))
                sums[cat] += count
            except KeyError:
                field_sizes[cat] = max(len(cat),
                                       len(str(count)))
                sums[cat] = count

    categories = list(categories)
    headings += categories

    io = StringIO()

    io.write(' '.join(['%*s' % (field_sizes[heading], heading) for heading in headings]))
    io.write('\n')
    io.write(' '.join(['%*s' % (field_sizes[heading], '-' * field_sizes[heading]) for heading in headings]))
    io.write('\n')

    for filetype, counts in values.items():
        io.write('%*s' % (field_sizes['file type'], filetype))
        for cat in categories:
            try:
                val = counts[cat]
            except:
                val = ''
            io.write(' %*s' % (field_sizes[cat], val))
        io.write('\n')

    io.write(' '.join(['%*s' % (field_sizes[heading], '-' * field_sizes[heading]) for heading in headings]))
    io.write('\n')        

    io.write('%*s' % (field_sizes['file type'], 'TOTAL'))
    for cat in categories:
        io.write(' %*s' % (field_sizes[cat], sums[cat]))
    io.write('\n')

    print io.getvalue()

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

    rslt = loc(args)

    format_by_language(rslt)

if __name__ == '__main__':
    main()
