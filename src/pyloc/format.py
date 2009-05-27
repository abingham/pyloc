from cStringIO import StringIO

SEPARATOR = None

def print_table(fields, rows):
    widths = {}
    for field in fields:
        widths[field] = len(field)
        for row in rows:
            if row is SEPARATOR:
                continue
            try:
                widths[field] = max(widths[field],
                                    len(str(row[field])))
            except KeyError:
                pass
    
    io = StringIO()

    io.write(' '.join(['%*s' % (widths[field], field) for field in fields]))
    io.write('\n')

    sums = {}
    for row in rows:
        if row is SEPARATOR:
            io.write(' '.join(['%*s' % (widths[field], '-' * widths[field]) for field in fields]))
        else:
            for field in fields:
                try:
                    io.write('%*s ' % (widths[field], row[field]))
                except KeyError:
                    io.write('%*s ' % (widths[field], ' ' * widths[field]))
            
        io.write('\n')

    return io.getvalue()

def by_language(rslt):
    categories = rslt.categories()
    types = rslt.types()

    rows = [SEPARATOR]
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
    rows.append(SEPARATOR)
    rows.append(sum_row)

    categories = ['type'] + categories

    return print_table(categories, rows)
