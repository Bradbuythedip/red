from datetime import datetime
import numpy as np

# Employment period boundaries
EMPLOYMENT_START = -120596400  # IBM Promotion (1966-03-07)
EMPLOYMENT_END = 552024000    # IBM Retirement (1987-06-30)
EMPLOYMENT_RANGE = EMPLOYMENT_END - EMPLOYMENT_START

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

def analyze_divisions():
    with open('/home/computeruse/red/employment_divisions.md', 'w') as f:
        f.write("# Employment Range Division Analysis\n\n")
        
        # Basic information
        f.write(f"## Employment Period\n")
        f.write(f"Start: {EMPLOYMENT_START} ({datetime.fromtimestamp(EMPLOYMENT_START)})\n")
        f.write(f"End: {EMPLOYMENT_END} ({datetime.fromtimestamp(EMPLOYMENT_END)})\n")
        f.write(f"Range: {EMPLOYMENT_RANGE:,d} seconds\n")
        f.write(f"Range (days): {EMPLOYMENT_RANGE/86400:,.2f} days\n")
        f.write(f"Range (years): {EMPLOYMENT_RANGE/(86400*365.25):,.2f} years\n\n")
        
        f.write("## Divisions by Magic Numbers\n\n")
        
        for name, value in MAGIC_NUMBERS.items():
            division = EMPLOYMENT_RANGE / value
            remainder = EMPLOYMENT_RANGE % value
            exact_periods = EMPLOYMENT_RANGE // value
            
            f.write(f"### Division by {name}\n")
            f.write(f"Value: {value:,d}\n")
            f.write(f"Result: {division:.12f}\n")
            f.write(f"Complete periods: {exact_periods:,d}\n")
            f.write(f"Remainder: {remainder:,d} seconds ({remainder/86400:.2f} days)\n")
            
            # Check if remainder is close to any known values
            for other_name, other_value in MAGIC_NUMBERS.items():
                if other_name != name:
                    if abs(remainder - other_value) < 1000:
                        f.write(f"* Remainder is close to {other_name}!\n")
                    if abs(remainder % other_value) < 1000:
                        f.write(f"* Remainder is divisible by {other_name}!\n")
            
            f.write("\n")
        
        # Additional analysis of the divisions
        f.write("## Additional Analysis\n\n")
        
        # Check if any quotients are close to integer values
        for name, value in MAGIC_NUMBERS.items():
            division = EMPLOYMENT_RANGE / value
            nearest_int = round(division)
            if abs(division - nearest_int) < 0.01:
                f.write(f"* Division by {name} is very close to {nearest_int}!\n")
        
        # Check for relationships between quotients
        quotients = {name: EMPLOYMENT_RANGE / value for name, value in MAGIC_NUMBERS.items()}
        f.write("\n### Relationships between quotients:\n")
        for name1, quot1 in quotients.items():
            for name2, quot2 in quotients.items():
                if name1 < name2:  # Avoid duplicate comparisons
                    ratio = quot1 / quot2
                    if abs(ratio - round(ratio, 2)) < 0.001:
                        f.write(f"* {name1}/{name2} ≈ {ratio:.3f}\n")

        # Look for patterns in binary representation
        f.write("\n### Binary Analysis\n")
        for name, value in MAGIC_NUMBERS.items():
            division_bin = bin(EMPLOYMENT_RANGE // value)[2:]  # Remove '0b' prefix
            f.write(f"\n{name} division binary pattern: {division_bin}\n")
            ones_count = division_bin.count('1')
            zeros_count = len(division_bin) - ones_count
            f.write(f"* Ones: {ones_count}, Zeros: {zeros_count}\n")
            if ones_count == zeros_count:
                f.write("* Equal number of ones and zeros!\n")

# Run the analysis
analyze_divisions()