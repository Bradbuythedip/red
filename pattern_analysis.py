import numpy as np
from datetime import datetime, timedelta

# Define key constants
TARGET_VALUE = 689278505
MAGIC_DIFF = 65705
GENESIS_TIMESTAMP = 1231006505

def analyze_time_patterns(timestamp):
    """Analyze a timestamp for specific patterns related to TARGET_VALUE"""
    patterns = []
    
    # Check if adding/subtracting MAGIC_DIFF creates interesting values
    magic_added = timestamp + MAGIC_DIFF
    magic_subtracted = timestamp - MAGIC_DIFF
    
    # Look for relationships with TARGET_VALUE
    if magic_added % TARGET_VALUE < 1000 or magic_added % TARGET_VALUE > TARGET_VALUE - 1000:
        patterns.append(f"Adding MAGIC_DIFF creates near-multiple of TARGET_VALUE: {magic_added}")
    
    if magic_subtracted % TARGET_VALUE < 1000 or magic_subtracted % TARGET_VALUE > TARGET_VALUE - 1000:
        patterns.append(f"Subtracting MAGIC_DIFF creates near-multiple of TARGET_VALUE: {magic_subtracted}")
    
    # Check for relationship with Genesis block
    genesis_diff = abs(GENESIS_TIMESTAMP - timestamp)
    if genesis_diff % MAGIC_DIFF < 100:
        patterns.append(f"Difference with Genesis is multiple of MAGIC_DIFF: {genesis_diff}")
    
    return patterns

# Original timestamps from the timeline
timestamps = [
    -1394478000,  # Birth
    -752871600,   # RPI Graduation
    -557784000,   # Significant Date
    -120596400,   # IBM Promotion
    552024000,    # IBM Retirement
    1256270400,   # Passing
]

with open('/home/computeruse/red/time_patterns.md', 'w') as f:
    f.write("# Time Pattern Analysis\n\n")
    
    # Analyze each timestamp
    for ts in timestamps:
        date = datetime.fromtimestamp(ts)
        f.write(f"\n## Timestamp: {ts} ({date})\n")
        
        patterns = analyze_time_patterns(ts)
        if patterns:
            f.write("\nPatterns found:\n")
            for pattern in patterns:
                f.write(f"* {pattern}\n")
        
        # Look for relationships with other timestamps
        f.write("\nRelationships with other dates:\n")
        for other_ts in timestamps:
            if other_ts != ts:
                diff = abs(other_ts - ts)
                if diff % MAGIC_DIFF < 100:
                    f.write(f"* Difference with {datetime.fromtimestamp(other_ts)} is related to MAGIC_DIFF: {diff}\n")
                if diff % TARGET_VALUE < 1000:
                    f.write(f"* Difference with {datetime.fromtimestamp(other_ts)} is near multiple of TARGET_VALUE: {diff}\n")
        
        # Check for cyclic patterns
        cycles = []
        for i in range(1, 101):  # Check first 100 multiples
            cycle_time = ts + (TARGET_VALUE * i)
            cycle_date = datetime.fromtimestamp(cycle_time)
            if cycle_date.year <= 2025:  # Only include cycles up to current year
                cycles.append((i, cycle_date))
        
        if cycles:
            f.write("\nCycles (multiples of TARGET_VALUE):\n")
            for i, cycle_date in cycles:
                f.write(f"* Cycle {i}: {cycle_date}\n")
                
    # Look for overall patterns
    f.write("\n## Overall Patterns\n")
    
    # Calculate all differences between timestamps
    differences = []
    for i, ts1 in enumerate(timestamps):
        for ts2 in timestamps[i+1:]:
            diff = abs(ts2 - ts1)
            differences.append(diff)
    
    # Find common factors
    common_factors = []
    for i in range(1, min(differences) + 1):
        if all(diff % i == 0 for diff in differences):
            common_factors.append(i)
    
    f.write("\nCommon factors across all time differences:\n")
    for factor in common_factors[-10:]:  # Show the 10 largest common factors
        f.write(f"* {factor}\n")
    
    # Check for relationships with Bitcoin-specific numbers
    f.write("\nBitcoin-related patterns:\n")
    bitcoin_constants = [2016, 21000000, 50, 210000]
    for const in bitcoin_constants:
        relations = []
        for diff in differences:
            if diff % const < 100 or diff % const > const - 100:
                relations.append(diff)
        if relations:
            f.write(f"\nNear multiples of {const}:\n")
            for rel in relations[:5]:  # Show first 5 examples
                f.write(f"* {rel}\n")