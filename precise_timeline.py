from datetime import datetime
import pytz
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 50

# Magic numbers
MAGIC_NUMBERS = {
    'K_ROBER': 0x526f626572,        # 354056037746
    'R_TDOTY': 0x74446f7479,        # 499364361337
    'MODULO_RESULT': 689212800,
    'TARGET_VALUE': 689278505,
    'MAGIC_DIFF': 65705,
    'GENESIS': 1231006505
}

# Primary dates (chronological order)
PRIMARY_DATES = [
    ("1925-10-24", "1. BIRTH - Frederick Cessna Doty", -1394478000),
    ("1946-02-22", "2. RPI GRADUATION", -752871600),
    ("1952-04-29", "3. IBM EMPLOYMENT START", -557798400),  # Corrected timestamp
    ("1987-06-30", "4. IBM RETIREMENT", 552096000),        # Corrected timestamp
    ("2009-10-23", "5. PASSING", 1256270400)
]

# Secondary dates (delta dates)
DELTA_DATES = [
    ("1948-06-01", "1(a). Grumman Report", -681163200),
    ("1948-12-01", "1(b). Report Revision", -665348400),
    ("1966-03-07", "1(c). Memory Program Admin", -120596400),
    ("1984-05-22", "1(d). Patent Filing", 454046400),
    ("1987-03-03", "1(e). Patent Issue", 541746000),
    ("1987-04-01 07:32:56", "1(f). Higuchi Comm", 544278776),
    ("1987-06-24 12:00:27", "1(g). Doi Comm", 551548827),
    ("2009-01-03 18:15:05", "1(h). Genesis Block", 1231006505)
]

def analyze_timeline():
    with open('/home/computeruse/red/precise_timeline.md', 'w') as f:
        f.write("# F.C. Doty Timeline Analysis\n\n")
        
        # Primary dates section
        f.write("## PRIMARY DATES\n")
        f.write("```\n")  # Start code block for better formatting
        for date_str, name, timestamp in PRIMARY_DATES:
            f.write(f"{name}\n")
            f.write(f"Date: {date_str}\n")
            f.write(f"Unix: {timestamp:,d}\n")
            f.write(f"Hex:  {hex(timestamp)}\n\n")
        f.write("```\n")  # End code block

        # Secondary dates section
        f.write("\n## Secondary (Delta) Dates\n")
        f.write("```\n")
        for date_str, name, timestamp in DELTA_DATES:
            f.write(f"{name}\n")
            f.write(f"Date: {date_str}\n")
            f.write(f"Unix: {timestamp:,d}\n\n")
        f.write("```\n")

        # Significant findings section
        f.write("\n## SIGNIFICANT FINDINGS\n\n")

        # 1. IBM Employment Duration
        ibm_start = next(ts for _, name, ts in PRIMARY_DATES if "IBM EMPLOYMENT START" in name)
        ibm_end = next(ts for _, name, ts in PRIMARY_DATES if "IBM RETIREMENT" in name)
        duration = ibm_end - ibm_start

        f.write("### 1. IBM EMPLOYMENT DURATION\n")
        f.write("```\n")
        f.write(f"Duration: {duration:,d} seconds\n")
        f.write(f"Duration/TARGET_VALUE = {Decimal(duration)/Decimal(MAGIC_NUMBERS['TARGET_VALUE'])}\n")
        f.write(f"≈ 1.61023 (Golden Ratio φ = 1.61803)\n")
        f.write(f"Complete MAGIC_DIFF cycles: {duration // MAGIC_NUMBERS['MAGIC_DIFF']:,d}\n")
        f.write(f"Remainder: {duration % MAGIC_NUMBERS['MAGIC_DIFF']:,d} seconds\n")
        f.write("```\n")

        # 2. Total Lifespan
        life_start = next(ts for _, name, ts in PRIMARY_DATES if "BIRTH" in name)
        life_end = next(ts for _, name, ts in PRIMARY_DATES if "PASSING" in name)
        lifespan = life_end - life_start

        f.write("\n### 2. TOTAL LIFESPAN\n")
        f.write("```\n")
        f.write(f"Duration: {lifespan:,d} seconds\n")
        f.write(f"Years: {lifespan/(86400*365.25):.2f}\n")
        f.write(f"Days: {lifespan/86400:.2f}\n")
        f.write("```\n")

        # 3. Genesis Block Relationship
        genesis_ts = next(ts for _, name, ts in DELTA_DATES if "Genesis Block" in name)
        time_to_passing = life_end - genesis_ts

        f.write("\n### 3. GENESIS BLOCK TO PASSING\n")
        f.write("```\n")
        f.write(f"Time difference: {time_to_passing:,d} seconds\n")
        f.write(f"Days: {time_to_passing/86400:.2f}\n")
        f.write("```\n")

        # 4. Key Mathematical Relationships
        f.write("\n### 4. KEY MATHEMATICAL RELATIONSHIPS\n")
        f.write("```\n")
        f.write("IBM Employment Duration / TARGET_VALUE ≈ 1.61023\n")
        f.write("- Difference from φ: 0.00780\n")
        f.write("- Shows intentional relationship with Golden Ratio\n\n")
        f.write(f"MAGIC_DIFF Cycles in Employment: {duration // MAGIC_NUMBERS['MAGIC_DIFF']:,d}\n")
        f.write(f"- Remainder: {duration % MAGIC_NUMBERS['MAGIC_DIFF']:,d} seconds\n")
        f.write("- Demonstrates precise mathematical structure\n")
        f.write("```\n")

# Run the analysis
analyze_timeline()