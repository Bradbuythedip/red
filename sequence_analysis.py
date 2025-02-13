import numpy as np
from datetime import datetime

# Employment period timestamps
TIMESTAMPS = [
    -120596400,  # IBM Promotion
    454046400,   # Patent Filing
    541746000,   # Patent Issue
    544278776,   # Higuchi Comm
    551548827,   # Doi Comm
    552024000    # IBM Retirement
]

MAGIC_DIFF = 65705
TARGET_VALUE = 689278505
MODULO_RESULT = 689212800

def analyze_sequences():
    with open('/home/computeruse/red/sequence_patterns.md', 'w') as f:
        f.write("# Detailed Sequence Analysis\n\n")
        
        # Analyze differences between consecutive events
        diffs = np.diff(TIMESTAMPS)
        f.write("## Time Differences Analysis\n\n")
        for i, diff in enumerate(diffs):
            f.write(f"Difference {i+1}: {diff:,d} seconds\n")
            # Check if difference is related to magic numbers
            if diff % MAGIC_DIFF < 100:
                f.write(f"* Multiple of MAGIC_DIFF! ({diff // MAGIC_DIFF})\n")
            if diff % TARGET_VALUE < 1000:
                f.write(f"* Near multiple of TARGET_VALUE ({diff / TARGET_VALUE:.3f})\n")
            if diff % MODULO_RESULT < 1000:
                f.write(f"* Near multiple of MODULO_RESULT ({diff / MODULO_RESULT:.3f})\n")
            f.write("\n")
        
        # Look for arithmetic sequences
        second_diffs = np.diff(diffs)
        f.write("\n## Second-Order Differences\n\n")
        for i, diff2 in enumerate(second_diffs):
            f.write(f"Second-order difference {i+1}: {diff2:,d}\n")
            if abs(diff2) % MAGIC_DIFF < 100:
                f.write("* Related to MAGIC_DIFF!\n")
        
        # Analyze modulo patterns
        f.write("\n## Modulo Pattern Analysis\n\n")
        for base in [MAGIC_DIFF, TARGET_VALUE, MODULO_RESULT]:
            mods = [t % base for t in TIMESTAMPS]
            f.write(f"\nModulo {base} sequence:\n")
            for i, mod in enumerate(mods):
                f.write(f"{i+1}: {mod:,d}\n")
            
            # Check for patterns in modulo differences
            mod_diffs = np.diff(mods)
            if any(d == mod_diffs[0] for d in mod_diffs[1:]):
                f.write("* Regular pattern found in differences!\n")
        
        # Look for geometric relationships
        f.write("\n## Geometric Analysis\n\n")
        ratios = []
        for i in range(len(TIMESTAMPS)-1):
            if TIMESTAMPS[i] != 0:  # Avoid division by zero
                ratio = TIMESTAMPS[i+1] / TIMESTAMPS[i]
                ratios.append(ratio)
                f.write(f"Ratio {i+1}: {ratio:.6f}\n")
        
        # Check for specific relationships with magic numbers
        f.write("\n## Magic Number Relationships\n\n")
        for ts in TIMESTAMPS:
            ts_abs = abs(ts)  # Use absolute value for negative timestamps
            factors = []
            for i in range(1, int(np.sqrt(ts_abs)) + 1):
                if ts_abs % i == 0:
                    factors.append(i)
                    if i != ts_abs // i:
                        factors.append(ts_abs // i)
            
            interesting_factors = [f for f in factors if 
                                abs(f - MAGIC_DIFF) < 100 or 
                                abs(f - TARGET_VALUE) < 1000 or
                                abs(f - MODULO_RESULT) < 1000]
            
            if interesting_factors:
                dt = datetime.fromtimestamp(ts)
                f.write(f"\nTimestamp: {ts:,d} ({dt})\n")
                f.write("Interesting factors:\n")
                for factor in sorted(interesting_factors):
                    f.write(f"* {factor:,d}\n")

analyze_sequences()