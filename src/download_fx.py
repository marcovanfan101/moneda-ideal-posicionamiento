"""
Modulo para descargar tipos de cambio desde Yahoo Finance.
"""

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd

from config.config import START_DATE, END_DATE, CURRENCIES, USD_TICKER, RAW_DATA_DIR


def descargar_fx(ticker):
    """
    Descarga datos OHLC diarios de Yahoo Finance.
    """
    try:
        df = yf.download(ticker, start=START_DATE, end=END_DATE,
                         progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if "High" not in df.columns or "Low" not in df.columns:
            return None
        return df[["High", "Low", "Close"]].dropna()
    except Exception:
        return None


def descargar_todas(verbose=True):
    """
    Descarga tipos de cambio para todas las divisas configuradas.
    Devuelve un diccionario: {codigo_divisa: DataFrame}
    """
    if verbose:
        print("=" * 70)
        print("DESCARGANDO TIPOS DE CAMBIO")
        print("=" * 70)

    fx_data = {}

    for code, (ticker, invertir) in CURRENCIES.items():
        if verbose:
            print(f"  {code:4s} {ticker:12s}...", end=" ")

        df = descargar_fx(ticker)

        if df is None or df.empty:
            if verbose:
                print("SIN DATOS")
            continue

        if invertir:
            old_high = df["High"].copy()
            old_low = df["Low"].copy()
            old_close = df["Close"].copy()
            df["Close"] = 1.0 / old_close
            df["High"] = 1.0 / old_low
            df["Low"] = 1.0 / old_high

        mask = df["High"] >= df["Low"]
        if not mask.all():
            df = df[mask]

        fx_data[code] = df
        if verbose:
            print(f"OK ({len(df)} obs.)")

    # USD con DXY
    if verbose:
        print(f"  USD  {USD_TICKER:12s}...", end=" ")
    dxy = descargar_fx(USD_TICKER)
    if dxy is not None and not dxy.empty:
        fx_data["USD"] = dxy
        if verbose:
            print(f"OK ({len(dxy)} obs.)")
    else:
        if verbose:
            print("SIN DATOS")

    if verbose:
        print(f"\n  Total: {len(fx_data)} divisas\n")

    return fx_data
