from datetime import datetime
import pytz
import numpy as np
import pandas as pd
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 50

def to_unix_timestamp(date_str, timezone='US/Eastern'):
    try:
        if len(date_str) > 10:  # If time is included
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        else:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt)
        return int(dt.timestamp())
    except Exception as e:
        return f"Error converting {date_str}: {str(e)}"

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

# All significant dates
DATES = [
    # Primary dates
    ("1925-10-24", "BIRTH", "P1"),
    ("1933-04-05", "EXECUTIVE ORDER 6102", "H1"),  # Adding April 5, 1933
    ("1946-02-22", "RPI GRADUATION", "P2"),
    ("1952-04-29", "IBM START", "P3"),
    ("1987-06-30", "IBM RETIREMENT", "P4"),
    ("2009-10-23", "PASSING", "P5"),
    
    # Delta dates
    ("1948-06-01", "GRUMMAN REPORT", "D1"),
    ("1948-12-01", "REPORT REVISION", "D2"),
    ("1966-03-07", "MEMORY PROGRAM", "D3"),
    ("1984-05-22", "PATENT FILING", "D4"),
    ("1987-03-03", "PATENT ISSUE", "D5"),
    ("1987-04-01 07:32:56", "HIGUCHI COMM", "D6"),
    ("1987-06-24 12:00:27", "DOI COMM", "D7"),
    ("2009-01-03 18:15:05", "GENESIS BLOCK", "D8")
]

def analyze_2d_timeline():
    # Convert dates to timestamps
    timestamps = []
    for date, name, code in DATES:
        ts = to_unix_timestamp(date)
        timestamps.append((ts, name, code))
    
    # Sort by timestamp
    timestamps.sort(key=lambda x: x[0])
    
    with open('/home/computeruse/red/2d_timeline.md', 'w') as f:
        f.write("# 2D Timeline Analysis\n\n")
        
        # Create chronological timeline
        f.write("## Chronological Timeline\n```\n")
        min_ts = min(ts for ts, _, _ in timestamps)
        max_ts = max(ts for ts, _, _ in timestamps)
        timeline_range = max_ts - min_ts
        
        for ts, name, code in timestamps:
            position = int(100 * (ts - min_ts) / timeline_range)
            line = "." * position + "●" + "." * (100 - position)
            date = datetime.fromtimestamp(ts)
            f.write(f"{line} {date.strftime('%Y-%m-%d')} | {code} | {name}\n")
        f.write("```\n\n")
        
        # Create delta matrix
        f.write("## Delta Matrix (in days)\n")
        n = len(timestamps)
        matrix = np.zeros((n, n))
        
        # Calculate deltas
        for i in range(n):
            for j in range(n):
                delta = (timestamps[j][0] - timestamps[i][0]) / 86400  # Convert to days
                matrix[i][j] = delta
        
        # Convert to DataFrame for better display
        df = pd.DataFrame(
            matrix,
            columns=[f"{code}" for _, _, code in timestamps],
            index=[f"{code}" for _, _, code in timestamps]
        )
        
        # Save matrix to CSV
        df.to_csv('/home/computeruse/red/delta_matrix.csv')
        f.write("Delta matrix saved to delta_matrix.csv\n\n")
        
        # Analyze significant deltas
        f.write("## Significant Time Deltas\n\n")
        
        # Look for deltas that are related to magic numbers
        significant_deltas = []
        for i in range(n):
            for j in range(i+1, n):
                delta = timestamps[j][0] - timestamps[i][0]
                
                # Check relationships with magic numbers
                for magic_name, magic_value in MAGIC_NUMBERS.items():
                    # Check if delta is close to a multiple of magic number
                    if abs(delta % magic_value) < 1000 or abs(magic_value - (delta % magic_value)) < 1000:
                        significant_deltas.append({
                            'from': timestamps[i][2],
                            'to': timestamps[j][2],
                            'delta': delta,
                            'relationship': f"Near multiple of {magic_name}",
                            'remainder': delta % magic_value
                        })
                    
                    # Check if delta divided by magic number is close to golden ratio
                    ratio = delta / magic_value
                    if abs(ratio - 1.618033988749895) < 0.01:
                        significant_deltas.append({
                            'from': timestamps[i][2],
                            'to': timestamps[j][2],
                            'delta': delta,
                            'relationship': f"Golden ratio with {magic_name}",
                            'ratio': ratio
                        })
        
        # Write significant deltas
        for delta in significant_deltas:
            f.write(f"### {delta['from']} to {delta['to']}\n")
            f.write(f"Delta: {delta['delta']:,d} seconds\n")
            f.write(f"Relationship: {delta['relationship']}\n")
            if 'remainder' in delta:
                f.write(f"Remainder: {delta['remainder']:,d} seconds\n")
            if 'ratio' in delta:
                f.write(f"Ratio: {delta['ratio']:.12f}\n")
            f.write("\n")
        
        # Special analysis of April 5, 1933 (Executive Order 6102)
        f.write("## Special Analysis: Executive Order 6102 (April 5, 1933)\n\n")
        eo6102_ts = to_unix_timestamp("1933-04-05")
        
        for ts, name, code in timestamps:
            if ts != eo6102_ts:
                delta = abs(ts - eo6102_ts)
                f.write(f"### To {code} ({name})\n")
                f.write(f"Delta: {delta:,d} seconds ({delta/86400:.2f} days)\n")
                
                # Check for relationships with magic numbers
                for magic_name, magic_value in MAGIC_NUMBERS.items():
                    if abs(delta % magic_value) < 1000:
                        f.write(f"* Related to {magic_name} (remainder: {delta % magic_value})\n")
                f.write("\n")

        # Look for overlapping patterns
        f.write("## Overlapping Patterns\n\n")
        all_deltas = []
        for i in range(n):
            for j in range(i+1, n):
                delta = timestamps[j][0] - timestamps[i][0]
                all_deltas.append((delta, timestamps[i][2], timestamps[j][2]))
        
        # Sort deltas and look for similar values
        all_deltas.sort()
        for i in range(len(all_deltas)-1):
            if abs(all_deltas[i][0] - all_deltas[i+1][0]) < 86400:  # Within 1 day
                f.write(f"Similar deltas found:\n")
                f.write(f"* {all_deltas[i][1]} to {all_deltas[i][2]}: {all_deltas[i][0]:,d} seconds\n")
                f.write(f"* {all_deltas[i+1][1]} to {all_deltas[i+1][2]}: {all_deltas[i+1][0]:,d} seconds\n")
                f.write(f"Difference: {abs(all_deltas[i][0] - all_deltas[i+1][0]):,d} seconds\n\n")

# Run the analysis
analyze_2d_timeline()