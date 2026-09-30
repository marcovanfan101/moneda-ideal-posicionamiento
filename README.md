# Distancia a la Moneda Ideal y Posicionamiento Global

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/marcovanfan101/moneda-ideal-posicionamiento/blob/main/notebooks/run_and_visualize.ipynb)

Codigo de replicacion para la tesis:

**"Distancia a la Moneda Ideal y posicionamiento global: un umbral empirico en la calidad monetaria de las divisas (2010-2025)"**

Marco Antonio Lopez Lazaro
Universidad de San Martin de Porres, 2026

## Como ejecutar

### Opcion 1: Un click en Colab (recomendado)

Click en el boton **Open in Colab** arriba. El notebook ejecuta todo automaticamente.

### Opcion 2: Manualmente en Colab

    !git clone https://github.com/marcovanfan101/moneda-ideal-posicionamiento.git
    %cd moneda-ideal-posicionamiento
    !pip install -q yfinance pandas numpy pandas-datareader requests scipy openpyxl matplotlib seaborn
    !python scripts/01_run_all.py

### Opcion 3: Localmente

    git clone https://github.com/marcovanfan101/moneda-ideal-posicionamiento.git
    cd moneda-ideal-posicionamiento
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python scripts/01_run_all.py

## Hallazgo principal

**Existe un umbral en D = 0.10.** Las 7 divisas con D < 0.10 concentran el **90.6%** de las reservas internacionales, mientras que las 16 divisas con D >= 0.10 concentran solo el **6.8%**.

## Resultados principales

| Prueba | Valor | p-valor |
|--------|-------|---------|
| Spearman D vs Reservas | -0.71 | 0.0002 |
| Spearman D vs BIS | -0.74 | 0.0001 |
| Regresion log(Reservas) vs D | R2 = 0.41 | 0.0055 |
| Umbral D=0.10 (Mann-Whitney) | 90.6% reservas | 0.0006 |

## Estructura del proyecto

    moneda-ideal-posicionamiento/
    |-- config/                # configuracion y diccionarios
    |-- src/                   # modulos de codigo
    |-- scripts/               # scripts de ejecucion
    |-- notebooks/             # notebooks para ejecutar en Colab
    |-- data/                  # datos crudos y procesados
    |-- results/               # figuras y tablas
    |-- docs/                  # documentacion

## Metodologia

### Indice de Eficiencia Operativa (Eo)

    CT_t = sqrt(1/(4*ln(2))) * |ln(H_t / L_t)| * 100
    Eo_y = 100 / (1 + mean(CT_t))

### Indice de Entropia Valorativa (Sv)

    VAU_t = (1 / e_t) * P_gold,t
    Sv_y = std(ln(VAU_t / VAU_{t-1})) * sqrt(252)

### Indice de Entropia de M2 (SM2)

    SM2_y = std(ln(M2_t / M2_{t-1})) * sqrt(12)

### Metrica de Distancia

    D = (100 - Eo) * Sv * SM2

## Fuentes de datos

| Dato | Fuente |
|------|--------|
| Tipos de cambio | Yahoo Finance |
| Precio del oro | Yahoo Finance (GC=F) |
| M2 (20 paises) | FRED |
| M2 (SGP, ARG, IND) | Banco Mundial |
| Reservas | IMF COFER Q4 2024 |
| Turnover | BIS Triennial Survey 2022 |

## Como citar

    Lopez Lazaro, M. A. (2026). Distancia a la Moneda Ideal y posicionamiento
    global: un umbral empirico en la calidad monetaria de las divisas
    (2010-2025). Tesis de licenciatura, Universidad de San Martin de Porres.

## Licencia

MIT License. Ver LICENSE.
