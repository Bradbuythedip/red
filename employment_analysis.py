from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

# Key constants
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,
    'R_TDOTY': 0x74446f7479,
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

# Employment period dates
EMPLOYMENT_DATES = [
    ("1966-03-07", "IBM Promotion", -120596400),
    ("1984-05-22", "Patent Filing", 454046400),
    ("1987-03-03", "Patent Issue", 541746000),
    ("1987-04-01 07:32:56", "Higuchi Comm", 544278776),
    ("1987-06-24 12:00:27", "Doi Comm", 551548827),
    ("1987-06-30", "IBM Retirement", 552024000)
]

def apply_magic_modulo(timestamp):
    """Apply various modulo operations and transformations"""
    results = {
        'timestamp': timestamp,
        'mod_target': timestamp % MAGIC_NUMBERS['TARGET_VALUE'],
        'mod_modulo': timestamp % MAGIC_NUMBERS['MODULO_RESULT'],
        'mod_genesis': timestamp % MAGIC_NUMBERS['GENESIS'],
        'mod_diff': timestamp % MAGIC_NUMBERS['MAGIC_DIFF'],
        'xor_krober': timestamp ^ MAGIC_NUMBERS['K_ROBER'],
        'xor_rtdoty': timestamp ^ MAGIC_NUMBERS['R_TDOTY'],
        'add_magic': timestamp + MAGIC_NUMBERS['MAGIC_DIFF'],
        'sub_magic': timestamp - MAGIC_NUMBERS['MAGIC_DIFF']
    }
    return results

def find_matches(all_results):
    """Find matching values across different dates and transformations"""
    value_locations = defaultdict(list)
    
    # Store all values and their locations
    for date_info in all_results:
        date = date_info['date']
        for trans_name, value in date_info['transformations'].items():
            value_locations[value].append((date, trans_name))
    
    # Find matches (values that appear more than once)
    matches = {value: locations for value, locations in value_locations.items() 
              if len(locations) > 1}
    
    return matches

def generate_analysis():
    all_results = []
    
    # Analyze each employment date
    for date_str, name, timestamp in EMPLOYMENT_DATES:
        transformations = apply_magic_modulo(timestamp)
        all_results.append({
            'date': name,
            'timestamp': timestamp,
            'transformations': transformations
        })
    
    # Find matching values
    matches = find_matches(all_results)
    
    # Write analysis to file
    with open('/home/computeruse/red/employment_magic_analysis.md', 'w') as f:
        f.write("# Employment Period Magic Number Analysis\n\n")
        
        # Individual date analysis
        f.write("## Individual Date Analysis\n\n")
        for result in all_results:
            f.write(f"### {result['date']}\n")
            f.write(f"Timestamp: {result['timestamp']}\n")
            f.write(f"Hex: {hex(result['timestamp'])}\n\n")
            
            f.write("Transformations:\n")
            for trans_name, value in result['transformations'].items():
                f.write(f"* {trans_name}: {value} (hex: {hex(value)})\n")
            f.write("\n")
        
        # Matching values analysis
        f.write("## Matching Values Found\n\n")
        for value, locations in matches.items():
            f.write(f"### Value: {value} (hex: {hex(value)})\n")
            f.write("Found in:\n")
            for date, trans_type in locations:
                f.write(f"* {date} ({trans_type})\n")
            f.write("\n")
        
        # Special analysis: look for sequences
        f.write("## Sequential Analysis\n\n")
        timestamps = [ts for _, _, ts in EMPLOYMENT_DATES]
        differences = []
        for i in range(len(timestamps)-1):
            diff = timestamps[i+1] - timestamps[i]
            differences.append(diff)
            f.write(f"Difference {i+1}: {diff} seconds ({diff/86400:.2f} days)\n")
            
            # Check if difference has relationship with magic numbers
            for magic_name, magic_value in MAGIC_NUMBERS.items():
                if diff % magic_value < 1000 or diff % magic_value > magic_value - 1000:
                    f.write(f"* Near multiple of {magic_name}\n")
                if abs(diff - magic_value) < 1000:
                    f.write(f"* Close to {magic_name}\n")
        
        # Look for patterns in the differences
        f.write("\n## Pattern Analysis\n\n")
        
        # Check for arithmetic sequences
        diffs_of_diffs = np.diff(differences)
        if any(abs(diffs_of_diffs[0] - d) < 1000 for d in diffs_of_diffs[1:]):
            f.write("* Possible arithmetic sequence found in time differences\n")
        
        # Check for geometric sequences
        ratios = [differences[i+1]/differences[i] for i in range(len(differences)-1)]
        if any(abs(ratios[0] - r) < 0.01 for r in ratios[1:]):
            f.write("* Possible geometric sequence found in time differences\n")
        
        # Check for modulo patterns
        for magic_name, magic_value in MAGIC_NUMBERS.items():
            mod_sequence = [ts % magic_value for ts in timestamps]
            diffs_mod = np.diff(mod_sequence)
            if any(d == diffs_mod[0] for d in diffs_mod[1:]):
                f.write(f"* Regular pattern found in modulo {magic_name} sequence\n")

# Additional analysis focusing on magic modulo patterns
def analyze_magic_modulo_patterns():
    time_range = range(EMPLOYMENT_DATES[0][2], EMPLOYMENT_DATES[-1][2], 3600)  # hourly steps
    interesting_times = []
    
    for t in time_range:
        mod_result = t % MAGIC_NUMBERS['MODULO_RESULT']
        if mod_result == 0 or mod_result == MAGIC_NUMBERS['MAGIC_DIFF']:
            interesting_times.append((t, mod_result))
    
    with open('/home/computeruse/red/magic_modulo_patterns.md', 'w') as f:
        f.write("# Magic Modulo Pattern Analysis\n\n")
        f.write("Times during employment that produce interesting modulo results:\n\n")
        
        for timestamp, result in interesting_times:
            date = datetime.fromtimestamp(timestamp)
            f.write(f"* {date}: {result}\n")
            
            # Check if this time is near any known events
            for event_date, event_name, event_ts in EMPLOYMENT_DATES:
                if abs(event_ts - timestamp) < 86400:  # within one day
                    f.write(f"  - Close to {event_name}!\n")

# Run both analyses
generate_analysis()
analyze_magic_modulo_patterns()