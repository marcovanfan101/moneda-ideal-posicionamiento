"""
Orquestador del pipeline completo.
"""

import os
import time
import pandas as pd

from config.config import TABLES_DIR, PROCESSED_DATA_DIR
from src.download_fx import descargar_todas
from src.download_m2 import descargar_m2_fred, descargar_m2_world_bank
from src.calculate_indices import (
    calcular_eo_todos, calcular_sv_todos,
    calcular_sm2_fred, calcular_sm2_wb,
)
from src.calculate_distance import construir_distancia
from src.analysis import (
    anadir_posicionamiento, analizar_correlaciones,
    analizar_regresion, analizar_umbral,
)
from src.robustness import analizar_robustez, analizar_d2


def descargar_oro():
    """Descarga el precio del oro desde Yahoo Finance."""
    import yfinance as yf
    from config.config import START_DATE, END_DATE

    print("=" * 70)
    print("DESCARGANDO ORO")
    print("=" * 70)

    gold = yf.download("GC=F", start=START_DATE, end=END_DATE,
                       progress=False, auto_adjust=False)
    if isinstance(gold.columns, pd.MultiIndex):
        gold.columns = gold.columns.get_level_values(0)
    gold = gold[["Close"]].rename(columns={"Close": "Gold"}).dropna()

    print(f"  Yahoo (GC=F): {len(gold)} obs.\n")
    return gold


def run_all():
    """Ejecuta el pipeline completo."""
    print("\n" + "=" * 70)
    print("MONEDA IDEAL - PIPELINE COMPLETO")
    print("=" * 70 + "\n")

    t0 = time.time()

    # 1. Descargas
    fx_data = descargar_todas(verbose=True)
    gold = descargar_oro()
    m2_fred = descargar_m2_fred(verbose=True)
    m2_wb = descargar_m2_world_bank(verbose=True)

    # 2. Calculos
    df_eo = calcular_eo_todos(fx_data, verbose=True)
    df_sv = calcular_sv_todos(fx_data, gold, verbose=True)
    df_sm2 = calcular_sm2_fred(m2_fred, verbose=True)
    sm2_wb = calcular_sm2_wb(m2_wb, verbose=True)

    # 3. Distancia
    df_D = construir_distancia(df_eo, df_sv, df_sm2, sm2_wb, verbose=True)

    # 4. Guardar
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)

    df_eo.to_excel(os.path.join(PROCESSED_DATA_DIR, "Eo_anual.xlsx"))
    df_sv.to_excel(os.path.join(PROCESSED_DATA_DIR, "Sv_anual.xlsx"))
    df_sm2.to_excel(os.path.join(PROCESSED_DATA_DIR, "SM2_anual.xlsx"))
    df_D.to_excel(os.path.join(PROCESSED_DATA_DIR, "distancia_D.xlsx"))

    # 5. Analisis
    df_completo = df_D.dropna(subset=["Eo", "Sv", "SM2", "D"])
    df_completo = anadir_posicionamiento(df_completo)

    print("\n" + "=" * 70)
    print("TABLA COMPLETA")
    print("=" * 70)
    cols = ["Eo", "Sv", "SM2", "D", "Reservas_COFER", "BIS_Turnover"]
    print("\n", df_completo[cols].round(4).to_string())

    corr = analizar_correlaciones(df_completo, verbose=True)
    reg = analizar_regresion(df_completo, verbose=True)
    umbral = analizar_umbral(df_completo, verbose=True)
    robust = analizar_robustez(df_completo, verbose=True)
    d2 = analizar_d2(df_completo, verbose=True)

    # 6. Guardar resultados
    corr.to_excel(os.path.join(TABLES_DIR, "correlaciones.xlsx"), index=False)
    reg.to_excel(os.path.join(TABLES_DIR, "regresiones.xlsx"), index=False)
    umbral.to_excel(os.path.join(TABLES_DIR, "umbral.xlsx"), index=False)
    robust.to_excel(os.path.join(TABLES_DIR, "robustez.xlsx"), index=False)
    d2.to_excel(os.path.join(TABLES_DIR, "d2_sin_m2.xlsx"), index=False)
    df_completo.to_excel(os.path.join(PROCESSED_DATA_DIR, "datos_completos.xlsx"))

    t1 = time.time()
    print(f"\n  Tiempo total: {t1 - t0:.1f} seg")
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    run_all()
