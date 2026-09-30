"""
Configuracion centralizada del proyecto: parametros, diccionarios y constantes.
"""

import os
import numpy as np

# DIRECTORIOS
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
TABLES_DIR = os.path.join(RESULTS_DIR, "tables")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, TABLES_DIR, FIGURES_DIR]:
    os.makedirs(d, exist_ok=True)

# PARAMETROS
START_DATE = "2010-01-01"
END_DATE = "2025-12-31"
START_YEAR = 2010
END_YEAR = 2025

PARKINSON_CONST = np.sqrt(1.0 / (4.0 * np.log(2.0)))
UMBRAL_D = 0.10

# DIVISAS: codigo -> (ticker_yahoo, invertir)
CURRENCIES = {
    "EUR": ("EURUSD=X", True),
    "GBP": ("GBPUSD=X", True),
    "JPY": ("JPY=X",    False),
    "CHF": ("CHF=X",    False),
    "CAD": ("CAD=X",    False),
    "AUD": ("AUDUSD=X", True),
    "NZD": ("NZDUSD=X", True),
    "CNY": ("CNY=X",    False),
    "HKD": ("HKD=X",    False),
    "SGD": ("SGD=X",    False),
    "KRW": ("KRW=X",    False),
    "INR": ("INR=X",    False),
    "NOK": ("NOK=X",    False),
    "SEK": ("SEK=X",    False),
    "DKK": ("DKK=X",    False),
    "PLN": ("PLN=X",    False),
    "CZK": ("CZK=X",    False),
    "HUF": ("HUF=X",    False),
    "RON": ("RON=X",    False),
    "TRY": ("TRY=X",    False),
    "RUB": ("RUB=X",    False),
    "ISK": ("ISK=X",    False),
    "BRL": ("BRL=X",    False),
    "MXN": ("MXN=X",    False),
    "ARS": ("ARS=X",    False),
    "CLP": ("CLP=X",    False),
    "COP": ("COP=X",    False),
    "PEN": ("PEN=X",    False),
    "UYU": ("UYU=X",    False),
    "IDR": ("IDR=X",    False),
    "MYR": ("MYR=X",    False),
    "PHP": ("PHP=X",    False),
    "THB": ("THB=X",    False),
    "TWD": ("TWD=X",    False),
    "PKR": ("PKR=X",    False),
    "BDT": ("BDT=X",    False),
    "LKR": ("LKR=X",    False),
    "KZT": ("KZT=X",    False),
    "ZAR": ("ZAR=X",    False),
    "EGP": ("EGP=X",    False),
    "NGN": ("NGN=X",    False),
    "KES": ("KES=X",    False),
    "MAD": ("MAD=X",    False),
    "ILS": ("ILS=X",    False),
    "SAR": ("SAR=X",    False),
    "AED": ("AED=X",    False),
}
USD_TICKER = "DX-Y.NYB"

# SERIES FRED PARA M2
M2_FRED_SERIES = {
    "USA": "M2SL",
    "JPN": "MYAGM2JPM189N",
    "CHN": "MYAGM2CNM189N",
    "KOR": "MYAGM2KRM189N",
    "BRA": "MYAGM2BRM189N",
    "MEX": "MYAGM2MXM189N",
    "ZAF": "MYAGM2ZAM189N",
    "TUR": "MYAGM2TRM189N",
    "GBR": "MABMM301GBM189S",
    "CAN": "MABMM301CAM189S",
    "AUS": "MABMM301AUM189S",
    "CHE": "MABMM301CHM189S",
    "SWE": "MABMM301SEM189S",
    "NOR": "MABMM301NOM189S",
    "DNK": "MABMM301DKM189S",
    "POL": "MABMM301PLM189S",
    "CZE": "MABMM301CZM189S",
    "HUN": "MABMM301HUM189S",
    "CHL": "MABMM301CLM189S",
    "EUZ": "MABMM301EZM189S",
}

# M2 DEL BANCO MUNDIAL
M2_WORLD_BANK = {
    "SGP": "SGD",
    "ARG": "ARS",
    "IND": "INR",
}

# MAPEO DIVISA <-> PAIS
DIVISA_A_PAIS = {
    "EUR": "EUZ", "GBP": "GBR", "JPY": "JPN", "CHF": "CHE",
    "CAD": "CAN", "AUD": "AUS", "NZD": "NZL", "CNY": "CHN",
    "HKD": "HKG", "SGD": "SGP", "KRW": "KOR", "INR": "IND",
    "NOK": "NOR", "SEK": "SWE", "DKK": "DNK", "PLN": "POL",
    "CZK": "CZE", "HUF": "HUN", "RON": "ROU", "TRY": "TUR",
    "RUB": "RUS", "ISK": "ISL", "BRL": "BRA", "MXN": "MEX",
    "ARS": "ARG", "CLP": "CHL", "COP": "COL", "PEN": "PER",
    "UYU": "URY", "IDR": "IDN", "MYR": "MYS", "PHP": "PHL",
    "THB": "THA", "TWD": "TWN", "PKR": "PAK", "BDT": "BGD",
    "LKR": "LKA", "KZT": "KAZ", "ZAR": "ZAF", "EGP": "EGY",
    "NGN": "NGA", "KES": "KEN", "MAD": "MAR", "ILS": "ISR",
    "SAR": "SAU", "AED": "ARE", "USD": "USA",
}
PAIS_A_DIVISA = {v: k for k, v in DIVISA_A_PAIS.items()}

# POSICIONAMIENTO GLOBAL
# Reservas: IMF COFER Q4 2024 (%)
# Turnover: BIS Triennial Survey 2022 (%)
POSICIONAMIENTO = {
    "USD": (57.80, 88.50), "EUR": (19.80, 30.50), "JPY": ( 5.50, 16.70),
    "GBP": ( 4.70, 12.90), "CNY": ( 2.30,  7.00), "CAD": ( 2.80,  6.20),
    "AUD": ( 2.20,  6.40), "CHF": ( 0.20,  5.20), "HKD": ( 0.00,  2.40),
    "SGD": ( 0.40,  1.70), "KRW": ( 0.50,  1.80), "SEK": ( 0.40,  2.10),
    "NOK": ( 0.10,  1.70), "DKK": ( 0.10,  0.70), "MXN": ( 0.30,  2.50),
    "INR": ( 0.00,  0.60), "BRL": ( 0.10,  0.90), "ZAR": ( 0.10,  0.70),
    "TRY": ( 0.00,  0.50), "PLN": ( 0.10,  0.50), "CZK": ( 0.00,  0.30),
    "HUF": ( 0.00,  0.30), "ILS": ( 0.00,  0.30), "CLP": ( 0.00,  0.20),
    "ARS": ( 0.00,  0.10),
}
