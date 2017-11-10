# multiwayDict.py
# Purpose: Generate a list of sea level rise (SLR) for each year
#          based on  an IPCC scenario.
# Usage: sea_level_rise_model time_interval
#        SLR should be B1, A1T, B2, A1B, A2, or A1F1;
#        time_interval must be between 1 and 100
# Example input:  AIB 50
import sys

# Input sea level rise model: B1, A1T, B2, A1B, A2, or A1F1
sres = sys.argv[1]

# Input time interval to examine sea level rise
#      (Must be integer between 1 and 100)
interval = int(sys.argv[2])

rateDict = {'B1': 0.0038, 'A1T': 0.0045, 'B2': 0.0043,
            'A1B': 0.0048, 'A2': 0.0051, 'A1F1': 0.0059}

if sres not in rateDict:
    print "Warning: Invalid resolution. Choose B1, A1T, B2, A1B, A2, or A1F1."
    sys.exit()

# Generate a list of sea level rise (SLR) based in the IPCC scenario for each year
print "Running Sea Level Rise Model for ",  sres
valList = []
elev = 0                            # Set a baseline elevation
for year in range(0, 101, interval):
    rate = rateDict[sres]           # mm increase in SL
    elev = elev + (rate * interval)
    valList.append(elev)
print valList
