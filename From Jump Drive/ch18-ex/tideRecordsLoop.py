# tideRecordsLoop.py
# Purpose: Practice performing dictionary operations.
# Usage: No arguments needed.


tides = {'G1': [1, 6], 'G2': [2], 'G3': [3, 8, 9]}

# Append 7 to the list for every item (Then print the dictionary).
for k in tides.keys():
    tides[k].append(7)
print '1.  {0}'.format(tides)

# Print the number of readings for each gauge.
for v in tides.values():
    print '2. Number of readings: {0}'.format(len(v))

# Square the value of every reading for every gauge.
for k, v in tides.items():
    squared = [i**2 for i in v]
    tides[k] = squared
print '3.  {0}'.format(tides)

# Find the minimum reading for each gauge in the dictionary.
for k, v in tides.items():
    m = min(v)
    print '4. Min reading at gauge {0} = {1}'.format(k, m)
