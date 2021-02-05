'''
Functions of general purpose
'''


def fortnight_number(date):
    ''' Calculate fortnight number based on a date '''
    month = date.month
    day = date.day
    year = date.year

    fn = month * 2

    if day >= 1 and day <= 15:
        fn = fn - 1

    return '{}{:02}'.format(year, fn)
