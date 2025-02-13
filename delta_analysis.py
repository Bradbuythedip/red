from datetime import datetime
import pytz
import pandas as pd
import numpy as np
from collections import defaultdict

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

def format_time_delta(seconds):
    years = seconds / (365.25 * 24 * 3600)
    days = seconds / (24 * 3600)
    hours = seconds / 3600
    return f"{seconds:,d} sec ({days:.2f} days) ({years:.2f} years)"

# Special values from Robert Doty's note
SPECIAL_VALUES = {
    'K_ROBER': 0x526f626572,
    'R_TDOTY': 0x74446f7479,
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'TIME_DIFF': 689278505,
    'DIFFERENCE': 0x100A9
}

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

# Convert all dates to timestamps
timestamps = {}
for category in ['primary', 'delta']:
    timestamps[category] = [(to_unix_timestamp(date), name) for date, name in all_dates[category]]

# Calculate all possible deltas
deltas = defaultdict(list)
all_ts = timestamps['primary'] + timestamps['delta']

for i, (ts1, name1) in enumerate(all_ts):
    for j, (ts2, name2) in enumerate(all_ts[i+1:], i+1):
        delta = abs(ts2 - ts1)
        deltas[delta].append((name1, name2))

# Find matching deltas (deltas that appear multiple times)
matching_deltas = {delta: pairs for delta, pairs in deltas.items() if len(pairs) > 1}

# Generate the analysis
with open('/home/computeruse/red/delta_analysis.md', 'w') as f:
    # Write header
    f.write("# Delta Analysis for F.C. Doty Timeline\n\n")
    
    # Special values section
    f.write("## Special Values\n")
    for name, value in SPECIAL_VALUES.items():
        f.write(f"* {name}: {value:,d}\n")
    f.write("\n")
    
    # Matching deltas section
    f.write("## Matching Time Deltas\n")
    for delta, pairs in sorted(matching_deltas.items()):
        f.write(f"\n### Delta: {format_time_delta(delta)}\n")
        f.write("Matching pairs:\n")
        for pair in pairs:
            f.write(f"* {pair[0]} → {pair[1]}\n")
    
    # Special value relationships
    f.write("\n## Relationships to Special Values\n")
    for name, value in SPECIAL_VALUES.items():
        f.write(f"\n### {name} Relationships\n")
        close_matches = []
        for cat in timestamps.values():
            for ts, ts_name in cat:
                diff = abs(value - ts)
                if diff < 31536000:  # Within 1 year
                    close_matches.append((ts_name, diff))
        if close_matches:
            f.write(f"Events within 1 year of {value:,d}:\n")
            for event, diff in sorted(close_matches, key=lambda x: x[1]):
                f.write(f"* {event}: {format_time_delta(diff)}\n")

    # Generate timeline visualization
    f.write("\n## Timeline Visualization\n```\n")
    timeline = []
    for cat in timestamps.values():
        for ts, name in cat:
            timeline.append((ts, name))
    
    timeline.sort()
    min_ts = min(t[0] for t in timeline)
    max_ts = max(t[0] for t in timeline)
    
    for ts, name in timeline:
        position = int(50 * (ts - min_ts) / (max_ts - min_ts))
        line = "." * position + "●" + "." * (50 - position)
        date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        f.write(f"{line} {date} | {name}\n")
    f.write("```\n")

# Create CSV with all deltas
df = pd.DataFrame(index=[name for _, name in all_ts])
for i, (ts1, name1) in enumerate(all_ts):
    deltas = []
    for ts2, name2 in all_ts:
        deltas.append(ts2 - ts1)
    df[name1] = deltas

df.to_csv('/home/computeruse/red/delta_matrix.csv')