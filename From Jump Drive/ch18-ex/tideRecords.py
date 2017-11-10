# tideRecords.py
# Purpose: Practice performing dictionary operations.
# Usage: No arguments needed.

tides = {'G1': [1, 6], 'G2': [2], 'G3': [3, 8, 9]}

# Add an item for gauge 'G5' to the dictionary. Record the only
# reading so far, 2, in the new value list.
tides['G5'] = [2]
print '1.  {0}'.format(tides)

# Append a second reading (6) to the 'G5' list.
tides['G5'].append(6)
print '2.  {0}'.format(tides)

# Remove the last reading from the 'G3' list using the 'pop' list method.
tides['G3'].pop()
print '3.  {0}'.format(tides)

# Add an item for gauge 'G6' to the dictionary.
# There are no reading from this gauge yet, so the value should be an empty list.
tides['G6'] = []

print '4.  {0}'.format(tides)

# Gauge 3 is no longer collecting data.  Remove this item from the list.append
del tides['G3']
print '5.  {0}'.format(tides)

# Gauge 1 recorded the measurements twices as high as they should be.
# Use list comprehension to correct this error.
tides['G1'] = [i/2.0 for i in tides['G1']]
print '6.  {0}'.format(tides)
