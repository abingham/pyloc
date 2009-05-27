import urllib

def by_language(rslt, cat, title):
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
