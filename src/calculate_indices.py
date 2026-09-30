"""
Modulo para calcular los indices Eo, Sv y SM2.
"""

import numpy as np
import pandas as pd

from config.config import PARKINSON_CONST


# ================================================================
# INDICE DE EFICIENCIA OPERATIVA (Eo)
# ================================================================

def calcular_eo(df_fx):
    """
    Eo anual usando el estimador de Parkinson.
    CT_t = sqrt(1/(4*ln(2))) * |ln(H_t/L_t)| * 100
    Eo_y = 100 / (1 + mean(CT))
    """
    df = df_fx.copy()
    df["CT"] = PARKINSON_CONST * np.abs(np.log(df["High"] / df["Low"])) * 100
    df["year"] = df.index.year
    eo = df.groupby("year")["CT"].mean().to_frame()
    eo["Eo"] = 100.0 / (1.0 + eo["CT"])
    return eo["Eo"]


def calcular_eo_todos(fx_data, verbose=True):
    """Calcula Eo para todas las divisas."""
    if verbose:
        print("=" * 70)
        print("CALCULANDO Eo (EFICIENCIA OPERATIVA)")
        print("=" * 70)

    resultados = {}
    for code, df in fx_data.items():
        try:
            resultados[code] = calcular_eo(df)
        except Exception:
            pass

    df_eo = pd.DataFrame(resultados)

    if verbose:
        print(f"  Divisas: {df_eo.shape[1]}")
        print(f"  Rango: {df_eo.mean().min():.2f} a {df_eo.mean().max():.2f}")
        print(f"  Anios: {df_eo.index.min()} - {df_eo.index.max()}\n")

    return df_eo


# ================================================================
# INDICE DE ENTROPIA VALORATIVA (Sv)
# ================================================================

def calcular_sv(df_fx, df_gold):
    """
    Sv anual: volatilidad del valor de la divisa en oro.
    VAU_t = (1/e_t) * P_gold,t
    Sv_y = std(log retornos) * sqrt(252)
    """
    df = df_fx[["Close"]].join(df_gold, how="inner").dropna()
    if df.empty or len(df) < 30:
        return None
    df["VAU"] = (1.0 / df["Close"]) * df["Gold"]
    df["r"] = np.log(df["VAU"] / df["VAU"].shift(1))
    df = df.dropna()
    df["year"] = df.index.year
    return df.groupby("year")["r"].std() * np.sqrt(252)


def calcular_sv_todos(fx_data, gold, verbose=True):
    """Calcula Sv para todas las divisas y winsoriza al P95."""
    if verbose:
        print("=" * 70)
        print("CALCULANDO Sv (ENTROPIA VALORATIVA)")
        print("=" * 70)

    resultados = {}
    for code, df in fx_data.items():
        try:
            sv = calcular_sv(df, gold)
            if sv is not None:
                resultados[code] = sv
        except Exception:
            pass

    df_sv = pd.DataFrame(resultados)

    # Winsorizar al percentil 95
    sv_flat = df_sv.stack()
    p95 = sv_flat.quantile(0.95)
    df_sv = df_sv.clip(upper=p95)

    if verbose:
        print(f"  Divisas: {df_sv.shape[1]}")
        print(f"  Winsorizado al P95: {p95:.4f}\n")

    return df_sv


# ================================================================
# INDICE DE ENTROPIA DE M2 (SM2)
# ================================================================

def calcular_sm2_mensual(df_m2):
    """
    SM2 a partir de datos mensuales.
    SM2_y = std(log retornos) * sqrt(12)
    """
    df = df_m2.copy()
    df["r"] = np.log(df["M2"] / df["M2"].shift(1))
    df = df.dropna()
    df["year"] = df.index.year
    return df.groupby("year")["r"].std() * np.sqrt(12)


def calcular_sm2_anual(serie):
    """
    SM2 a partir de datos anuales.
    Usado para SGP, ARG, IND (Banco Mundial).
    """
    serie = serie.dropna()
    if len(serie) < 5:
        return np.nan
    r = np.log(serie / serie.shift(1)).dropna()
    if len(r) < 3:
        return np.nan
    return r.std()


def calcular_sm2_fred(m2_fred, verbose=True):
    """Calcula SM2 para todas las series de FRED."""
    if verbose:
        print("=" * 70)
        print("CALCULANDO SM2 (FRED, mensual)")
        print("=" * 70)

    resultados = {}
    for code, df in m2_fred.items():
        try:
            sm2 = calcular_sm2_mensual(df)
            if len(sm2) >= 5:
                resultados[code] = sm2
        except Exception:
            pass

    df_sm2 = pd.DataFrame(resultados)

    if verbose:
        print(f"  Paises: {df_sm2.shape[1]}\n")

    return df_sm2


def calcular_sm2_wb(m2_wb, verbose=True):
    """Calcula SM2 anual para los paises del Banco Mundial."""
    if verbose:
        print("=" * 70)
        print("CALCULANDO SM2 (Banco Mundial, anual)")
        print("=" * 70)

    resultados = {}
    for pais in m2_wb.columns:
        sm2 = calcular_sm2_anual(m2_wb[pais])
        if not np.isnan(sm2):
            resultados[pais] = sm2
            if verbose:
                print(f"  {pais}: SM2 = {sm2:.4f}")

    if verbose:
        print()

    return resultados
