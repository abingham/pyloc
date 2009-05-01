def loc(filename):
    '''count lines of code in python files'''

    count_maxi = 0
    count_mini = 0

    skip = False
    for line in open(filename).readlines():
        count_maxi += 1
            
        # TODO: The counting of ''' comments is wrong. It definitely
        # is not doing balancing correctly.

        line = line.strip()
        if line:
            if line.startswith('#'):
                continue
            elif line.startswith('"""'):
                skip = not skip
                continue
            elif not skip:
                count_mini += 1

    return count_mini, count_maxi
