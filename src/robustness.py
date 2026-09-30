"""
Modulo de analisis de robustez: sin outliers, sin Turquia, sin Argentina.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, linregress


def analizar_sin_pais(df, pais, verbose=True):
    """
    Analiza el modelo excluyendo un pais especifico.
    """
    if verbose:
        print(f"\n  --- Sin {pais} ---")

    df_sin = df[df.index != pais].copy()

    resultados = {}

    for pos_var in ["Reservas_COFER", "BIS_Turnover"]:
        datos = df_sin.dropna(subset=["D", pos_var])
        if len(datos) < 3:
            continue
        x = datos["D"].values
        y = datos[pos_var].values
        rho, p = spearmanr(x, y)
        resultados[f"Spearman_{pos_var}"] = (rho, p)

        if verbose:
            print(f"    {pos_var}: rho={rho:.4f}, p={p:.4f}")

    return resultados


def analizar_robustez(df, verbose=True):
    """
    Analisis de robustez completo: muestra completa, sin TRY, sin ARS.
    """
    if verbose:
        print("=" * 70)
        print("ANALISIS DE ROBUSTEZ")
        print("=" * 70)

    resultados = []

    for excluir in [None, "TRY", "ARS"]:
        if excluir:
            df_sub = df[df.index != excluir]
            nombre = f"Sin {excluir}"
        else:
            df_sub = df
            nombre = "Muestra completa"

        for pos_var in ["Reservas_COFER", "BIS_Turnover"]:
            datos = df_sub.dropna(subset=["D", pos_var])
            if len(datos) < 3:
                continue
            rho, p = spearmanr(datos["D"], datos[pos_var])
            resultados.append({
                "Muestra": nombre,
                "Variable": pos_var,
                "N": len(datos),
                "Spearman_rho": rho,
                "Spearman_p": p,
            })

    df_rob = pd.DataFrame(resultados)

    if verbose:
        print()
        print(df_rob.round(4).to_string(index=False))

    return df_rob


def analizar_d2(df, verbose=True):
    """
    Analisis complementario D2 = (100-Eo)*Sv (sin M2).
    """
    if verbose:
        print("\n" + "=" * 70)
        print("ANALISIS COMPLEMENTARIO D2 (sin SM2)")
        print("=" * 70)

    df = df.copy()
    df["D2"] = (100 - df["Eo"]) * df["Sv"]

    resultados = []
    for pos_var in ["Reservas_COFER", "BIS_Turnover"]:
        datos = df.dropna(subset=["D2", pos_var])
        if len(datos) < 3:
            continue
        rho, p = spearmanr(datos["D2"], datos[pos_var])

        resultados.append({
            "Variable": pos_var,
            "N": len(datos),
            "Spearman_rho": rho,
            "Spearman_p": p,
        })

        if verbose:
            print(f"  {pos_var} (N={len(datos)}): rho = {rho:.4f}, p = {p:.4f}")

    return pd.DataFrame(resultados)
