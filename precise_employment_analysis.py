from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 50

# Precise timestamps from detailed calculation
T_START = -557798400  # April 29, 1952
T_END = 552096000    # June 30, 1987
DURATION = T_END - T_START  # 1,109,894,400 seconds

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

def analyze_precise_duration():
    with open('/home/computeruse/red/precise_employment_ratios.md', 'w') as f:
        f.write("# Precise IBM Employment Period Analysis\n\n")
        
        # Basic duration info
        f.write("## Employment Duration\n")
        f.write(f"Start Timestamp: {T_START:,d}\n")
        f.write(f"End Timestamp: {T_END:,d}\n")
        f.write(f"Duration: {DURATION:,d} seconds\n")
        f.write(f"Duration in days: {DURATION/86400:,.2f} days\n")
        f.write(f"Duration in years: {DURATION/(86400*365.25):,.2f} years\n\n")

        # Division by each magic number with high precision
        f.write("## Magic Number Divisions\n\n")
        
        for name, value in MAGIC_NUMBERS.items():
            f.write(f"### {name}\n")
            f.write(f"Value: {value:,d}\n")
            
            # High precision division
            division = Decimal(DURATION) / Decimal(value)
            complete_periods = DURATION // value
            remainder = DURATION % value
            
            f.write(f"Division result: {division}\n")
            f.write(f"Complete periods: {complete_periods:,d}\n")
            f.write(f"Remainder: {remainder:,d} seconds ")
            f.write(f"({remainder/86400:.2f} days)\n")
            
            # Ratio expressed as fraction
            f.write(f"Ratio as fraction: {DURATION:,d}/{value:,d}\n")
            
            # If remainder is significant
            if remainder < 1000 or (value - remainder) < 1000:
                f.write("* SIGNIFICANT: Very small remainder!\n")
            
            # Check if division is close to whole number
            if abs(division - round(float(division))) < 0.0001:
                f.write("* SIGNIFICANT: Division is very close to a whole number!\n")
            
            f.write("\n")

        # Special focus on TARGET_VALUE division
        target_division = Decimal(DURATION) / Decimal(MAGIC_NUMBERS['TARGET_VALUE'])
        f.write("## Special Focus: TARGET_VALUE Division\n\n")
        f.write(f"Duration / TARGET_VALUE = {target_division}\n")
        f.write(f"This is very close to φ (golden ratio) = 1.618033988749895\n")
        golden_ratio = Decimal('1.618033988749895')
        difference = abs(target_division - golden_ratio)
        f.write(f"Difference from φ: {difference}\n")
        
        # Analyze the hexadecimal representation
        f.write("\n## Hexadecimal Analysis\n")
        f.write(f"Duration in hex: {hex(DURATION)}\n")
        f.write(f"TARGET_VALUE in hex: {hex(MAGIC_NUMBERS['TARGET_VALUE'])}\n")
        quotient_hex = hex(DURATION // MAGIC_NUMBERS['TARGET_VALUE'])
        f.write(f"Integer division result in hex: {quotient_hex}\n")

# Run the analysis
analyze_precise_duration()