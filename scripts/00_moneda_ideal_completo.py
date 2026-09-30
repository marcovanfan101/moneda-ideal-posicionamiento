"""
================================================================
MONEDA IDEAL Y POSICIONAMIENTO GLOBAL
================================================================
Script completo: descarga, calcula, analiza y muestra todos
los resultados en una sola ejecucion.

Uso en Colab:
    !python scripts/00_moneda_ideal_completo.py

Tesis de licenciatura - Marco Antonio Lopez Lazaro
Universidad de San Martin de Porres, 2026
================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import os
import time
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import pandas_datareader.data as web
from scipy.stats import spearmanr, pearsonr, mannwhitneyu, linregress

# ================================================================
# CONFIGURACION
# ================================================================
START_DATE = "2010-01-01"
END_DATE   = "2025-12-31"
START_YEAR = 2010
END_YEAR   = 2025
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("results/tables", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)

PARKINSON_CONST = np.sqrt(1.0 / (4.0 * np.log(2.0)))

CURRENCIES = {
    "EUR": ("EURUSD=X", True), "GBP": ("GBPUSD=X", True),
    "JPY": ("JPY=X", False), "CHF": ("CHF=X", False),
    "CAD": ("CAD=X", False), "AUD": ("AUDUSD=X", True),
    "NZD": ("NZDUSD=X", True), "CNY": ("CNY=X", False),
    "HKD": ("HKD=X", False), "SGD": ("SGD=X", False),
    "KRW": ("KRW=X", False), "INR": ("INR=X", False),
    "NOK": ("NOK=X", False), "SEK": ("SEK=X", False),
    "DKK": ("DKK=X", False), "PLN": ("PLN=X", False),
    "CZK": ("CZK=X", False), "HUF": ("HUF=X", False),
    "RON": ("RON=X", False), "TRY": ("TRY=X", False),
    "RUB": ("RUB=X", False), "ISK": ("ISK=X", False),
    "BRL": ("BRL=X", False), "MXN": ("MXN=X", False),
    "ARS": ("ARS=X", False), "CLP": ("CLP=X", False),
    "COP": ("COP=X", False), "PEN": ("PEN=X", False),
    "UYU": ("UYU=X", False), "IDR": ("IDR=X", False),
    "MYR": ("MYR=X", False), "PHP": ("PHP=X", False),
    "THB": ("THB=X", False), "TWD": ("TWD=X", False),
    "PKR": ("PKR=X", False), "BDT": ("BDT=X", False),
    "LKR": ("LKR=X", False), "KZT": ("KZT=X", False),
    "ZAR": ("ZAR=X", False), "EGP": ("EGP=X", False),
    "NGN": ("NGN=X", False), "KES": ("KES=X", False),
    "MAD": ("MAD=X", False), "ILS": ("ILS=X", False),
    "SAR": ("SAR=X", False), "AED": ("AED=X", False),
}
USD_TICKER = "DX-Y.NYB"

M2_FRED = {
    "USA": "M2SL", "JPN": "MYAGM2JPM189N", "CHN": "MYAGM2CNM189N",
    "KOR": "MYAGM2KRM189N", "BRA": "MYAGM2BRM189N", "MEX": "MYAGM2MXM189N",
    "ZAF": "MYAGM2ZAM189N", "TUR": "MYAGM2TRM189N",
    "GBR": "MABMM301GBM189S", "CAN": "MABMM301CAM189S", "AUS": "MABMM301AUM189S",
    "CHE": "MABMM301CHM189S", "SWE": "MABMM301SEM189S", "NOR": "MABMM301NOM189S",
    "DNK": "MABMM301DKM189S", "POL": "MABMM301PLM189S", "CZE": "MABMM301CZM189S",
    "HUN": "MABMM301HUM189S", "CHL": "MABMM301CLM189S", "EUZ": "MABMM301EZM189S",
}
M2_WB = {"SGP": "SGD", "ARG": "ARS", "IND": "INR"}

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

# POSICIONAMIENTO GLOBAL (IMF COFER Q4 2024 + BIS Triennial 2022)
POSICIONAMIENTO = {
    "USD": (57.80, 88.50), "EUR": (19.80, 30.50), "JPY": (5.50, 16.70),
    "GBP": (4.70, 12.90), "CNY": (2.30, 7.00), "CAD": (2.80, 6.20),
    "AUD": (2.20, 6.40), "CHF": (0.20, 5.20), "HKD": (0.00, 2.40),
    "SGD": (0.40, 1.70), "KRW": (0.50, 1.80), "SEK": (0.40, 2.10),
    "NOK": (0.10, 1.70), "DKK": (0.10, 0.70), "MXN": (0.30, 2.50),
    "INR": (0.00, 0.60), "BRL": (0.10, 0.90), "ZAR": (0.10, 0.70),
    "TRY": (0.00, 0.50), "PLN": (0.10, 0.50), "CZK": (0.00, 0.30),
    "HUF": (0.00, 0.30), "ILS": (0.00, 0.30), "CLP": (0.00, 0.20),
    "ARS": (0.00, 0.10),
}


# ================================================================
# FUNCIONES DE DESCARGA
# ================================================================

def descargar_fx(ticker):
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


def descargar_todos_fx():
    print("=" * 70)
    print("1. DESCARGANDO TIPOS DE CAMBIO (Yahoo Finance)")
    print("=" * 70)
    fx = {}
    for code, (ticker, inv) in CURRENCIES.items():
        print(f"  {code:4s} {ticker:12s}...", end=" ")
        df = descargar_fx(ticker)
        if df is None or df.empty:
            print("SIN DATOS")
            continue
        if inv:
            h, l, c = df["High"].copy(), df["Low"].copy(), df["Close"].copy()
            df["Close"] = 1.0 / c
            df["High"] = 1.0 / l
            df["Low"] = 1.0 / h
        mask = df["High"] >= df["Low"]
        if not mask.all():
            df = df[mask]
        fx[code] = df
        print(f"OK ({len(df)})")

    print(f"  USD  {USD_TICKER:12s}...", end=" ")
    dxy = descargar_fx(USD_TICKER)
    if dxy is not None and not dxy.empty:
        fx["USD"] = dxy
        print(f"OK ({len(dxy)})")

    print(f"\n  Total: {len(fx)} divisas\n")
    return fx


def descargar_oro():
    print("=" * 70)
    print("2. DESCARGANDO PRECIO DEL ORO")
    print("=" * 70)
    try:
        g = web.DataReader("GOLDPMGBD228NLBM", "fred", START_DATE, END_DATE)
        g.columns = ["Gold"]
        g = g.dropna()
        if len(g) > 100:
            print(f"  FRED: {len(g)} obs.\n")
            return g
    except Exception:
        pass
    g = yf.download("GC=F", start=START_DATE, end=END_DATE,
                    progress=False, auto_adjust=False)
    if isinstance(g.columns, pd.MultiIndex):
        g.columns = g.columns.get_level_values(0)
    g = g[["Close"]].rename(columns={"Close": "Gold"}).dropna()
    print(f"  Yahoo (GC=F): {len(g)} obs.\n")
    return g


def descargar_m2_fred():
    print("=" * 70)
    print("3. DESCARGANDO M2 DE FRED (20 paises)")
    print("=" * 70)
    m2 = {}
    for pais, sid in M2_FRED.items():
        print(f"  {pais:5s} {sid:25s}...", end=" ")
        try:
            df = web.DataReader(sid, "fred", START_DATE, END_DATE)
            df.columns = ["M2"]
            df = df.dropna()
            if len(df) < 24:
                print(f"INSUF ({len(df)})")
                continue
            m2[pais] = df
            print(f"OK ({len(df)})")
        except Exception:
            print("FALLO")
    print(f"\n  Paises: {len(m2)}\n")
    return m2


def descargar_m2_wb():
    print("=" * 70)
    print("4. DESCARGANDO M2 DEL BANCO MUNDIAL (SGP, ARG, IND)")
    print("=" * 70)
    ind = "FM.LBL.BMNY.CN"
    datos = {}
    for pais in M2_WB:
        print(f"  {pais}...", end=" ")
        url = (f"https://api.worldbank.org/v2/country/{pais}/indicator/"
               f"{ind}?date={START_YEAR}:{END_YEAR}&format=json&per_page=100")
        for intento in range(5):
            try:
                r = requests.get(url, timeout=60)
                if r.status_code == 200:
                    js = r.json()
                    if len(js) > 1 and js[1]:
                        n = 0
                        for o in js[1]:
                            if o["value"] is not None:
                                datos.setdefault(int(o["date"]), {})[pais] = o["value"]
                                n += 1
                        print(f"{n} obs.")
                        break
            except Exception:
                if intento < 4:
                    continue
        else:
            print("sin datos")
    df = pd.DataFrame(datos).T.sort_index()
    df.index.name = "year"
    print()
    return df


# ================================================================
# CALCULO DE INDICES
# ================================================================

def calc_eo(df):
    df = df.copy()
    df["CT"] = PARKINSON_CONST * np.abs(np.log(df["High"] / df["Low"])) * 100
    df["year"] = df.index.year
    eo = df.groupby("year")["CT"].mean().to_frame()
    eo["Eo"] = 100.0 / (1.0 + eo["CT"])
    return eo["Eo"]


def calc_eo_todos(fx):
    print("=" * 70)
    print("5. CALCULANDO Eo (Eficiencia Operativa)")
    print("=" * 70)
    res = {}
    for code, df in fx.items():
        try:
            res[code] = calc_eo(df)
        except Exception:
            pass
    df_eo = pd.DataFrame(res)
    print(f"  Divisas: {df_eo.shape[1]}")
    print(f"  Rango: {df_eo.mean().min():.2f} a {df_eo.mean().max():.2f}\n")
    return df_eo


def calc_sv(df_fx, gold):
    df = df_fx[["Close"]].join(gold, how="inner").dropna()
    if len(df) < 30:
        return None
    df["VAU"] = (1.0 / df["Close"]) * df["Gold"]
    df["r"] = np.log(df["VAU"] / df["VAU"].shift(1))
    df = df.dropna()
    df["year"] = df.index.year
    return df.groupby("year")["r"].std() * np.sqrt(252)


def calc_sv_todos(fx, gold):
    print("=" * 70)
    print("6. CALCULANDO Sv (Entropia Valorativa)")
    print("=" * 70)
    res = {}
    for code, df in fx.items():
        try:
            sv = calc_sv(df, gold)
            if sv is not None:
                res[code] = sv
        except Exception:
            pass
    df_sv = pd.DataFrame(res)
    p95 = df_sv.stack().quantile(0.95)
    df_sv = df_sv.clip(upper=p95)
    print(f"  Divisas: {df_sv.shape[1]}")
    print(f"  Winsorizado P95: {p95:.4f}\n")
    return df_sv


def sm2_mensual(df):
    df = df.copy()
    df["r"] = np.log(df["M2"] / df["M2"].shift(1))
    df = df.dropna()
    df["year"] = df.index.year
    return df.groupby("year")["r"].std() * np.sqrt(12)


def sm2_anual(serie):
    serie = serie.dropna()
    if len(serie) < 5:
        return np.nan
    r = np.log(serie / serie.shift(1)).dropna()
    return r.std() if len(r) >= 3 else np.nan


def calc_sm2(m2_fred, m2_wb):
    print("=" * 70)
    print("7. CALCULANDO SM2 (Entropia de M2)")
    print("=" * 70)
    res = {}
    for code, df in m2_fred.items():
        try:
            s = sm2_mensual(df)
            if len(s) >= 5:
                res[code] = s
        except Exception:
            pass
    df_sm2 = pd.DataFrame(res)
    print(f"  FRED: {df_sm2.shape[1]}")

    wb_vals = {}
    for p in m2_wb.columns:
        v = sm2_anual(m2_wb[p])
        if not np.isnan(v):
            wb_vals[p] = v
            print(f"  {p}: SM2 = {v:.4f}")
    print()
    return df_sm2, wb_vals


def construir_D(df_eo, df_sv, df_sm2, sm2_wb):
    print("=" * 70)
    print("8. CONSTRUYENDO D = (100-Eo) * Sv * SM2")
    print("=" * 70)

    peo = df_eo.mean().to_frame("Eo")
    psv = df_sv.mean().to_frame("Sv")
    psm2 = df_sm2.mean().to_frame("SM2")
    df = peo.join(psv, how="outer").join(psm2, how="outer")

    sm2_map = {}
    for pais, v in df_sm2.mean().items():
        sm2_map[PAIS_A_DIVISA.get(pais, pais)] = v
    for pais, div in M2_WB.items():
        if pais in sm2_wb:
            sm2_map[div] = sm2_wb[pais]

    df["SM2"] = df.index.map(lambda x: sm2_map.get(x, np.nan))
    df["D"] = (100 - df["Eo"]) * df["Sv"] * df["SM2"]
    df["Reservas_COFER"] = df.index.map(
        lambda x: POSICIONAMIENTO.get(x, (np.nan, np.nan))[0]
    )
    df["BIS_Turnover"] = df.index.map(
        lambda x: POSICIONAMIENTO.get(x, (np.nan, np.nan))[1]
    )
    df = df.sort_values("D")
    completos = df.dropna(subset=["D"])
    print(f"  Divisas con los 3 indices: {len(completos)}\n")
    return df


# ================================================================
# ANALISIS
# ================================================================

def analizar_correlaciones(df):
    print("=" * 70)
    print("9. CORRELACIONES: D vs POSICIONAMIENTO")
    print("=" * 70)
    print()
    print(f"  {'Variable':<20} {'N':>4} {'Spearman':>10} {'p-valor':>10} "
          f"{'Pearson':>10} {'p-valor':>10}")
    print("  " + "-" * 70)

    for var in ["Reservas_COFER", "BIS_Turnover"]:
        d = df.dropna(subset=["D", var])
        rho, p_s = spearmanr(d["D"], d[var])
        r, p_p = pearsonr(d["D"], d[var])
        print(f"  {var:<20} {len(d):>4} {rho:>10.4f} {p_s:>10.4f} "
              f"{r:>10.4f} {p_p:>10.4f}")


def analizar_regresion(df):
    print()
    print("=" * 70)
    print("10. REGRESION log(posicionamiento) ~ D")
    print("=" * 70)
    print()
    print(f"  {'Variable':<20} {'N':>4} {'Pendiente':>12} {'R2':>8} {'p-valor':>10}")
    print("  " + "-" * 70)

    for var in ["Reservas_COFER", "BIS_Turnover"]:
        d = df[df[var] > 0].dropna(subset=["D", var]).copy()
        d["log_pos"] = np.log(d[var])
        slope, intercept, r_val, p_val, std_err = linregress(d["D"], d["log_pos"])
        print(f"  {var:<20} {len(d):>4} {slope:>12.4f} {r_val**2:>8.4f} "
              f"{p_val:>10.4f}")


def analizar_umbral(df):
    print()
    print("=" * 70)
    print("11. ANALISIS DE UMBRAL")
    print("=" * 70)
    print()
    print(f"  {'Umbral':>8} {'N_cerca':>8} {'Res_cerca':>12} "
          f"{'Res_lejos':>12} {'p-valor':>10}")
    print("  " + "-" * 70)

    df_p = df.dropna(subset=["D", "Reservas_COFER"])
    for u in np.arange(0.07, 0.16, 0.005):
        c = df_p[df_p["D"] < u]
        l = df_p[df_p["D"] >= u]
        if len(c) >= 3 and len(l) >= 3:
            r_c = c["Reservas_COFER"].sum()
            r_l = l["Reservas_COFER"].sum()
            try:
                _, p = mannwhitneyu(c["Reservas_COFER"], l["Reservas_COFER"],
                                    alternative="greater")
            except Exception:
                p = np.nan
            marker = " ←" if r_c > 90 else ""
            print(f"  {u:>8.3f} {len(c):>8} {r_c:>12.2f} "
                  f"{r_l:>12.2f} {p:>10.4f}{marker}")


def analizar_robustez(df):
    print()
    print("=" * 70)
    print("12. ROBUSTEZ: sin Turquia, sin Argentina")
    print("=" * 70)
    print()
    print(f"  {'Muestra':<20} {'Variable':<20} {'N':>4} {'rho':>10} {'p-valor':>10}")
    print("  " + "-" * 70)

    for exc in [None, "TRY", "ARS"]:
        sub = df if exc is None else df[df.index != exc]
        nombre = "Completa" if exc is None else f"Sin {exc}"
        for var in ["Reservas_COFER", "BIS_Turnover"]:
            d = sub.dropna(subset=["D", var])
            rho, p = spearmanr(d["D"], d[var])
            print(f"  {nombre:<20} {var:<20} {len(d):>4} {rho:>10.4f} {p:>10.4f}")


def analizar_d2(df):
    print()
    print("=" * 70)
    print("13. ANALISIS COMPLEMENTARIO D2 = (100-Eo)*Sv (sin SM2)")
    print("=" * 70)
    print()
    print(f"  {'Variable':<20} {'N':>4} {'rho':>10} {'p-valor':>10}")
    print("  " + "-" * 70)

    df = df.copy()
    df["D2"] = (100 - df["Eo"]) * df["Sv"]
    for var in ["Reservas_COFER", "BIS_Turnover"]:
        d = df.dropna(subset=["D2", var])
        rho, p = spearmanr(d["D2"], d[var])
        print(f"  {var:<20} {len(d):>4} {rho:>10.4f} {p:>10.4f}")


# ================================================================
# MAIN
# ================================================================

def main():
    print("\n" + "=" * 70)
    print("MONEDA IDEAL Y POSICIONAMIENTO GLOBAL")
    print("Tesis de licenciatura - Marco Antonio Lopez Lazaro")
    print(f"Periodo: {START_DATE} a {END_DATE}")
    print("=" * 70 + "\n")

    t0 = time.time()

    # Descargas
    fx = descargar_todos_fx()
    gold = descargar_oro()
    m2_fred = descargar_m2_fred()
    m2_wb = descargar_m2_wb()

    # Calculos
    df_eo = calc_eo_todos(fx)
    df_sv = calc_sv_todos(fx, gold)
    df_sm2, sm2_wb = calc_sm2(m2_fred, m2_wb)

    # Distancia
    df_D = construir_D(df_eo, df_sv, df_sm2, sm2_wb)
    df_completo = df_D.dropna(subset=["Eo", "Sv", "SM2", "D"])

    # ============================================================
    # MOSTRAR LA TABLA COMPLETA
    # ============================================================
    print("=" * 70)
    print("TABLA COMPLETA: Eo, Sv, SM2, D, POSICIONAMIENTO")
    print("=" * 70)
    print()
    cols = ["Eo", "Sv", "SM2", "D", "Reservas_COFER", "BIS_Turnover"]
    print(df_completo[cols].round(4).to_string())

    # ============================================================
    # GRUPO ELITE
    # ============================================================
    print()
    print("=" * 70)
    print("GRUPO ELITE: divisas con D < 0.10")
    print("=" * 70)
    print()
    cerca = df_completo[df_completo["D"] < 0.10]
    lejos = df_completo[df_completo["D"] >= 0.10]
    print(f"  Divisas con D < 0.10: {len(cerca)}")
    print(f"    Reservas totales: {cerca['Reservas_COFER'].sum():.2f}%")
    print(f"    BIS Turnover: {cerca['BIS_Turnover'].sum():.2f}%")
    print()
    print(f"  Divisas con D >= 0.10: {len(lejos)}")
    print(f"    Reservas totales: {lejos['Reservas_COFER'].sum():.2f}%")
    print(f"    BIS Turnover: {lejos['BIS_Turnover'].sum():.2f}%")

    # Analisis
    analizar_correlaciones(df_completo)
    analizar_regresion(df_completo)
    analizar_umbral(df_completo)
    analizar_robustez(df_completo)
    analizar_d2(df_completo)

    # Guardar
    df_eo.to_excel(f"{OUTPUT_DIR}/Eo_anual.xlsx")
    df_sv.to_excel(f"{OUTPUT_DIR}/Sv_anual.xlsx")
    df_sm2.to_excel(f"{OUTPUT_DIR}/SM2_anual.xlsx")
    df_completo.to_excel(f"{OUTPUT_DIR}/datos_completos.xlsx")

    t1 = time.time()
    print()
    print("=" * 70)
    print(f"PROCESO COMPLETADO en {t1 - t0:.1f} segundos")
    print("=" * 70)


if __name__ == "__main__":
    main()
