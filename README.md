# Distancia a la Moneda Ideal y Posicionamiento Global

Codigo de replicacion para la tesis:

**"Distancia a la Moneda Ideal y posicionamiento global: un umbral empirico en la calidad monetaria de las divisas (2010-2025)"**

Marco Antonio Lopez Lazaro
Universidad de San Martin de Porres, 2026

## Resumen

Este repositorio contiene el codigo completo para:

1. Descargar datos de tipos de cambio, precio del oro y agregados monetarios M2.
2. Calcular los indices de Eficiencia Operativa (Eo), Entropia Valorativa (Sv) y Entropia de M2 (SM2).
3. Construir la metrica de distancia a la Moneda Ideal: D = (100 - Eo) * Sv * SM2.
4. Contrastar la hipotesis principal: las divisas mas cercanas al ideal tienen mayor posicionamiento global.

## Hallazgo principal

Existe un umbral en D aproximadamente 0.10. Las 7 divisas con D < 0.10 concentran el 90.6 por ciento de las reservas internacionales, mientras que las 16 divisas con D >= 0.10 concentran solo el 6.8 por ciento.

## Estructura del proyecto

    moneda-ideal-posicionamiento/
    |-- config/                # configuracion y diccionarios
    |-- src/                   # modulos de codigo
    |-- scripts/               # scripts de ejecucion
    |-- data/                  # datos crudos y procesados
    |-- results/               # figuras y tablas
    |-- notebooks/             # analisis exploratorio
    |-- docs/                  # documentacion

## Requisitos

- Python 3.9 o superior
- Ver requirements.txt

## Instalacion

    git clone https://github.com/marcovanfan101/moneda-ideal-posicionamiento.git
    cd moneda-ideal-posicionamiento
    python -m venv venv
    source venv/bin/activate   # En Windows: venv\Scripts\activate
    pip install -r requirements.txt

## Uso

    python scripts/01_run_all.py

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
| Reservas | IMF COFER |
| Turnover | BIS Triennial Survey 2022 |

## Resultados principales

| Prueba | Valor | p-valor |
|--------|-------|---------|
| Spearman D vs Reservas | -0.71 | 0.0002 |
| Spearman D vs BIS | -0.74 | 0.0001 |
| Regresion log(Reservas) vs D | R2 = 0.41 | 0.0055 |
| Umbral D=0.10 (Mann-Whitney) | 90.6% reservas | 0.0006 |

## Como citar

    Lopez Lazaro, M. A. (2026). Distancia a la Moneda Ideal y posicionamiento
    global: un umbral empirico en la calidad monetaria de las divisas
    (2010-2025). Tesis de licenciatura, Universidad de San Martin de Porres.

## Licencia

MIT License. Ver LICENSE.
