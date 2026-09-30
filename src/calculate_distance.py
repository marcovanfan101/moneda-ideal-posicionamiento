"""
Modulo para construir la metrica de distancia a la Moneda Ideal.
D = (100 - Eo) * Sv * SM2
"""

import numpy as np
import pandas as pd

from config.config import PAIS_A_DIVISA, M2_WORLD_BANK


def construir_distancia(df_eo, df_sv, df_sm2_fred, sm2_wb, verbose=True):
    """
    Construye el DataFrame resumen con Eo, Sv, SM2 y D.

    Parametros:
        df_eo       : DataFrame con Eo por anio y divisa
        df_sv       : DataFrame con Sv por anio y divisa
        df_sm2_fred : DataFrame con SM2 por anio y pais (FRED)
        sm2_wb      : dict {pais: SM2} del Banco Mundial

    Devuelve:
        DataFrame ordenado por D con columnas Eo, Sv, SM2, D
    """
    if verbose:
        print("=" * 70)
        print("CONSTRUYENDO METRICA DE DISTANCIA D")
        print("=" * 70)

    # Promedios
    peo = df_eo.mean().to_frame("Eo")
    psv = df_sv.mean().to_frame("Sv")
    psm2 = df_sm2_fred.mean().to_frame("SM2")

    # Combinar
    df = peo.join(psv, how="outer").join(psm2, how="outer")

    # Mapear SM2 de FRED (codigo pais -> codigo divisa)
    sm2_map = {}
    for pais, valor in df_sm2_fred.mean().items():
        div = PAIS_A_DIVISA.get(pais, pais)
        sm2_map[div] = valor

    # Aniadir SM2 del Banco Mundial
    for pais, div in M2_WORLD_BANK.items():
        if pais in sm2_wb:
            sm2_map[div] = sm2_wb[pais]

    # Asignar SM2
    df["SM2"] = df.index.map(lambda x: sm2_map.get(x, np.nan))

    # Calcular D = (100 - Eo) * Sv * SM2
    df["D"] = (100 - df["Eo"]) * df["Sv"] * df["SM2"]

    # Ordenar por D (menor = mas cercano al ideal)
    df = df.sort_values("D")

    completos = df.dropna(subset=["D"])

    if verbose:
        print(f"  Divisas con los 3 indices: {len(completos)}")
        print(f"  Divisas con D < 0.10: {len(completos[completos['D'] < 0.10])}\n")

    return df
