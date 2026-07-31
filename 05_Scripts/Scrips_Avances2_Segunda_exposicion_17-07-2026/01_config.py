"""
01_config.py
=============

Configuración general del proyecto de análisis geoespacial de cobre.

Uso recomendado en Google Colab
-------------------------------
1. Guarda este archivo en:
   MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/01_config.py

2. Ejecútalo desde el notebook con:
   %run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/01_config.py"

El script:
- conecta Google Drive cuando se ejecuta en Colab;
- define la estructura de directorios;
- crea las carpetas que no existan;
- importa las librerías generales del proyecto;
- define parámetros globales reproducibles.
"""

from __future__ import annotations

import warnings
from pathlib import Path

# ==========================================================
# 1. CONEXIÓN CON GOOGLE DRIVE
# ==========================================================

RUTA_DRIVE = Path("/content/drive")
RUTA_PROYECTO = RUTA_DRIVE / "MyDrive" / "Analisis_Geoespacial_Cobre"


def conectar_drive(forzar_remontaje: bool = False) -> None:
    """
    Conecta Google Drive cuando el script se ejecuta en Google Colab.

    Fuera de Colab no genera error; únicamente muestra una advertencia.
    """
    try:
        from google.colab import drive
    except ImportError:
        print(
            "Advertencia: el entorno actual no es Google Colab. "
            "Google Drive no fue montado."
        )
        return

    if RUTA_DRIVE.exists() and any(RUTA_DRIVE.iterdir()):
        print("Google Drive ya se encuentra conectado.")
        return

    drive.mount(
        str(RUTA_DRIVE),
        force_remount=forzar_remontaje,
    )


conectar_drive()


# ==========================================================
# 2. ESTRUCTURA DE DIRECTORIOS
# ==========================================================

# Notebook
NOTEBOOK = RUTA_PROYECTO / "01_Notebook"

# Datos
DATOS = RUTA_PROYECTO / "02_Datos"
ORIGINALES = DATOS / "01_Originales"
PROCESADOS = DATOS / "02_Procesados"
ESTUDIO = DATOS / "03_Estudio"

# Figuras
FIGURAS = RUTA_PROYECTO / "03_Figuras"

# Resultados
RESULTADOS = RUTA_PROYECTO / "04_Resultados"
TABLAS = RESULTADOS / "01_Tablas"
MODELOS = RESULTADOS / "02_Modelos"
VALIDACION = RESULTADOS / "03_Validacion"

# Código fuente
SCRIPTS = RUTA_PROYECTO / "05_Scripts"

# Documentación
DOCUMENTACION = RUTA_PROYECTO / "06_Documentacion"


CARPETAS_PROYECTO = [
    RUTA_PROYECTO,
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


def crear_directorios() -> None:
    """Crea la estructura de carpetas del proyecto si no existe."""
    for carpeta in CARPETAS_PROYECTO:
        carpeta.mkdir(parents=True, exist_ok=True)


crear_directorios()


# ==========================================================
# 3. IMPORTACIÓN DE LIBRERÍAS GENERALES
# ==========================================================

import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

try:
    import contextily as ctx
except ImportError as exc:
    raise ImportError(
        "No se encontró 'contextily'. Instálalo en Colab con: "
        "!pip -q install contextily"
    ) from exc

try:
    from adjustText import adjust_text
except ImportError as exc:
    raise ImportError(
        "No se encontró 'adjustText'. Instálalo en Colab con: "
        "!pip -q install adjustText"
    ) from exc

try:
    from matplotlib_scalebar.scalebar import ScaleBar
except ImportError as exc:
    raise ImportError(
        "No se encontró 'matplotlib-scalebar'. Instálalo en Colab con: "
        "!pip -q install matplotlib-scalebar"
    ) from exc

try:
    from pointpats import QStatistic
    from pointpats import random as pp_random
except ImportError as exc:
    raise ImportError(
        "No se encontró 'pointpats'. Instálalo en Colab con: "
        "!pip -q install pointpats"
    ) from exc

from matplotlib.lines import Line2D
from matplotlib.patches import Patch


# ==========================================================
# 4. PARÁMETROS GENERALES DEL ANÁLISIS
# ==========================================================

# Sistema de referencia proyectado utilizado en el proyecto
CRS_PROYECTO = "EPSG:21897"

# Parámetros reproducibles
SEMILLA = 1234
N_SIMULACIONES = 999
NIVEL_SIGNIFICANCIA = 0.05

# Parámetros geoquímicos
PERCENTIL_ANOMALIA = 90
MINIMO_MUESTRAS_UNIDAD = 10

# Configuración NumPy
np.random.seed(SEMILLA)
np.set_printoptions(
    precision=4,
    suppress=True,
)

# Configuración Pandas
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)
pd.set_option("display.float_format", lambda valor: f"{valor:,.4f}")

# Advertencias
warnings.filterwarnings("ignore")


# ==========================================================
# 5. CONFIGURACIÓN GRÁFICA GENERAL
# ==========================================================

mpl.rcParams.update(
    {
        "figure.figsize": (10, 7),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "axes.grid": False,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.constrained_layout.use": False,
    }
)


# ==========================================================
# 6. FUNCIONES GENERALES DE EXPORTACIÓN
# ==========================================================

def guardar_figura(
    figura: mpl.figure.Figure,
    nombre_archivo: str,
    *,
    dpi: int = 300,
    cerrar: bool = False,
) -> Path:
    """
    Guarda una figura en la carpeta 03_Figuras.

    Parameters
    ----------
    figura:
        Objeto Figure de Matplotlib.
    nombre_archivo:
        Nombre del archivo, incluida la extensión.
    dpi:
        Resolución de salida.
    cerrar:
        Si True, cierra la figura después de guardarla.
    """
    ruta_salida = FIGURAS / nombre_archivo
    figura.savefig(
        ruta_salida,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.15,
    )

    if cerrar:
        plt.close(figura)

    print(f"Figura guardada: {ruta_salida}")
    return ruta_salida


def guardar_tabla(
    tabla: pd.DataFrame,
    nombre_archivo: str,
    *,
    indice: bool = False,
) -> Path:
    """
    Guarda una tabla en CSV dentro de 04_Resultados/01_Tablas.
    """
    ruta_salida = TABLAS / nombre_archivo
    tabla.to_csv(
        ruta_salida,
        index=indice,
        encoding="utf-8-sig",
    )
    print(f"Tabla guardada: {ruta_salida}")
    return ruta_salida


# ==========================================================
# 7. VERIFICACIÓN
# ==========================================================

def mostrar_configuracion() -> None:
    """Muestra un resumen de la configuración activa."""
    print("=" * 72)
    print("CONFIGURACIÓN GENERAL DEL PROYECTO")
    print("=" * 72)
    print(f"Proyecto          : {RUTA_PROYECTO}")
    print(f"Datos procesados  : {PROCESADOS}")
    print(f"Datos de estudio  : {ESTUDIO}")
    print(f"Figuras           : {FIGURAS}")
    print(f"Tablas            : {TABLAS}")
    print(f"Modelos           : {MODELOS}")
    print(f"Validación        : {VALIDACION}")
    print(f"Scripts           : {SCRIPTS}")
    print(f"CRS del proyecto  : {CRS_PROYECTO}")
    print(f"Semilla           : {SEMILLA}")
    print(f"Simulaciones      : {N_SIMULACIONES}")
    print("=" * 72)
    print("Configuración cargada correctamente.")


mostrar_configuracion()
