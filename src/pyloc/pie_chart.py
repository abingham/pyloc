def by_language(rslt, cat, title):
    types = rslt.types()
    counts = []
    for t in types:
        try:
            counts.append(rslt.counts_by_type(t)[cat])
        except KeyError:
            counts.append(0)

    counts = ','.join([str(c) for c in counts])
    types = '|'.join(types)
    print 'http://chart.apis.google.com/chart?chs=250x100&chd=t:%s&cht=p3&chl=%s&chtt=%s' % (counts,types,title)
