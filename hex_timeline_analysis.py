from datetime import datetime, timezone
import pytz
from collections import defaultdict

# All significant hexadecimal values
HEX_VALUES = {
    # Original Magic Numbers
    'K_ROBER': 0x526f626572,        # "Rober"
    'R_TDOTY': 0x74446f7479,        # "tDoty"
    'MODULO_RESULT': 0x29148d80,    # 689212800
    'TARGET_VALUE': 0x29158e29,     # 689278505
    'MAGIC_DIFF': 0x100a9,          # 65705
    
    # Primary Date Timestamps
    'BIRTH': -0x531e0bb0,           # 1925-10-24
    'RPI_GRAD': -0x2cdfe8b0,        # 1946-02-22
    'IBM_START': -0x213f5400,       # 1952-04-29
    'IBM_RETIRE': 0x20e85100,       # 1987-06-30
    'PASSING': 0x4ae12a40,          # 2009-10-23
    
    # Delta Date Timestamps
    'GRUMMAN': -0x28944b00,         # 1948-06-01
    'REVISION': -0x27a4d100,        # 1948-12-01
    'MEMORY_PROG': -0x73027b0,      # 1966-03-07
    'PATENT_FILE': 0x1b1032c0,      # 1984-05-22
    'PATENT_ISSUE': 0x204a6350,     # 1987-03-03
    'HIGUCHI': 0x207108f8,          # 1987-04-01
    'DOI': 0x20dff79b,             # 1987-06-24
    'GENESIS': 0x49742cc9,          # 2009-01-03
    
    # Additional Derived Values
    'IBM_DURATION': 0x4227a500,     # Employment duration
    'LIFE_DURATION': 0x9DFF3600,    # Total lifespan
}

# Additional binary operation results
BINARY_OPS = {
    'XOR_KROBER': [
        ('BIRTH_KROBER_XOR', -0x523c7c6ede),
        ('RPI_KROBER_XOR', -0x5243bd8dde),
        ('START_KROBER_XOR', -0x523517c672),
        ('RETIRE_KROBER_XOR', 0x524f8552b2),
        ('PASS_KROBER_XOR', 0x524a58cf32)
    ],
    'XOR_RTDOTY': [
        ('BIRTH_RTDOTY_XOR', -0x7417717fd7),
        ('RPI_RTDOTY_XOR', -0x7468b09cd7),
        ('START_RTDOTY_XOR', -0x745a17d576),
        ('RETIRE_RTDOTY_XOR', 0x74648843b9),
        ('PASS_RTDOTY_XOR', 0x745f584e39)
    ]
}

def hex_to_date(hex_val):
    """Convert hex value to date, handling both positive and negative timestamps"""
    try:
        # Convert to integer timestamp
        if isinstance(hex_val, str):
            timestamp = int(hex_val, 16)
        else:
            timestamp = int(hex_val)
        
        # Convert to datetime
        dt = datetime.fromtimestamp(timestamp, timezone.utc)
        return dt, timestamp
    except Exception as e:
        return f"Invalid timestamp: {hex_val} ({str(e)})", None

def analyze_hex_timeline():
    with open('/home/computeruse/red/hex_timeline.md', 'w') as f:
        f.write("# Comprehensive Hexadecimal Timeline Analysis\n\n")
        
        # Process all hex values
        timeline_entries = []
        value_relationships = defaultdict(list)
        
        # Process main hex values
        f.write("## 1. Primary Hexadecimal Values\n\n")
        f.write("```\n")
        for name, hex_val in HEX_VALUES.items():
            dt, timestamp = hex_to_date(hex_val)
            if isinstance(dt, datetime):
                timeline_entries.append((timestamp, dt, name, hex_val))
                f.write(f"{name}:\n")
                f.write(f"  Hex: {hex(hex_val)}\n")
                f.write(f"  Dec: {timestamp:,d}\n")
                f.write(f"  Date: {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
        f.write("```\n\n")
        
        # Process binary operations
        f.write("## 2. Binary Operation Results\n\n")
        f.write("```\n")
        for op_type, operations in BINARY_OPS.items():
            f.write(f"\n{op_type}:\n")
            for name, hex_val in operations:
                dt, timestamp = hex_to_date(hex_val)
                if isinstance(dt, datetime):
                    timeline_entries.append((timestamp, dt, name, hex_val))
                    f.write(f"  {name}:\n")
                    f.write(f"    Hex: {hex(hex_val)}\n")
                    f.write(f"    Dec: {timestamp:,d}\n")
                    f.write(f"    Date: {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        f.write("```\n\n")
        
        # Sort timeline entries
        timeline_entries.sort()
        
        # Create visual timeline
        f.write("## 3. Visual Timeline\n\n")
        f.write("```\n")
        min_ts = min(entry[0] for entry in timeline_entries)
        max_ts = max(entry[0] for entry in timeline_entries)
        timeline_range = max_ts - min_ts
        
        for ts, dt, name, hex_val in timeline_entries:
            position = int(100 * (ts - min_ts) / timeline_range)
            line = "." * position + "●" + "." * (100 - position)
            f.write(f"{line} {dt.strftime('%Y-%m-%d')} | {name} | {hex(hex_val)}\n")
        f.write("```\n\n")
        
        # Analyze relationships between hex values
        f.write("## 4. Hexadecimal Relationships\n\n")
        
        # XOR relationships
        f.write("### XOR Patterns\n```\n")
        for i, (ts1, dt1, name1, hex1) in enumerate(timeline_entries):
            for ts2, dt2, name2, hex2 in timeline_entries[i+1:]:
                xor_result = hex1 ^ hex2
                if xor_result in HEX_VALUES.values() or abs(xor_result) in HEX_VALUES.values():
                    f.write(f"{name1} XOR {name2} = {hex(xor_result)}\n")
                    matching_name = [k for k, v in HEX_VALUES.items() if v == xor_result or v == abs(xor_result)]
                    if matching_name:
                        f.write(f"  Matches {matching_name[0]}!\n")
        f.write("```\n\n")
        
        # Addition/Subtraction patterns
        f.write("### Addition/Subtraction Patterns\n```\n")
        for i, (ts1, dt1, name1, hex1) in enumerate(timeline_entries):
            for ts2, dt2, name2, hex2 in timeline_entries[i+1:]:
                diff = abs(hex1 - hex2)
                if diff in HEX_VALUES.values() or diff in [abs(x) for x in HEX_VALUES.values()]:
                    f.write(f"|{name1} - {name2}| = {hex(diff)}\n")
                    matching_name = [k for k, v in HEX_VALUES.items() if v == diff or v == abs(diff)]
                    if matching_name:
                        f.write(f"  Matches {matching_name[0]}!\n")
        f.write("```\n\n")
        
        # Check for patterns in hexadecimal digits
        f.write("## 5. Hexadecimal Digit Patterns\n\n")
        digit_patterns = defaultdict(int)
        for _, _, name, hex_val in timeline_entries:
            hex_str = hex(abs(hex_val))[2:]  # Remove '0x' prefix
            for i in range(len(hex_str)-1):
                pattern = hex_str[i:i+2]
                digit_patterns[pattern] += 1
        
        # Show most common patterns
        f.write("Most common 2-digit patterns:\n```\n")
        for pattern, count in sorted(digit_patterns.items(), key=lambda x: x[1], reverse=True)[:10]:
            if count > 1:
                f.write(f"Pattern '{pattern}': {count} occurrences\n")
        f.write("```\n")

# Run the analysis
analyze_hex_timeline()