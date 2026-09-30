"""
Modulo de analisis estadistico: correlaciones, regresiones y umbral.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr, mannwhitneyu, linregress

from config.config import POSICIONAMIENTO


def anadir_posicionamiento(df):
    """Anade columnas de reservas COFER y turnover BIS."""
    df = df.copy()
    df["Reservas_COFER"] = df.index.map(
        lambda x: POSICIONAMIENTO.get(x, (np.nan, np.nan))[0]
    )
    df["BIS_Turnover"] = df.index.map(
        lambda x: POSICIONAMIENTO.get(x, (np.nan, np.nan))[1]
    )
    return df


def analizar_correlaciones(df, verbose=True):
    """Correlaciones de Spearman y Pearson."""
    if verbose:
        print("=" * 70)
        print("CORRELACIONES: D vs POSICIONAMIENTO")
        print("=" * 70)

    resultados = []
    for pos_var in ["Reservas_COFER", "BIS_Turnover"]:
        datos = df.dropna(subset=["D", pos_var])
        x = datos["D"].values
        y = datos[pos_var].values

        rho_s, p_s = spearmanr(x, y)
        r_p, p_p = pearsonr(x, y)

        resultados.append({
            "Variable": pos_var,
            "N": len(datos),
            "Spearman_rho": rho_s,
            "Spearman_p": p_s,
            "Pearson_r": r_p,
            "Pearson_p": p_p,
        })

        if verbose:
            print(f"\n  {pos_var} (N={len(datos)}):")
            print(f"    Spearman: rho = {rho_s:.4f}, p = {p_s:.4f}")
            print(f"    Pearson:  r  = {r_p:.4f}, p = {p_p:.4f}")

    return pd.DataFrame(resultados)


def analizar_regresion(df, verbose=True):
    """Regresion log(posicionamiento) ~ D."""
    if verbose:
        print("\n" + "=" * 70)
        print("REGRESION: log(posicionamiento) ~ D")
        print("=" * 70)

    resultados = []
    for pos_var in ["Reservas_COFER", "BIS_Turnover"]:
        datos = df[df[pos_var] > 0].dropna(subset=["D", pos_var]).copy()
        datos["log_pos"] = np.log(datos[pos_var])

        x = datos["D"].values
        y = datos["log_pos"].values
        slope, intercept, r_val, p_val, std_err = linregress(x, y)

        resultados.append({
            "Variable": pos_var,
            "N": len(datos),
            "Pendiente": slope,
            "Error_est": std_err,
            "R2": r_val ** 2,
            "p_valor": p_val,
        })

        if verbose:
            print(f"\n  log({pos_var}) (N={len(datos)}):")
            print(f"    Pendiente: {slope:.4f} (EE: {std_err:.4f})")
            print(f"    R2: {r_val**2:.4f}")
            print(f"    p-valor: {p_val:.4f}")

    return pd.DataFrame(resultados)


def analizar_umbral(df, verbose=True):
    """Analisis de umbral: divisas con D < umbral vs D >= umbral."""
    if verbose:
        print("\n" + "=" * 70)
        print("ANALISIS DE UMBRAL")
        print("=" * 70)

    df_pos = df.dropna(subset=["D", "Reservas_COFER"])
    resultados = []

    if verbose:
        print(f"\n  {'Umbral':>8}  {'N_cerca':>8}  {'Res_cerca':>10}  "
              f"{'Res_lejos':>10}  {'p-valor':>10}")

    for umbral in np.arange(0.07, 0.16, 0.005):
        cerca = df_pos[df_pos["D"] < umbral]
        lejos = df_pos[df_pos["D"] >= umbral]

        if len(cerca) >= 3 and len(lejos) >= 3:
            r_c = cerca["Reservas_COFER"].sum()
            r_l = lejos["Reservas_COFER"].sum()

            try:
                stat, p = mannwhitneyu(
                    cerca["Reservas_COFER"],
                    lejos["Reservas_COFER"],
                    alternative="greater"
                )
            except Exception:
                stat, p = np.nan, np.nan

            resultados.append({
                "Umbral": umbral,
                "N_cerca": len(cerca),
                "Reservas_cerca": r_c,
                "Reservas_lejos": r_l,
                "MannWhitney_U": stat,
                "MannWhitney_p": p,
            })

            if verbose:
                print(f"  {umbral:>8.3f}  {len(cerca):>8}  {r_c:>10.2f}  "
                      f"{r_l:>10.2f}  {p:>10.4f}")

    return pd.DataFrame(resultados)
