import urllib

def by_language(rslt, cat, title):
    '''create google-chart URL for a particular category over all
    filetypes
    '''
    types = rslt.types()
    counts = []
    for t in types:
        try:
            counts.append(rslt.counts_by_type(t)[cat])
        except KeyError:
            counts.append(0)

    # the data values must be scaled between 0 and 100.0.
    max_val = max(counts)
    if max_val == 0: max_val = 1
    counts = [c / float(max_val) for c in counts]

    counts = ','.join([str(c) for c in counts])
    types = '|'.join(types)

    params = urllib.urlencode({
            'chs' : '500x200',
            'chd' : 't:%s' % counts,
            'cht' : 'p3',
            'chl' : types,
            'chtt' : title,
            })

    return 'http://chart.apis.google.com/chart?%s' % params

def by_type(rslt, type, title):
    '''create a google-chart URL for a particular file-type over all
    categories'''

    categories = rslt.categories()
    categories.remove('total')
    counts = []
    keep_categories = []
    for cat in list(categories):
        try:
            counts.append(rslt.counts_by_category(cat)[type])
        except KeyError:
            categories.remove(cat)

    max_val = max(counts)
    if max_val == 0: max_val = 1
    counts = [c / float(max_val) for c in counts]
    
    counts = ','.join([str(c) for c in counts])
    categories = '|'.join(categories)

    params = urllib.urlencode({
            'chs' : '500x200',
            'chd' : 't:%s' % counts,
            'cht' : 'p3',
            'chl' : categories,
            'chtt' : title,
            })

    return 'http://chart.apis.google.com/chart?%s' % params
    
