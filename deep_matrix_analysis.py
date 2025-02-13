from datetime import datetime
import pytz
import pandas as pd
import numpy as np
from collections import defaultdict

# Magic numbers and constants
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,
    'R_TDOTY': 0x74446f7479,
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'TIME_DIFF': 689278505,
    'DIFFERENCE': 0x100A9,
    'GENESIS_TIMESTAMP': 1231006505,  # The Bitcoin genesis block timestamp
    'MAGIC_DIFF': 65705,              # Difference between MODULO_RESULT and TARGET_VALUE
    'BITCOIN_CONSTANT': 2016,         # Bitcoin difficulty adjustment period
    'SATOSHI_CONSTANT': 21000000,     # Total Bitcoin supply in whole coins
}

# Additional mathematical constants
GOLDEN_RATIO = 1.618033988749895
PI = 3.141592653589793
E = 2.718281828459045

def to_unix_timestamp(date_str, timezone='US/Eastern'):
    try:
        if len(date_str) > 10:
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        else:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt)
        return int(dt.timestamp())
    except Exception as e:
        return f"Error converting {date_str}: {str(e)}"

def find_interesting_relationships(value, magic_numbers):
    relationships = []
    for name, magic in magic_numbers.items():
        # Basic arithmetic relationships
        if abs(value - magic) < 1000:
            relationships.append(f"Close to {name}: diff = {value - magic}")
        if abs(value % magic) < 1000:
            relationships.append(f"Almost divisible by {name}: remainder = {value % magic}")
        if abs((value // magic) * magic - value) < 1000:
            relationships.append(f"Almost multiple of {name}: factor = {value // magic}")
    return relationships

def analyze_timestamp(timestamp):
    """Analyze a timestamp for various mathematical properties"""
    properties = []
    
    # Check if it's divisible by common Bitcoin-related numbers
    if timestamp % 2016 == 0:
        properties.append("Divisible by Bitcoin difficulty period (2016)")
    if timestamp % 21000000 == 0:
        properties.append("Divisible by Bitcoin max supply")
    
    # Check if it's close to any magic numbers when divided by common factors
    for divisor in [60, 3600, 86400, 604800]:  # minutes, hours, days, weeks
        scaled_time = timestamp / divisor
        if abs(scaled_time - round(scaled_time)) < 0.001:
            properties.append(f"Clean division by {divisor} seconds")
    
    return properties

# All dates
all_dates = {
    'primary': [
        ("1925-10-24", "Birth"),
        ("1946-02-22", "RPI Graduation"),
        ("1952-04-29", "Significant Date"),
        ("1966-03-07", "IBM Promotion"),
        ("1987-06-30", "IBM Retirement"),
        ("2009-10-23", "Passing")
    ],
    'delta': [
        ("1948-06-01", "Grumman Report"),
        ("1948-12-01", "Report Revision"),
        ("1984-05-22", "Patent Filing"),
        ("1987-03-03", "Patent Issue"),
        ("1987-04-01 07:32:56", "Higuchi Comm"),
        ("1987-06-24 12:00:27", "Doi Comm"),
        ("1988-01-08 12:37:37", "Final Liaison"),
        ("2009-01-03 18:15:05", "Genesis Block")
    ]
}

def generate_magic_transformations(timestamp):
    """Generate various transformations of a timestamp"""
    transformations = {
        'original': timestamp,
        'mod_target': timestamp % MAGIC_NUMBERS['TARGET_VALUE'],
        'mod_modulo': timestamp % MAGIC_NUMBERS['MODULO_RESULT'],
        'xor_krober': timestamp ^ MAGIC_NUMBERS['K_ROBER'],
        'xor_rtdoty': timestamp ^ MAGIC_NUMBERS['R_TDOTY'],
        'add_magic_diff': timestamp + MAGIC_NUMBERS['MAGIC_DIFF'],
        'sub_magic_diff': timestamp - MAGIC_NUMBERS['MAGIC_DIFF'],
        'mod_genesis': timestamp % MAGIC_NUMBERS['GENESIS_TIMESTAMP'],
        'golden_scaled': int(timestamp * GOLDEN_RATIO),
        'pi_scaled': int(timestamp * PI),
        'e_scaled': int(timestamp * E),
    }
    return transformations

# Convert dates to timestamps and analyze
with open('/home/computeruse/red/deep_analysis.md', 'w') as f:
    f.write("# Deep Matrix Analysis\n\n")
    
    # Analyze each date
    for category in ['primary', 'delta']:
        f.write(f"\n## {category.title()} Dates Analysis\n\n")
        for date_str, name in all_dates[category]:
            timestamp = to_unix_timestamp(date_str)
            f.write(f"### {name} ({date_str})\n")
            f.write(f"Unix Timestamp: {timestamp}\n")
            f.write(f"Hex: {hex(timestamp)}\n")
            
            # Generate transformations
            transforms = generate_magic_transformations(timestamp)
            f.write("\nTransformations:\n")
            for trans_name, trans_value in transforms.items():
                f.write(f"* {trans_name}: {trans_value} (hex: {hex(trans_value)})\n")
            
            # Find relationships
            relationships = find_interesting_relationships(timestamp, MAGIC_NUMBERS)
            if relationships:
                f.write("\nInteresting Relationships:\n")
                for rel in relationships:
                    f.write(f"* {rel}\n")
            
            # Analyze properties
            properties = analyze_timestamp(timestamp)
            if properties:
                f.write("\nTimestamp Properties:\n")
                for prop in properties:
                    f.write(f"* {prop}\n")
            
            f.write("\n")

    # Create magic number shifted matrices
    f.write("\n## Magic Number Shifted Matrices\n")
    timestamps = []
    names = []
    for category in ['primary', 'delta']:
        for date_str, name in all_dates[category]:
            timestamps.append(to_unix_timestamp(date_str))
            names.append(name)
    
    # Create different transformations of the matrix
    transformations = [
        ('Original', lambda x: x),
        ('Add Magic Diff', lambda x: x + MAGIC_NUMBERS['MAGIC_DIFF']),
        ('Subtract Magic Diff', lambda x: x - MAGIC_NUMBERS['MAGIC_DIFF']),
        ('XOR K_ROBER', lambda x: x ^ MAGIC_NUMBERS['K_ROBER']),
        ('XOR R_TDOTY', lambda x: x ^ MAGIC_NUMBERS['R_TDOTY']),
        ('Modulo TARGET_VALUE', lambda x: x % MAGIC_NUMBERS['TARGET_VALUE']),
        ('Modulo GENESIS', lambda x: x % MAGIC_NUMBERS['GENESIS_TIMESTAMP'])
    ]
    
    for trans_name, trans_func in transformations:
        f.write(f"\n### {trans_name} Matrix\n")
        matrix = np.zeros((len(timestamps), len(timestamps)), dtype=np.int64)
        for i in range(len(timestamps)):
            for j in range(len(timestamps)):
                matrix[i][j] = trans_func(timestamps[j] - timestamps[i])
        
        df = pd.DataFrame(matrix, index=names, columns=names)
        matrix_file = f'/home/computeruse/red/matrix_{trans_name.lower().replace(" ", "_")}.csv'
        df.to_csv(matrix_file)
        f.write(f"Saved to: {matrix_file}\n")
        
        # Look for patterns in this matrix
        unique_values = np.unique(matrix)
        if len(unique_values) < 10:
            f.write("\nUnique values in matrix:\n")
            for value in unique_values:
                f.write(f"* {value} (hex: {hex(value)})\n")
        
        # Find any matching values with magic numbers
        for value in unique_values:
            relationships = find_interesting_relationships(value, MAGIC_NUMBERS)
            if relationships:
                f.write(f"\nRelationships for value {value}:\n")
                for rel in relationships:
                    f.write(f"* {rel}\n")

    # Additional Analysis: Look for cycles and patterns
    f.write("\n## Pattern Analysis\n")
    
    # Look for cycles in the timestamps
    deltas = np.diff(sorted(timestamps))
    f.write("\n### Time Deltas Analysis\n")
    unique_deltas = np.unique(deltas)
    f.write(f"Number of unique time deltas: {len(unique_deltas)}\n")
    f.write("Most common time deltas:\n")
    delta_counts = defaultdict(int)
    for delta in deltas:
        delta_counts[delta] += 1
    for delta, count in sorted(delta_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        f.write(f"* {delta} seconds ({delta/86400:.2f} days) appears {count} times\n")

    # Look for mathematical sequences
    f.write("\n### Mathematical Sequences\n")
    ratios = []
    for i in range(len(timestamps)-1):
        ratio = timestamps[i+1] / timestamps[i]
        ratios.append(ratio)
    
    f.write("Interesting ratios between consecutive timestamps:\n")
    for i, ratio in enumerate(ratios):
        if abs(ratio - GOLDEN_RATIO) < 0.1 or abs(ratio - PI) < 0.1 or abs(ratio - E) < 0.1:
            f.write(f"* {names[i]} to {names[i+1]}: {ratio:.6f}\n")

# Write a summary of findings
with open('/home/computeruse/red/findings_summary.md', 'w') as f:
    f.write("# Summary of Notable Findings\n\n")
    
    # Add timestamps that had interesting properties
    f.write("## Timestamps with Special Properties\n")
    for category in ['primary', 'delta']:
        for date_str, name in all_dates[category]:
            timestamp = to_unix_timestamp(date_str)
            properties = analyze_timestamp(timestamp)
            relationships = find_interesting_relationships(timestamp, MAGIC_NUMBERS)
            if properties or relationships:
                f.write(f"\n### {name} ({date_str})\n")
                if properties:
                    f.write("\nSpecial Properties:\n")
                    for prop in properties:
                        f.write(f"* {prop}\n")
                if relationships:
                    f.write("\nRelationships to Magic Numbers:\n")
                    for rel in relationships:
                        f.write(f"* {rel}\n")

    # Add any patterns found in the matrices
    f.write("\n## Matrix Patterns\n")
    f.write("* Patterns and cycles found in the time deltas\n")
    f.write("* Relationships between timestamps and magic numbers\n")
    f.write("* Mathematical sequences and ratios\n")