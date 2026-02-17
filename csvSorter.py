import pandas as pd
import re

PREFIX_TO_COUNTRY = {
        # Single-letter prefixes
        "B": "China",
        "C": "Canada",
        "D": "Germany",
        "F": "France",
        "G": "United Kingdom",
        "I": "Italy",
        "M": "Isle of Man",
        "N": "United States",
        "P": "North Korea",
        "Z": "Zimbabwe",

        # Two-letter prefixes
        "AP": "Pakistan",
        "CC": "Chile",
        "CN": "Morocco",
        "CP": "Bolivia",
        "CR": "Portugal",
        "CS": "Portugal",
        "CU": "Cuba",
        "CX": "Uruguay",
        "EC": "Spain",
        "EI": "Ireland",
        "EJ": "Ireland",
        "EK": "Armenia",
        "EM": "Spain",
        "EP": "Iran",
        "ER": "Moldova",
        "ES": "Estonia",
        "ET": "Ethiopia",
        "EW": "Belarus",
        "EX": "Kyrgyzstan",
        "EY": "Tajikistan",
        "EZ": "Turkmenistan",
        "HA": "Hungary",
        "HB": "Switzerland",
        "HC": "Ecuador",
        "HI": "Dominican Republic",
        "HJ": "Colombia",
        "HK": "Colombia",
        "HL": "South Korea",
        "HP": "Panama",
        "HR": "Honduras",
        "HS": "Thailand",
        "HZ": "Saudi Arabia",
        "JA": "Japan",
        "JR": "Japan",
        "JU": "Mongolia",
        "JY": "Jordan",
        "LN": "Norway",
        "LQ": "Argentina",
        "LV": "Argentina",
        "LX": "Luxembourg",
        "LY": "Lithuania",
        "LZ": "Bulgaria",
        "OB": "Peru",
        "OD": "Lebanon",
        "OE": "Austria",
        "OK": "Czech Republic",
        "OM": "Slovakia",
        "OO": "Belgium",
        "OY": "Denmark",
        "PH": "Netherlands",
        "PJ": "Netherlands Antilles",
        "PK": "Indonesia",
        "PP": "Brazil",
        "PR": "Brazil",
        "PS": "Brazil",
        "PT": "Brazil",
        "PU": "Brazil",
        "PZ": "Suriname",
        "RA": "Russia",
        "RF": "Russia",
        "RP": "Philippines",
        "SE": "Sweden",
        "SN": "Poland",
        "SP": "Poland",
        "ST": "Sudan",
        "SU": "Egypt",
        "SX": "Greece",
        "TF": "Iceland",
        "TG": "Guatemala",
        "TI": "Costa Rica",
        "TJ": "Cameroon",
        "TN": "Congo, Republic of",
        "TR": "Gabon",
        "TS": "Tunisia",
        "TU": "Ivory Coast",
        "TY": "Benin",
        "TZ": "Mali",
        "UK": "Uzbekistan",
        "UP": "Kazakhstan",
        "UR": "Ukraine",
        "VH": "Australia",
        "VN": "Vietnam",
        "VT": "India",
        "XA": "Mexico",
        "XB": "Mexico",
        "XC": "Mexico",
        "XT": "Burkina Faso",
        "XU": "Cambodia",
        "XY": "Myanmar",
        "YA": "Afghanistan",
        "YI": "Iraq",
        "YJ": "Vanuatu",
        "YK": "Syria",
        "YL": "Latvia",
        "YN": "Nicaragua",
        "YR": "Romania",
        "YS": "El Salvador",
        "YU": "Serbia",
        "YV": "Venezuela",
        "ZA": "Albania",
        "ZK": "New Zealand",
        "ZL": "New Zealand",
        "ZM": "New Zealand",
        "ZP": "Paraguay",
        "ZS": "South Africa",
        "ZT": "South Africa",
        "ZU": "South Africa"
    }

df = pd.read_csv('ddb.csv', quotechar="'")

## Replace empty values with "" to prevent NaN errors
df = df.fillna("")

##Remove rows with no comp number
def remove_no_comp_num(df):
    df = df[df["CN"] != ""]
    return df

##Add hyphens to registrations
def hyphenate(df):

    _US_N_RE = re.compile(r"^N\d{1,5}[A-Z]{0,2}$")

    ## Prefixes that use a hyphen
    ##Single letter prefixes
    _PREFIXES_1 = {
        "B", "C", "D", "F", "G", "I", "M", "N", "P", "Z"
    }

    ##Two letter prefixes
    _PREFIXES_2 = {
        "YA", "ZA", "LV", "LQ", "EK", "VH", "OE", "EW", "OO", "TY",
        "CP", "PP", "PT", "PR", "PU", "PS", "LZ", "XT", "XU", "TJ",
        "CC", "HJ", "TN", "TI", "CU", "OK", "OY", "HI", "HC", "SU",
        "YS", "ES", "ET", "TR", "SX", "TG", "HH", "HR", "HA", "TF",
        "VT", "PK", "EP", "YI", "EI", "EJ", "TU", "JA", "JR", "JY",
        "UP", "EX", "YL", "OD", "HB", "LY", "LX", "TZ", "XA", "XB",
        "XC", "ER", "JU", "CN", "XY", "PH", "PJ", "ZK", "ZL", "ZM",
        "YN", "LN", "AP", "HP", "ZP", "OB", "RP", "SP", "SN", "CR",
        "CS", "YR", "RA", "RF", "HZ", "YU", "OM", "ZS", "ZT", "ZU",
        "HL", "EC", "EM", "ST", "PZ", "SE", "YK", "EY", "HS", "TS",
        "TC", "EZ", "UR", "CX", "UK", "YJ", "YV", "VN"
    }

    ##Add a hyphen to non-hyphenated registrations
    def hyphenate_reg(reg: str) -> str:
        if reg is None:
            return ""

        s = reg.strip().upper().replace(" ", "")
        if not s:
            return s

        ## Already hyphenated
        if "-" in s:
            return s

        ## US N-numbers aren't hypenated
        if _US_N_RE.fullmatch(s):
            return s

        ## 2-letter prefixes (e.g. VHJKB -> VH-JKB, PH1308 -> PH-1308)
        if len(s) >= 5 and s[:2].isalpha() and s[:2] in _PREFIXES_2:
            return s[:2] + "-" + s[2:]

        ## 1-letter prefixes (e.g. GCHNM -> G-CHNM, D3832 -> D-3832)
        if len(s) >= 4 and s[0].isalpha() and s[0] in _PREFIXES_1:
            return s[0] + "-" + s[1:]

        return s

    df["REGISTRATION"] = df["REGISTRATION"].apply(hyphenate_reg)
    return df

##Remove unregistered aircraft (e.g. hang-gliders and paragliders)
def remove_unregistered(df):
    def is_registered(reg: str) -> bool:
        _BAD_TOKENS = {
            "", "-", "—", "-----", "NONE", "N/A", "NA", "N.A.", "NULL", "UNREGISTERED", "TEST", "UNKNOWN"
        }

        ## Regexes to match most registrations
        _REG_RE = re.compile(
            r"^(?:"
            r"N\d{1,5}[A-Z]{0,2}"  # US N-number (approx)
            r"|[A-Z]{1,3}-[A-Z0-9]{3,5}"  # hyphenated: G-XXXX, D-KGOR, C-GOED, ZT-GOU, etc.
            r")$"
        )

        if reg is None:
            return False

        s = reg.strip().upper().replace(" ", "")
        if s in _BAD_TOKENS:
            return False

        ## If it contains placeholder characters, treat as unregistered/invalid
        if any(ch in s for ch in ("?", "*")):
            return False

        ## Exclude pure numeric IDs
        if s.isdigit():
            return False

        return bool(_REG_RE.fullmatch(s))

    df = df[df["REGISTRATION"].apply(is_registered)]
    return df

def sort_by_cn(df):
    return df.sort_values(by=["CN"])

def get_country_from_reg(reg):
    if not reg or not isinstance(reg, str):
        return "Unknown"
    # Check for 2-letter prefix first
    if len(reg) >= 2 and reg[:2].upper() in PREFIX_TO_COUNTRY:
        return PREFIX_TO_COUNTRY[reg[:2].upper()]
    # Check for 1-letter prefix
    if len(reg) >= 1 and reg[0].upper() in PREFIX_TO_COUNTRY:
        return PREFIX_TO_COUNTRY[reg[0].upper()]
    return "Unknown"

# Processing Pipeline
df = remove_no_comp_num(df)
df = hyphenate(df)
# Populate the new COUNTRY column
df["COUNTRY"] = df["REGISTRATION"].apply(get_country_from_reg)

# Sort and Save
df = df.sort_values(by=["CN"])
df.to_csv('ddb_sorted.csv', index=False)
