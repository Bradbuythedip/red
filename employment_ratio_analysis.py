from decimal import Decimal, getcontext
import numpy as np

# Set precision for decimal calculations
getcontext().prec = 50

# Employment duration
EMPLOYMENT_START = -120596400  # IBM Promotion (1966-03-07)
EMPLOYMENT_END = 552024000    # IBM Retirement (1987-06-30)
EMPLOYMENT_DURATION = EMPLOYMENT_END - EMPLOYMENT_START  # 672,620,400

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

def analyze_ratios():
    with open('/home/computeruse/red/employment_ratios.md', 'w') as f:
        f.write("# Employment Duration / Magic Number Ratio Analysis\n\n")
        
        # Basic information
        f.write(f"## Employment Duration\n")
        f.write(f"Total duration: {EMPLOYMENT_DURATION:,d} seconds\n")
        f.write(f"In days: {EMPLOYMENT_DURATION/86400:,.2f} days\n")
        f.write(f"In years: {EMPLOYMENT_DURATION/(86400*365.25):,.2f} years\n\n")
        
        f.write("## Ratio Analysis (Duration / Magic Number)\n\n")
        
        ratios = {}
        for name, value in MAGIC_NUMBERS.items():
            # Calculate ratio with high precision
            ratio_decimal = Decimal(EMPLOYMENT_DURATION) / Decimal(value)
            ratio_float = float(ratio_decimal)
            ratios[name] = ratio_float
            
            f.write(f"### {name}\n")
            f.write(f"Magic number: {value:,d}\n")
            f.write(f"Ratio (50 decimal places): {ratio_decimal}\n")
            
            # Check if ratio is close to any interesting numbers
            interesting_numbers = [0.5, 1.0, 1.5, 2.0, np.pi, np.e, 1.618033988749895]  # Golden ratio
            for number in interesting_numbers:
                if abs(ratio_float - number) < 0.01:
                    f.write(f"* Close to {number}!\n")
            
            # Check if inverse ratio is interesting
            inverse = 1 / ratio_float
            f.write(f"Inverse ratio: {inverse:.12f}\n")
            
            # Binary representation analysis
            binary = bin(EMPLOYMENT_DURATION)[2:]  # Remove '0b' prefix
            binary_ratio = binary.count('1') / len(binary)
            f.write(f"Binary density: {binary_ratio:.4f}\n\n")
        
        # Cross-ratio analysis
        f.write("## Cross-Ratio Analysis\n\n")
        for name1, ratio1 in ratios.items():
            for name2, ratio2 in ratios.items():
                if name1 < name2:  # Avoid duplicates
                    cross_ratio = ratio1 / ratio2
                    f.write(f"{name1}/{name2} ratio: {cross_ratio:.12f}\n")
                    
                    # Check if cross-ratio is close to any interesting numbers
                    if abs(cross_ratio - 1) < 0.01:
                        f.write(f"* {name1} and {name2} ratios are very close!\n")
                    elif abs(cross_ratio - 2) < 0.01:
                        f.write(f"* {name1} ratio is approximately double {name2} ratio\n")
                    elif abs(cross_ratio - 0.5) < 0.01:
                        f.write(f"* {name1} ratio is approximately half {name2} ratio\n")
        
        # Additional analysis for significant patterns
        f.write("\n## Pattern Analysis\n\n")
        
        # Convert ratios to array for numerical analysis
        ratio_values = np.array(list(ratios.values()))
        
        # Check for arithmetic sequences
        diffs = np.diff(sorted(ratio_values))
        if np.allclose(diffs, diffs[0], rtol=0.01):
            f.write("* Ratios form an arithmetic sequence!\n")
        
        # Check for geometric sequences
        ratios_nonzero = ratio_values[ratio_values != 0]
        if len(ratios_nonzero) > 1:
            geometric_ratio = ratios_nonzero[1:] / ratios_nonzero[:-1]
            if np.allclose(geometric_ratio, geometric_ratio[0], rtol=0.01):
                f.write("* Ratios form a geometric sequence!\n")
        
        # Look for common factors in denominators
        denominators = []
        for ratio in ratio_values:
            decimal_str = str(Decimal(ratio))
            if '.' in decimal_str:
                decimal_part = decimal_str.split('.')[1]
                denominators.append(len(decimal_part))
        
        if len(set(denominators)) == 1:
            f.write(f"* All ratios have the same number of decimal places: {denominators[0]}\n")

# Run the analysis
analyze_ratios()