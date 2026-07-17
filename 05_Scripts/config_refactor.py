"""
Configuración portable del proyecto.

La raíz del repositorio se detecta automáticamente a partir de la
ubicación de este archivo. No utiliza Google Drive ni rutas absolutas.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib as mpl
import numpy as np
import pandas as pd

# ==========================================================
# RUTAS
# ==========================================================

RUTA_PROYECTO = Path(__file__).resolve().parents[1]

NOTEBOOK = RUTA_PROYECTO / "01_Notebook"

DATOS = RUTA_PROYECTO / "02_Datos"
ORIGINALES = DATOS / "01_Originales"
PROCESADOS = DATOS / "02_Procesados"
ESTUDIO = DATOS / "03_Estudio"

FIGURAS = RUTA_PROYECTO / "03_Figuras"

RESULTADOS = RUTA_PROYECTO / "04_Resultados"
TABLAS = RESULTADOS / "01_Tablas"
MODELOS = RESULTADOS / "02_Modelos"
VALIDACION = RESULTADOS / "03_Validacion"

SCRIPTS = RUTA_PROYECTO / "05_Scripts"
DOCUMENTACION = RUTA_PROYECTO / "06_Documentacion"

CARPETAS_SALIDA = [
    NOTEBOOK,
    DATOS,
    ORIGINALES,
    PROCESADOS,
    ESTUDIO,
    FIGURAS,
    RESULTADOS,
    TABLAS,
    MODELOS,
    VALIDACION,
    SCRIPTS,
    DOCUMENTACION,
]

for carpeta in CARPETAS_SALIDA:
    carpeta.mkdir(parents=True, exist_ok=True)

# ==========================================================
# PARÁMETROS
# ==========================================================

CRS_PROYECTO = "EPSG:21897"
SEMILLA = 1234
N_SIMULACIONES = 999
NIVEL_SIGNIFICANCIA = 0.05
PERCENTIL_ANOMALIA = 90
MINIMO_MUESTRAS_UNIDAD = 10

np.random.seed(SEMILLA)
np.set_printoptions(precision=4, suppress=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)
pd.set_option("display.float_format", lambda valor: f"{valor:,.4f}")

warnings.filterwarnings("ignore")

mpl.rcParams.update(
    {
        "figure.figsize": (10, 7),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
    }
)


def mostrar_configuracion() -> None:
    """Muestra las rutas y parámetros principales."""
    print("=" * 72)
    print("CONFIGURACIÓN DEL PROYECTO")
    print("=" * 72)
    print(f"Raíz       : {RUTA_PROYECTO}")
    print(f"Procesados : {PROCESADOS}")
    print(f"Estudio    : {ESTUDIO}")
    print(f"Figuras    : {FIGURAS}")
    print(f"Tablas     : {TABLAS}")
    print(f"CRS        : {CRS_PROYECTO}")
    print(f"Semilla    : {SEMILLA}")
    print("=" * 72)
