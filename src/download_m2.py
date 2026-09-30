"""
Modulo para descargar M2 desde FRED y Banco Mundial.
"""

import warnings
warnings.filterwarnings("ignore")

import requests
import pandas as pd
import pandas_datareader.data as web

from config.config import (
    START_DATE, END_DATE, START_YEAR, END_YEAR,
    M2_FRED_SERIES, M2_WORLD_BANK
)


def descargar_m2_fred(verbose=True):
    """
    Descarga series de M2 desde FRED.
    Devuelve: {codigo_pais: DataFrame}
    """
    if verbose:
        print("=" * 70)
        print("DESCARGANDO M2 DE FRED")
        print("=" * 70)

    m2_data = {}

    for pais, sid in M2_FRED_SERIES.items():
        if verbose:
            print(f"  {pais:5s} {sid:25s}...", end=" ")

        try:
            df = web.DataReader(sid, "fred", START_DATE, END_DATE)
            df.columns = ["M2"]
            df = df.dropna()

            if len(df) < 24:
                if verbose:
                    print(f"INSUF ({len(df)})")
                continue

            m2_data[pais] = df
            if verbose:
                print(f"OK ({len(df)} obs.)")

        except Exception:
            if verbose:
                print("FALLO")

    if verbose:
        print(f"\n  Paises con M2: {len(m2_data)}\n")

    return m2_data


def descargar_pais_wb(pais, max_reintentos=5, verbose=True):
    """
    Descarga M2 de un pais del Banco Mundial con reintentos.
    Indicador: FM.LBL.BMNY.CN (Broad money, current LCU).
    """
    indicador = "FM.LBL.BMNY.CN"
    url = (f"https://api.worldbank.org/v2/country/{pais}/indicator/"
           f"{indicador}?date={START_YEAR}:{END_YEAR}&format=json&per_page=100")

    for intento in range(max_reintentos):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                js = r.json()
                if len(js) > 1 and js[1]:
                    datos = {}
                    for obs in js[1]:
                        if obs["value"] is not None:
                            datos[int(obs["date"])] = obs["value"]
                    if len(datos) >= 5:
                        return pd.Series(datos).sort_index()
        except Exception:
            pass

        if intento < max_reintentos - 1 and verbose:
            print(f"    Reintento {intento + 1}...")

    return None


def descargar_m2_world_bank(verbose=True):
    """
    Descarga M2 del Banco Mundial para SGP, ARG, IND.
    Devuelve: DataFrame con anios en indice y paises en columnas.
    """
    if verbose:
        print("=" * 70)
        print("DESCARGANDO M2 DEL BANCO MUNDIAL")
        print("=" * 70)

    datos = {}

    for pais in M2_WORLD_BANK.keys():
        if verbose:
            print(f"  {pais}...", end=" ")

        serie = descargar_pais_wb(pais, verbose=verbose)
        if serie is not None and not serie.empty:
            for year, valor in serie.items():
                datos.setdefault(year, {})[pais] = valor
            if verbose:
                print(f"{len(serie)} obs.")
        else:
            if verbose:
                print("sin datos")

    df = pd.DataFrame(datos).T.sort_index()
    df.index.name = "year"

    if verbose:
        print()

    return df
