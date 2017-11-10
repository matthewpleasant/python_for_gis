# landUse.py
# Purpose: Practice performing dictionary operations.
# Usage: No arguments needed.

landUse = {'res': 1, 'com': 2, 'ind': 3, 'other': [4, 5, 6, 7]}

ans1 = landUse['com']
print "1. Print the value of the item with key 'com': {0}".format(ans1)

ans2 = 'res' in landUse
print "2. Check if the dictionary has key 'res': {0}".format(ans2)

landUse['ind'] = landUse['com'] + 1
ans3 = landUse['ind']
print "3. Increment the value of the item with key 'ind': {0}".format(ans3)

landUse['agr'] = 0
print "4. Add an item with land use 'agr'  a value of 0:"
print landUse

landUse['res'] = 10
print "5. Change land use 'res' value to 10."
print landUse

print '6. Print a list of the dictionary keys:'
print landUse.keys()

print '7. Print the dictionary values:'
for value in landUse.values():
    print value

print '8. Print a list of the dictionary items:'
print landUse.items()

del landUse['ind']
print "9. Delete the item with key 'ind':"
print landUse

ans10 = 'ind' in landUse
print "10. Check for membership of the key 'ind': {0}".format(ans10)
