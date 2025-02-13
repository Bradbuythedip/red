from datetime import datetime
import pytz
from decimal import Decimal, getcontext

# Set high precision for calculations
getcontext().prec = 50

# Correct employment dates
START_DATE = "1952-04-29"
END_DATE = "1987-06-30"

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

def to_unix_timestamp(date_str, timezone='US/Eastern'):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    tz = pytz.timezone(timezone)
    dt = tz.localize(dt)
    return int(dt.timestamp())

def analyze_full_employment():
    # Get timestamps
    start_ts = to_unix_timestamp(START_DATE)
    end_ts = to_unix_timestamp(END_DATE)
    duration = end_ts - start_ts

    with open('/home/computeruse/red/full_employment_ratios.md', 'w') as f:
        f.write("# Full IBM Employment Period Analysis\n\n")
        
        # Basic duration info
        f.write("## Employment Duration\n")
        f.write(f"Start Date: {START_DATE}\n")
        f.write(f"End Date: {END_DATE}\n")
        f.write(f"Start Timestamp: {start_ts}\n")
        f.write(f"End Timestamp: {end_ts}\n")
        f.write(f"Duration: {duration:,d} seconds\n")
        f.write(f"Duration in days: {duration/86400:,.2f} days\n")
        f.write(f"Duration in years: {duration/(86400*365.25):,.2f} years\n\n")

        # Division by each magic number
        f.write("## Magic Number Divisions\n\n")
        
        for name, value in MAGIC_NUMBERS.items():
            f.write(f"### {name}\n")
            f.write(f"Value: {value:,d}\n")
            
            # High precision division
            division = Decimal(duration) / Decimal(value)
            complete_periods = duration // value
            remainder = duration % value
            
            f.write(f"Division result: {division}\n")
            f.write(f"Complete periods: {complete_periods:,d}\n")
            f.write(f"Remainder: {remainder:,d} seconds ")
            f.write(f"({remainder/86400:.2f} days)\n")
            
            # If remainder is significant
            if remainder < 1000 or (value - remainder) < 1000:
                f.write("* SIGNIFICANT: Very small remainder!\n")
            
            # Check if division is close to whole number
            if abs(division - round(float(division))) < 0.0001:
                f.write("* SIGNIFICANT: Division is very close to a whole number!\n")
            
            f.write("\n")

        # Special focus on MAGIC_DIFF division
        magic_diff_division = Decimal(duration) / Decimal(MAGIC_NUMBERS['MAGIC_DIFF'])
        f.write("## Special Focus: MAGIC_DIFF Division\n\n")
        f.write(f"Duration / MAGIC_DIFF = {magic_diff_division}\n")
        
        # Binary analysis of duration
        binary = bin(duration)[2:]  # Remove '0b' prefix
        ones = binary.count('1')
        zeros = len(binary) - ones
        f.write("\n## Binary Analysis of Duration\n\n")
        f.write(f"Binary: {binary}\n")
        f.write(f"Length: {len(binary)} bits\n")
        f.write(f"Ones: {ones}\n")
        f.write(f"Zeros: {zeros}\n")
        f.write(f"Ratio of ones: {ones/len(binary):.4f}\n")

        # Hexadecimal analysis
        hex_duration = hex(duration)[2:]  # Remove '0x' prefix
        f.write("\n## Hexadecimal Analysis\n\n")
        f.write(f"Hex: {hex_duration}\n")
        f.write(f"Length: {len(hex_duration)} digits\n")

# Run the analysis
analyze_full_employment()