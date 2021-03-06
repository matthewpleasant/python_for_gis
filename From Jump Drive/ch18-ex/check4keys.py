# check4keys.py
# Purpose: Check if the input number(s) are in the dictionary.
# Usage: One or more number

import sys

d = {21: 1, 22: 4, 23: 18, 24: 2, 25: 17, 26: 2, 27: 18,
     31: 6, 33: 22, 34: 21, 35: 17, 37: 15, 39: 27, 41: 19,
     44: 28, 45: 26, 46: 18, 49: 19, 51: 16, 52: 29, 53: 17,
     54: 1, 55: 7, 59: 7, 61: 21, 63: 20, 64: 7, 65: 10,
     66: 10, 68: 4, 70: 22, 71: 17, 74: 17, 75: 8, 78: 17,
     79: 11, 80: 25, 82: 8, 83: 15, 85: 21}
values = sys.argv[1:]
for value in values:
    num = float(value)
    if num in d:
        print 'Key {0} has value: {1}'.format(num, d[num])
    else:
        print 'Key {0} not found.'.format(num)
