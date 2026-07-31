"""
05_patron_anomalias.py
======================

Capítulo 4. Patrón espacial de las anomalías de cobre

Este archivo fue generado a partir del notebook:
Analisis_Geoespacial_Cobre(1).ipynb

Ejecución en Google Colab
-------------------------
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/05_patron_anomalias.py"
"""

from __future__ import annotations

import runpy
from pathlib import Path

# ==========================================================
# 0. CARGAR EL SCRIPT PRECEDENTE
# ==========================================================

RUTA_DEPENDENCIA = Path(__file__).with_name("04_patron_muestreo.py")

if not RUTA_DEPENDENCIA.exists():
    raise FileNotFoundError(
        "No se encontró 04_patron_muestreo.py en la misma carpeta que este script."
    )

_contexto_previo = runpy.run_path(str(RUTA_DEPENDENCIA))
globals().update(_contexto_previo)

print("\n" + "=" * 72)
print("CAPÍTULO 4. PATRÓN ESPACIAL DE LAS ANOMALÍAS DE COBRE")
print("=" * 72)



# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 96
# ==========================================================
# ==========================================================
# 4.1 DEFINICIÓN DEL UMBRAL DE ANOMALÍA
# TABLA 4.1 (UMBRALES CANDIDATOS) Y FIGURA 4.1
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# 1. Preparar la variable Cu
# ----------------------------------------------------------

if "muestras" not in globals():
    raise NameError(
        "No se encontró la capa de muestras. Ejecuta primero "
        "la preparación de los datos (capítulo 1)."
    )

cu_umbral = pd.to_numeric(
    muestras["Cu"],
    errors="coerce"
).dropna()

numero_muestras_umbral = len(cu_umbral)


# ----------------------------------------------------------
# 2. Calcular el percentil 90
# ----------------------------------------------------------

percentil_90 = float(np.percentile(cu_umbral, 90))

empates_p90 = int((cu_umbral == percentil_90).sum())


# ----------------------------------------------------------
# 3. Evaluar los umbrales candidatos
# ----------------------------------------------------------

candidatos_umbral = [
    (
        "Percentil 90 estricto",
        f"Cu > {percentil_90:,.0f} ppm",
        int((cu_umbral > percentil_90).sum())
    ),
    (
        "Percentil 90 inclusivo (adoptado)",
        f"Cu >= {percentil_90:,.0f} ppm",
        int((cu_umbral >= percentil_90).sum())
    ),
    (
        "Límite de valores atípicos (boxplot)",
        "Cu >= 200 ppm",
        int((cu_umbral >= 200).sum())
    ),
]

tabla_4_1 = pd.DataFrame({
    "Criterio": [c[0] for c in candidatos_umbral],
    "Condición": [c[1] for c in candidatos_umbral],
    "Anomalías resultantes": [c[2] for c in candidatos_umbral],
    "Porcentaje del total (%)": [
        c[2] / numero_muestras_umbral * 100
        for c in candidatos_umbral
    ]
})


# ----------------------------------------------------------
# 4. Definir el umbral oficial del estudio
# ----------------------------------------------------------

umbral_anomalia = percentil_90

print("=" * 68)
print("DEFINICIÓN DEL UMBRAL DE ANOMALÍA")
print("=" * 68)
print(f"Percentil 90               : {percentil_90:,.1f} ppm")
print(f"Muestras empatadas en P90  : {empates_p90}")
print(f"Umbral adoptado            : Cu >= {umbral_anomalia:,.1f} ppm")
print("=" * 68)


# ----------------------------------------------------------
# 5. Mostrar y guardar la Tabla 4.1
# ----------------------------------------------------------

tabla_4_1_estilizada = (
    tabla_4_1.style
    .hide(axis="index")
    .set_caption(
        "Tabla 4.1. Umbrales candidatos para la definición "
        "de las anomalías de cobre."
    )
    .format({
        "Anomalías resultantes": "{:,.0f}",
        "Porcentaje del total (%)": "{:.2f}"
    })
    .set_properties(
        subset=[
            "Condición",
            "Anomalías resultantes",
            "Porcentaje del total (%)"
        ],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_4_1.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_4-1_Umbrales_Candidatos.csv",
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 6. Figura 4.1: distribución de Cu y umbral adoptado
# ----------------------------------------------------------

valores_unicos, conteos_unicos = np.unique(
    cu_umbral,
    return_counts=True
)

numero_anomalias_umbral = int(
    (cu_umbral >= umbral_anomalia).sum()
)

figura_umbral, eje_umbral = plt.subplots(figsize=(12, 6.5))

eje_umbral.bar(
    valores_unicos,
    conteos_unicos,
    width=8,
    color="#7B9EC9",
    edgecolor="#3B5A80",
    linewidth=0.5
)

eje_umbral.axvline(
    umbral_anomalia,
    color="#B22222",
    linestyle="--",
    linewidth=2.2
)

eje_umbral.axvspan(
    umbral_anomalia,
    float(cu_umbral.max()) + 20,
    color="#B22222",
    alpha=0.06
)

eje_umbral.text(
    umbral_anomalia,
    conteos_unicos.max() * 0.95,
    (
        "  Umbral de anomalía\n"
        f"  P90 = {umbral_anomalia:,.0f} ppm"
    ),
    color="#B22222",
    fontsize=12,
    fontweight="bold",
    ha="left",
    va="top"
)

eje_umbral.text(
    0.98, 0.80,
    (
        f"n = {numero_muestras_umbral:,}\n"
        f"Anomalías (Cu ≥ {umbral_anomalia:,.0f} ppm) = "
        f"{numero_anomalias_umbral}\n"
        f"({numero_anomalias_umbral / numero_muestras_umbral * 100:.2f} %)"
    ),
    transform=eje_umbral.transAxes,
    ha="right",
    va="top",
    fontsize=11,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.5"
    )
)

eje_umbral.set_xlim(0, 1020)
eje_umbral.set_xlabel("Concentración de cobre (ppm)")
eje_umbral.set_ylabel("Número de muestras")
eje_umbral.set_title(
    "Distribución de la concentración de cobre y umbral "
    "de anomalía",
    fontweight="bold"
)
eje_umbral.grid(alpha=0.3, axis="y")

figura_umbral.text(
    0.99, 0.01,
    "Fuente: base geoquímica de Cu y elaboración propia.",
    ha="right",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.02, 1, 1])

plt.savefig(
    FIGURAS / "Figura_4-1_Umbral_Anomalia.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

tabla_4_1_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 98
# ==========================================================
# ==========================================================
# 4.2 TRANSFORMACIÓN INDICADORA
# TABLA 4.2 (RESUMEN DE LA TRANSFORMACIÓN)
# ==========================================================

import numpy as np
import pandas as pd
import geopandas as gpd


# ----------------------------------------------------------
# 1. Verificar los insumos de la sección 4.1
# ----------------------------------------------------------

if "umbral_anomalia" not in globals():
    raise NameError(
        "Primero debes ejecutar la definición del umbral (4.1)."
    )


# ----------------------------------------------------------
# 2. Preparar la capa de muestras
# ----------------------------------------------------------

muestras_indicadora = muestras.copy()

muestras_indicadora = muestras_indicadora[
    muestras_indicadora.geometry.notna()
    & ~muestras_indicadora.geometry.is_empty
].copy()

muestras_indicadora["Cu"] = pd.to_numeric(
    muestras_indicadora["Cu"],
    errors="coerce"
)

muestras_indicadora = muestras_indicadora[
    muestras_indicadora["Cu"].notna()
].copy()


# ----------------------------------------------------------
# 3. Aplicar la transformación indicadora
# ----------------------------------------------------------
# El umbral es inclusivo (>=) por la discretización de la
# variable Cu, según lo definido en la sección 4.1.

muestras_indicadora["INDICADOR"] = (
    muestras_indicadora["Cu"] >= umbral_anomalia
).astype(int)


# ----------------------------------------------------------
# 4. Definir el patrón de anomalías y el fondo
# ----------------------------------------------------------

muestras_anomalias = muestras_indicadora[
    muestras_indicadora["INDICADOR"] == 1
].copy()

muestras_fondo = muestras_indicadora[
    muestras_indicadora["INDICADOR"] == 0
].copy()

numero_total = len(muestras_indicadora)
numero_anomalias = len(muestras_anomalias)
numero_fondo = len(muestras_fondo)

porcentaje_anomalias = numero_anomalias / numero_total * 100

if numero_anomalias < 30:
    print(
        "Advertencia: el patrón de anomalías tiene menos de "
        "30 puntos; considera reducir el umbral."
    )


# ----------------------------------------------------------
# 5. Guardar el patrón de anomalías
# ----------------------------------------------------------

muestras_anomalias.to_file(
    ESTUDIO / "Muestras_Cu_Anomalias.gpkg",
    driver="GPKG"
)


# ----------------------------------------------------------
# 6. Construir la Tabla 4.2
# ----------------------------------------------------------

tabla_4_2 = pd.DataFrame({

    "Parámetro": [
        "Umbral aplicado",
        "Muestras evaluadas",
        "Anomalías (I = 1)",
        "Fondo geoquímico (I = 0)",
        "Porcentaje de anomalías",
        "Rango de Cu en las anomalías"
    ],

    "Valor": [
        f"Cu >= {umbral_anomalia:,.0f} ppm",
        f"{numero_total:,}",
        f"{numero_anomalias:,}",
        f"{numero_fondo:,}",
        f"{porcentaje_anomalias:.2f} %",
        (
            f"{muestras_anomalias['Cu'].min():,.0f} – "
            f"{muestras_anomalias['Cu'].max():,.0f} ppm"
        )
    ]
})


# ----------------------------------------------------------
# 7. Mostrar y guardar la Tabla 4.2
# ----------------------------------------------------------

tabla_4_2_estilizada = (
    tabla_4_2.style
    .hide(axis="index")
    .set_caption(
        "Tabla 4.2. Resumen de la transformación indicadora "
        "y del patrón de anomalías resultante."
    )
    .set_properties(
        subset=["Valor"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_4_2.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_4-2_Transformacion_Indicadora.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_4_2_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 100
# ==========================================================
# ==========================================================
# FIGURA 4.3. DISTRIBUCIÓN ESPACIAL DEL PATRÓN DE ANOMALÍAS
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt

from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.lines import Line2D


# ----------------------------------------------------------
# 1. Verificar los insumos de la sección 4.2
# ----------------------------------------------------------

if "muestras_anomalias" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )

limite_estudio_anomalias = municipios.dissolve()


# ----------------------------------------------------------
# 2. Definir las clases graduadas
# ----------------------------------------------------------
# Las clases corresponden a los valores reportados de la
# variable discretizada.

clases_anomalias = [
    (150, 150, "150 ppm", "#FDB863", 18),
    (200, 200, "200 ppm", "#E66101", 34),
    (300, 300, "300 ppm", "#B2182B", 55),
    (500, 1000, "500 – 1,000 ppm", "#67001F", 90),
]


# ----------------------------------------------------------
# 3. Construir la figura
# ----------------------------------------------------------

figura_anomalias, eje_anomalias = plt.subplots(
    figsize=(11, 11.5)
)

municipios.plot(
    ax=eje_anomalias,
    facecolor="#F2F2F2",
    edgecolor="#BDBDBD",
    linewidth=0.4
)

limite_estudio_anomalias.boundary.plot(
    ax=eje_anomalias,
    color="black",
    linewidth=1.3
)

# Fondo geoquímico
eje_anomalias.scatter(
    muestras_fondo.geometry.x,
    muestras_fondo.geometry.y,
    s=5,
    color="#C9C9C9",
    edgecolor="none",
    zorder=3
)

elementos_leyenda = [
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor="#C9C9C9",
        markersize=5,
        label=(
            f"Fondo geoquímico, Cu < "
            f"{umbral_anomalia:,.0f} ppm "
            f"(n = {len(muestras_fondo):,})"
        )
    )
]

# Anomalías por clase
for valor_min, valor_max, etiqueta, color, tamano in clases_anomalias:

    subconjunto = muestras_anomalias[
        (muestras_anomalias["Cu"] >= valor_min)
        & (muestras_anomalias["Cu"] <= valor_max)
    ]

    eje_anomalias.scatter(
        subconjunto.geometry.x,
        subconjunto.geometry.y,
        s=tamano,
        color=color,
        edgecolor="white",
        linewidth=0.5,
        zorder=5
    )

    elementos_leyenda.append(
        Line2D(
            [0], [0],
            marker="o",
            color="none",
            markerfacecolor=color,
            markeredgecolor="white",
            markersize=np.sqrt(tamano) + 2,
            label=f"{etiqueta} (n = {len(subconjunto)})"
        )
    )


# ----------------------------------------------------------
# 4. Elementos cartográficos
# ----------------------------------------------------------

eje_anomalias.legend(
    handles=elementos_leyenda,
    title="Concentración de cobre",
    loc="upper right",
    fontsize=10,
    title_fontsize=11,
    framealpha=0.95
)

eje_anomalias.add_artist(
    ScaleBar(1, units="m", location="lower left", box_alpha=0.8)
)

eje_anomalias.annotate(
    "N",
    xy=(0.06, 0.87), xytext=(0.06, 0.78),
    xycoords="axes fraction", textcoords="axes fraction",
    ha="center", fontsize=13, fontweight="bold",
    arrowprops=dict(facecolor="black", width=4, headwidth=11)
)

eje_anomalias.text(
    0.98, 0.02,
    "Sistema de referencia\nEPSG:21897",
    transform=eje_anomalias.transAxes,
    ha="right", va="bottom", fontsize=9,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.4"
    )
)

eje_anomalias.set_title(
    (
        "Distribución espacial del patrón de anomalías "
        f"de cobre (n = {len(muestras_anomalias)})"
    ),
    fontsize=15,
    fontweight="bold"
)

eje_anomalias.set_xlabel("Coordenada Este (m)")
eje_anomalias.set_ylabel("Coordenada Norte (m)")
eje_anomalias.ticklabel_format(style="plain")

figura_anomalias.text(
    0.99, 0.005,
    "Fuente: base geoquímica de Cu, cartografía municipal "
    "y elaboración propia.",
    ha="right",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.01, 1, 1])

plt.savefig(
    FIGURAS / "Figura_4-3_Distribucion_Anomalias.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 102
# ==========================================================
# ==========================================================
# FIGURAS 4.3A Y 4.3B
# RELACIÓN ESPACIAL DE LAS ANOMALÍAS DE Cu
# CON LA GEOLOGÍA Y LAS FALLAS
# ==========================================================

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar


# ----------------------------------------------------------
# 1. Verificar insumos requeridos
# ----------------------------------------------------------

variables_requeridas = [
    "muestras_anomalias",
    "muestras_fondo",
    "municipios",
    "geologia",
    "fallas",
    "umbral_anomalia",
    "FIGURAS"
]

variables_faltantes = [
    variable
    for variable in variables_requeridas
    if variable not in globals()
]

if variables_faltantes:
    raise NameError(
        "Faltan las siguientes variables o capas: "
        + ", ".join(variables_faltantes)
    )


# ----------------------------------------------------------
# 2. Preparar copias de trabajo
# ----------------------------------------------------------

municipios_43 = municipios.copy()
geologia_43 = geologia.copy()
fallas_43 = fallas.copy()

anomalias_43 = muestras_anomalias.copy()
fondo_43 = muestras_fondo.copy()


# ----------------------------------------------------------
# 3. Limpiar geometrías
# ----------------------------------------------------------

def limpiar_capa(capa):

    capa = capa[
        capa.geometry.notna()
        & ~capa.geometry.is_empty
    ].copy()

    capa["geometry"] = (
        capa.geometry.make_valid()
    )

    return capa


municipios_43 = limpiar_capa(municipios_43)
geologia_43 = limpiar_capa(geologia_43)
fallas_43 = limpiar_capa(fallas_43)
anomalias_43 = limpiar_capa(anomalias_43)
fondo_43 = limpiar_capa(fondo_43)


# ----------------------------------------------------------
# 4. Homologar sistemas de referencia
# ----------------------------------------------------------

crs_43 = municipios_43.crs

if crs_43 is None:
    raise ValueError(
        "La capa de municipios no tiene CRS definido."
    )

if not crs_43.is_projected:
    raise ValueError(
        "Los mapas deben construirse en un CRS proyectado."
    )

capas_reproyectar = {
    "geologia": geologia_43,
    "fallas": fallas_43,
    "anomalias": anomalias_43,
    "fondo": fondo_43
}

for nombre, capa in capas_reproyectar.items():

    if capa.crs is None:
        raise ValueError(
            f"La capa '{nombre}' no tiene CRS definido."
        )

    if capa.crs != crs_43:

        if nombre == "geologia":
            geologia_43 = capa.to_crs(crs_43)

        elif nombre == "fallas":
            fallas_43 = capa.to_crs(crs_43)

        elif nombre == "anomalias":
            anomalias_43 = capa.to_crs(crs_43)

        elif nombre == "fondo":
            fondo_43 = capa.to_crs(crs_43)


# ----------------------------------------------------------
# 5. Crear el límite del área y recortar capas
# ----------------------------------------------------------

poligono_estudio_43 = (
    municipios_43.geometry.union_all()
)

limite_estudio_43 = gpd.GeoDataFrame(
    geometry=[poligono_estudio_43],
    crs=crs_43
)

geologia_43 = gpd.clip(
    geologia_43,
    limite_estudio_43
)

fallas_43 = gpd.clip(
    fallas_43,
    limite_estudio_43
)


# ----------------------------------------------------------
# 6. Clases de anomalías
# ----------------------------------------------------------

clases_anomalias_43 = [
    (150, 150, "150 ppm", "#FDB863", 18),
    (200, 200, "200 ppm", "#E66101", 34),
    (300, 300, "300 ppm", "#B2182B", 55),
    (500, 1000, "500–1.000 ppm", "#67001F", 90)
]


# ----------------------------------------------------------
# 7. Función para añadir anomalías y construir su leyenda
# ----------------------------------------------------------

def dibujar_anomalias(ax, incluir_fondo=True):

    elementos = []

    if incluir_fondo:

        ax.scatter(
            fondo_43.geometry.x,
            fondo_43.geometry.y,
            s=4,
            color="#C9C9C9",
            edgecolor="none",
            alpha=0.65,
            zorder=5
        )

        elementos.append(
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor="#C9C9C9",
                markeredgecolor="none",
                markersize=5,
                label=(
                    f"Fondo geoquímico, Cu < "
                    f"{umbral_anomalia:,.0f} ppm "
                    f"(n = {len(fondo_43):,})"
                )
            )
        )

    for valor_min, valor_max, etiqueta, color, tamano in (
        clases_anomalias_43
    ):

        subconjunto = anomalias_43[
            (anomalias_43["Cu"] >= valor_min)
            & (anomalias_43["Cu"] <= valor_max)
        ]

        ax.scatter(
            subconjunto.geometry.x,
            subconjunto.geometry.y,
            s=tamano,
            color=color,
            edgecolor="white",
            linewidth=0.5,
            alpha=0.95,
            zorder=8
        )

        elementos.append(
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor=color,
                markeredgecolor="white",
                markersize=np.sqrt(tamano) + 2,
                label=(
                    f"{etiqueta} "
                    f"(n = {len(subconjunto):,})"
                )
            )
        )

    return elementos


# ----------------------------------------------------------
# 8. Función para añadir elementos cartográficos
# ----------------------------------------------------------

def configurar_mapa(
    fig,
    ax,
    titulo,
    fuente
):

    limite_estudio_43.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1.4,
        zorder=10
    )

    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            location="lower left",
            length_fraction=0.20,
            box_alpha=0.90,
            box_color="white",
            color="black",
            font_properties={"size": 8}
        )
    )

    ax.annotate(
        "N",
        xy=(0.06, 0.88),
        xytext=(0.06, 0.79),
        xycoords="axes fraction",
        textcoords="axes fraction",
        ha="center",
        fontsize=13,
        fontweight="bold",
        arrowprops=dict(
            facecolor="black",
            edgecolor="black",
            width=4,
            headwidth=11
        ),
        zorder=15
    )

    ax.text(
        0.98,
        0.02,
        "Sistema de referencia\nEPSG:21897",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        bbox=dict(
            facecolor="white",
            edgecolor="black",
            boxstyle="square,pad=0.35"
        ),
        zorder=15
    )

    ax.set_title(
        titulo,
        fontsize=15,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel(
        "Coordenada Este (m)"
    )

    ax.set_ylabel(
        "Coordenada Norte (m)"
    )

    ax.ticklabel_format(
        style="plain",
        axis="both"
    )

    ax.set_aspect("equal")
    ax.grid(False)

    fig.text(
        0.99,
        0.005,
        fuente,
        ha="right",
        fontsize=8
    )


# ==========================================================
# FIGURA 4.3A. ANOMALÍAS Y UNIDADES LITOLÓGICAS
# ==========================================================

# ----------------------------------------------------------
# 9. Identificar la columna de unidades geológicas
# ----------------------------------------------------------

columnas_geologia = [
    "ENTITY",
    "UNIDAD_DES",
    "DESCRIPTIO",
    "DESCRIPCIO"
]

columna_geologia_43 = next(
    (
        columna
        for columna in columnas_geologia
        if columna in geologia_43.columns
    ),
    None
)

if columna_geologia_43 is None:
    raise ValueError(
        "No se encontró una columna para identificar "
        "las unidades geológicas.\n"
        f"Columnas disponibles: {geologia_43.columns.tolist()}"
    )


# ----------------------------------------------------------
# 10. Preparar categorías litológicas
# ----------------------------------------------------------

geologia_43["UNIDAD_MAPA"] = (
    geologia_43[columna_geologia_43]
    .fillna("Sin identificación")
    .astype(str)
    .str.strip()
)

unidades_43 = sorted(
    geologia_43["UNIDAD_MAPA"]
    .unique()
    .tolist()
)

mapa_colores = plt.get_cmap(
    "tab20",
    max(len(unidades_43), 1)
)

colores_unidades_43 = {
    unidad: mapa_colores(indice)
    for indice, unidad in enumerate(unidades_43)
}


# ----------------------------------------------------------
# 11. Crear el mapa litológico
# ----------------------------------------------------------

figura_43a, eje_43a = plt.subplots(
    figsize=(14, 11.5)
)

for unidad in unidades_43:

    geologia_43[
        geologia_43["UNIDAD_MAPA"] == unidad
    ].plot(
        ax=eje_43a,
        facecolor=colores_unidades_43[unidad],
        edgecolor="#777777",
        linewidth=0.30,
        alpha=0.72,
        zorder=1
    )

municipios_43.boundary.plot(
    ax=eje_43a,
    color="#777777",
    linewidth=0.35,
    alpha=0.55,
    zorder=3
)

elementos_anomalias_43a = dibujar_anomalias(
    eje_43a,
    incluir_fondo=False
)


# ----------------------------------------------------------
# 12. Leyendas de la Figura 4.3A
# ----------------------------------------------------------

elementos_geologia_43a = [
    Patch(
        facecolor=colores_unidades_43[unidad],
        edgecolor="#777777",
        label=unidad
    )
    for unidad in unidades_43
]

leyenda_geologia_43a = eje_43a.legend(
    handles=elementos_geologia_43a,
    title="Unidades litológicas",
    loc="center left",
    bbox_to_anchor=(1.01, 0.50),
    fontsize=7,
    title_fontsize=9,
    framealpha=0.96
)

eje_43a.add_artist(
    leyenda_geologia_43a
)

eje_43a.legend(
    handles=elementos_anomalias_43a,
    title="Anomalías de cobre",
    loc="upper right",
    fontsize=9,
    title_fontsize=10,
    framealpha=0.96
)


# ----------------------------------------------------------
# 13. Configurar y guardar la Figura 4.3A
# ----------------------------------------------------------

configurar_mapa(
    figura_43a,
    eje_43a,
    (
        "Distribución de las anomalías de cobre "
        "sobre las unidades litológicas"
    ),
    (
        "Fuente: base geoquímica de Cu, cartografía geológica, "
        "cartografía municipal y elaboración propia."
    )
)

figura_43a.subplots_adjust(
    left=0.08,
    right=0.78,
    bottom=0.08,
    top=0.96
)

ruta_figura_43a = (
    FIGURAS
    / "Figura_4-3A_Anomalias_Unidades_Litologicas.png"
)

figura_43a.savefig(
    ruta_figura_43a,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()


# ==========================================================
# FIGURA 4.3B. ANOMALÍAS Y FALLAS GEOLÓGICAS
# ==========================================================

# ----------------------------------------------------------
# 14. Crear el mapa estructural
# ----------------------------------------------------------

figura_43b, eje_43b = plt.subplots(
    figsize=(11, 11.5)
)

municipios_43.plot(
    ax=eje_43b,
    facecolor="#F4F4F1",
    edgecolor="#BDBDBD",
    linewidth=0.40,
    zorder=1
)

fallas_43.plot(
    ax=eje_43b,
    color="#202020",
    linewidth=1.15,
    alpha=0.85,
    zorder=4
)

elementos_anomalias_43b = dibujar_anomalias(
    eje_43b,
    incluir_fondo=False
)

# ----------------------------------------------------------
# 14.1 Añadir nombres de las fallas principales
# ----------------------------------------------------------

import matplotlib.patheffects as pe


# Posibles columnas donde puede estar el nombre de la falla
columnas_nombre_falla = [
    "NombreFall",
    "NOMBRE_FAL",
    "NOMBRE",
    "Nombre",
    "FALLA",
    "NOM_FALLA",
    "NAME"
]

columna_nombre_falla = next(
    (
        columna
        for columna in columnas_nombre_falla
        if columna in fallas_43.columns
    ),
    None
)

if columna_nombre_falla is None:

    print(
        "No se encontró automáticamente una columna "
        "con el nombre de las fallas."
    )

    print(
        "Columnas disponibles:",
        fallas_43.columns.tolist()
    )

else:

    # Limpiar nombres
    fallas_43["NOMBRE_FALLA_MAPA"] = (
        fallas_43[columna_nombre_falla]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Excluir registros sin nombre útil
    nombres_no_validos = [
        "",
        "NONE",
        "NAN",
        "SIN NOMBRE",
        "NO IDENTIFICADA",
        "NO DEFINIDA"
    ]

    fallas_principales_43 = fallas_43[
        ~fallas_43["NOMBRE_FALLA_MAPA"]
        .str.upper()
        .isin(nombres_no_validos)
    ].copy()

    # Evitar repetir muchas veces el mismo nombre
    fallas_principales_43 = (
        fallas_principales_43
        .sort_values(
            by="NOMBRE_FALLA_MAPA"
        )
        .drop_duplicates(
            subset="NOMBRE_FALLA_MAPA"
        )
    )

    # Añadir etiquetas
    for _, fila in fallas_principales_43.iterrows():

        geometria = fila.geometry
        nombre_falla = fila["NOMBRE_FALLA_MAPA"]

        if geometria is None or geometria.is_empty:
            continue

        # Punto ubicado aproximadamente a la mitad de la línea
        punto_etiqueta = geometria.interpolate(
            0.5,
            normalized=True
        )

        texto_falla = eje_43b.text(
            punto_etiqueta.x,
            punto_etiqueta.y,
            nombre_falla,
            fontsize=6.5,
            color="#3A0000",
            fontstyle="italic",
            ha="center",
            va="center",
            rotation=0,
            zorder=12
        )

        # Contorno blanco para facilitar la lectura
        texto_falla.set_path_effects([
            pe.withStroke(
                linewidth=2.2,
                foreground="white"
            )
        ])

    print(
        f"Nombres de fallas añadidos: "
        f"{len(fallas_principales_43)}"
    )
# ----------------------------------------------------------
# 15. Crear leyenda de la Figura 4.3B
# ----------------------------------------------------------

elementos_estructura_43b = [
    Line2D(
        [0],
        [0],
        color="#202020",
        linewidth=1.5,
        label="Fallas geológicas"
    )
]

elementos_leyenda_43b = (
    elementos_estructura_43b
    + elementos_anomalias_43b
)

eje_43b.legend(
    handles=elementos_leyenda_43b,
    title="Información estructural y geoquímica",
    loc="upper right",
    fontsize=9,
    title_fontsize=10,
    framealpha=0.96
)


# ----------------------------------------------------------
# 16. Configurar y guardar la Figura 4.3B
# ----------------------------------------------------------

configurar_mapa(
    figura_43b,
    eje_43b,
    (
        "Distribución de las anomalías de cobre "
        "respecto a las fallas geológicas"
    ),
    (
        "Fuente: base geoquímica de Cu, cartografía de fallas, "
        "cartografía municipal y elaboración propia."
    )
)

plt.tight_layout(
    rect=[0, 0.01, 1, 1]
)

ruta_figura_43b = (
    FIGURAS
    / "Figura_4-3B_Anomalias_Fallas_Geologicas.png"
)

figura_43b.savefig(
    ruta_figura_43b,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()


# ----------------------------------------------------------
# 17. Confirmar resultados
# ----------------------------------------------------------

print("=" * 76)
print("FIGURAS COMPLEMENTARIAS DE LA SECCIÓN 4.3 GENERADAS")
print("=" * 76)

print(
    f"Anomalías representadas: "
    f"{len(anomalias_43):,}"
)

print(
    f"Unidades litológicas: "
    f"{len(unidades_43):,}"
)

print(
    f"Fallas representadas: "
    f"{len(fallas_43):,}"
)

print("-" * 76)
print(f"Figura 4.3A: {ruta_figura_43a}")
print(f"Figura 4.3B: {ruta_figura_43b}")
print("=" * 76)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 104
# ==========================================================
# ==========================================================
# TABLA 11. PARÁMETROS DE LA ESTIMACIÓN KERNEL
# DEL PATRÓN DE ANOMALÍAS
# ==========================================================

import numpy as np
import pandas as pd

from scipy.stats import gaussian_kde


# ----------------------------------------------------------
# 1. Verificar los insumos de la sección 4.2
# ----------------------------------------------------------

if "muestras_anomalias" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )


# ----------------------------------------------------------
# 2. Preparar la capa de anomalías
# ----------------------------------------------------------

anomalias_kernel = muestras_anomalias.copy()

anomalias_kernel = anomalias_kernel[
    anomalias_kernel.geometry.notna()
    & ~anomalias_kernel.geometry.is_empty
].copy()

municipios_kernel_an = municipios.copy()

poligono_kernel_an = (
    municipios_kernel_an.geometry.union_all()
)


# ----------------------------------------------------------
# 3. Extraer coordenadas válidas
# ----------------------------------------------------------

x_kernel_an = anomalias_kernel.geometry.x.to_numpy()
y_kernel_an = anomalias_kernel.geometry.y.to_numpy()

mascara_kernel_an = (
    np.isfinite(x_kernel_an)
    & np.isfinite(y_kernel_an)
)

x_kernel_an = x_kernel_an[mascara_kernel_an]
y_kernel_an = y_kernel_an[mascara_kernel_an]

numero_anomalias_kernel = len(x_kernel_an)

if numero_anomalias_kernel < 3:
    raise ValueError(
        "Se requieren al menos tres anomalías válidas "
        "para calcular la densidad Kernel."
    )

coordenadas_kernel_an = np.vstack([
    x_kernel_an,
    y_kernel_an
])


# ----------------------------------------------------------
# 4. Ajustar el modelo Kernel
# ----------------------------------------------------------
# Kernel gaussiano y regla de Scott, en consistencia con
# la sección 3.4.

modelo_kernel_an = gaussian_kde(
    coordenadas_kernel_an,
    bw_method="scott"
)

factor_banda_an = float(modelo_kernel_an.factor)

banda_este_an = factor_banda_an * np.std(x_kernel_an, ddof=1)
banda_norte_an = factor_banda_an * np.std(y_kernel_an, ddof=1)

banda_promedio_an = np.sqrt(banda_este_an * banda_norte_an)


# ----------------------------------------------------------
# 5. Definir la resolución de la malla
# ----------------------------------------------------------

RESOLUCION_KERNEL_AN = 300

xmin_an, ymin_an, xmax_an, ymax_an = (
    municipios_kernel_an.total_bounds
)

tamano_celda_an = (
    ((xmax_an - xmin_an) / (RESOLUCION_KERNEL_AN - 1))
    + ((ymax_an - ymin_an) / (RESOLUCION_KERNEL_AN - 1))
) / 2


# ----------------------------------------------------------
# 6. Construir la Tabla 11
# ----------------------------------------------------------

tabla_11 = pd.DataFrame({

    "Parámetro": [
        "Número de anomalías",
        "Tipo de kernel",
        "Método del ancho de banda",
        "Factor de Scott",
        "Ancho de banda Este",
        "Ancho de banda Norte",
        "Ancho de banda promedio",
        "Resolución de la malla",
        "Tamaño de celda promedio"
    ],

    "Valor": [
        f"{numero_anomalias_kernel:,}",
        "Gaussiano",
        "Regla de Scott",
        f"{factor_banda_an:.4f}",
        f"{banda_este_an:,.0f} m",
        f"{banda_norte_an:,.0f} m",
        f"{banda_promedio_an:,.0f} m",
        f"{RESOLUCION_KERNEL_AN} x {RESOLUCION_KERNEL_AN}",
        f"{tamano_celda_an:,.0f} m"
    ]
})


# ----------------------------------------------------------
# 7. Mostrar y guardar la Tabla 11
# ----------------------------------------------------------

tabla_11_estilizada = (
    tabla_11.style
    .hide(axis="index")
    .set_caption(
        "Tabla 11. Parámetros de la estimación Kernel del "
        "patrón de anomalías de cobre."
    )
    .set_properties(
        subset=["Valor"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_11.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_11_Parametros_Kernel_Anomalias.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_11_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 105
# ==========================================================
# ==========================================================
# FIGURA 12. DENSIDAD KERNEL DEL PATRÓN DE ANOMALÍAS
# ==========================================================

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar


# ----------------------------------------------------------
# 1. Verificar los insumos de la Tabla 11
# ----------------------------------------------------------

variables_requeridas = [
    "modelo_kernel_an", "x_kernel_an", "y_kernel_an",
    "poligono_kernel_an", "municipios_kernel_an",
    "RESOLUCION_KERNEL_AN"
]

variables_faltantes = [
    v for v in variables_requeridas if v not in globals()
]

if variables_faltantes:
    raise NameError(
        "Primero debes ejecutar la celda de la Tabla 11. "
        f"Variables faltantes: {variables_faltantes}"
    )


# ----------------------------------------------------------
# 2. Crear la malla de evaluación
# ----------------------------------------------------------

xmin_an, ymin_an, xmax_an, ymax_an = (
    municipios_kernel_an.total_bounds
)

x_malla_an = np.linspace(xmin_an, xmax_an, RESOLUCION_KERNEL_AN)
y_malla_an = np.linspace(ymin_an, ymax_an, RESOLUCION_KERNEL_AN)

xx_an, yy_an = np.meshgrid(x_malla_an, y_malla_an)

posiciones_an = np.vstack([xx_an.ravel(), yy_an.ravel()])


# ----------------------------------------------------------
# 3. Evaluar y recortar la densidad
# ----------------------------------------------------------

densidad_an = modelo_kernel_an(posiciones_an).reshape(
    xx_an.shape
)

try:

    from shapely import intersects_xy

    mascara_poligono_an = intersects_xy(
        poligono_kernel_an, xx_an, yy_an
    )

except ImportError:

    puntos_malla_an = gpd.GeoSeries(
        gpd.points_from_xy(xx_an.ravel(), yy_an.ravel()),
        crs=municipios_kernel_an.crs
    )

    mascara_poligono_an = (
        puntos_malla_an.within(poligono_kernel_an)
        | puntos_malla_an.touches(poligono_kernel_an)
    ).to_numpy().reshape(xx_an.shape)

densidad_an_recortada = np.where(
    mascara_poligono_an, densidad_an, np.nan
)


# ----------------------------------------------------------
# 4. Normalizar entre 0 y 1
# ----------------------------------------------------------
# La normalización facilita la comparación visual y no
# representa concentraciones de cobre.

densidad_an_maxima = np.nanmax(densidad_an_recortada)

if not np.isfinite(densidad_an_maxima) or densidad_an_maxima <= 0:
    raise ValueError(
        "No fue posible obtener una densidad Kernel válida."
    )

densidad_an_relativa = (
    densidad_an_recortada / densidad_an_maxima
)


# ----------------------------------------------------------
# 5. Construir la figura
# ----------------------------------------------------------

figura_kernel_an, eje_kernel_an = plt.subplots(
    figsize=(11, 11.5)
)

superficie = eje_kernel_an.imshow(
    densidad_an_relativa,
    extent=[xmin_an, xmax_an, ymin_an, ymax_an],
    origin="lower",
    cmap="magma",
    alpha=0.85,
    zorder=2
)

contornos = eje_kernel_an.contour(
    xx_an, yy_an, densidad_an_relativa,
    levels=[0.2, 0.4, 0.6, 0.8],
    colors="white",
    linewidths=0.7,
    alpha=0.8,
    zorder=3
)

municipios_kernel_an.boundary.plot(
    ax=eje_kernel_an,
    color="#9E9E9E",
    linewidth=0.4,
    zorder=4
)

municipios_kernel_an.dissolve().boundary.plot(
    ax=eje_kernel_an,
    color="black",
    linewidth=1.3,
    zorder=5
)

eje_kernel_an.scatter(
    x_kernel_an, y_kernel_an,
    s=10,
    color="#00E5FF",
    edgecolor="black",
    linewidth=0.3,
    zorder=6
)


# ----------------------------------------------------------
# 6. Elementos cartográficos
# ----------------------------------------------------------

barra_color = plt.colorbar(
    superficie,
    ax=eje_kernel_an,
    shrink=0.65,
    pad=0.02
)

barra_color.set_label(
    "Densidad Kernel relativa (0 – 1)",
    fontsize=11
)

eje_kernel_an.legend(
    handles=[
        Line2D(
            [0], [0],
            marker="o", color="none",
            markerfacecolor="#00E5FF",
            markeredgecolor="black",
            markersize=6,
            label=(
                "Anomalías de Cu "
                f"(n = {len(x_kernel_an)})"
            )
        )
    ],
    loc="upper right",
    fontsize=10,
    framealpha=0.95
)

eje_kernel_an.add_artist(
    ScaleBar(1, units="m", location="lower left", box_alpha=0.8)
)

eje_kernel_an.annotate(
    "N",
    xy=(0.06, 0.87), xytext=(0.06, 0.78),
    xycoords="axes fraction", textcoords="axes fraction",
    ha="center", fontsize=13, fontweight="bold",
    arrowprops=dict(facecolor="black", width=4, headwidth=11)
)

eje_kernel_an.text(
    0.98, 0.02,
    "Sistema de referencia\nEPSG:21897",
    transform=eje_kernel_an.transAxes,
    ha="right", va="bottom", fontsize=9,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.4"
    )
)

eje_kernel_an.set_title(
    "Densidad Kernel del patrón de anomalías de cobre",
    fontsize=15, fontweight="bold"
)
eje_kernel_an.set_xlabel("Coordenada Este (m)")
eje_kernel_an.set_ylabel("Coordenada Norte (m)")
eje_kernel_an.ticklabel_format(style="plain")

figura_kernel_an.text(
    0.99, 0.005,
    "Fuente: base geoquímica de Cu, cartografía municipal "
    "y elaboración propia.",
    ha="right", fontsize=9
)

plt.tight_layout(rect=[0, 0.01, 1, 1])

plt.savefig(
    FIGURAS / "Figura_12_Densidad_Kernel_Anomalias.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 108
# ==========================================================
# ==========================================================
# TABLA 12. ANÁLISIS DEL VECINO MÁS CERCANO
# DEL PATRÓN DE ANOMALÍAS
# ==========================================================

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from scipy.stats import norm


# ----------------------------------------------------------
# 1. Verificar los insumos de la sección 4.2
# ----------------------------------------------------------

if "muestras_anomalias" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )


# ----------------------------------------------------------
# 2. Preparar la capa y extraer coordenadas
# ----------------------------------------------------------

anomalias_ann = muestras_anomalias.copy()

anomalias_ann = anomalias_ann[
    anomalias_ann.geometry.notna()
    & ~anomalias_ann.geometry.is_empty
].copy()

poligono_ann_an = municipios.geometry.union_all()

coordenadas_ann_an = np.column_stack([
    anomalias_ann.geometry.x.to_numpy(),
    anomalias_ann.geometry.y.to_numpy()
])

mascara_ann_an = np.isfinite(
    coordenadas_ann_an
).all(axis=1)

coordenadas_ann_an = coordenadas_ann_an[mascara_ann_an]

numero_anomalias_ann = len(coordenadas_ann_an)

if numero_anomalias_ann < 2:
    raise ValueError(
        "Se requieren al menos dos anomalías válidas."
    )


# ----------------------------------------------------------
# 3. Calcular la distancia al vecino más cercano
# ----------------------------------------------------------
# Se solicitan dos vecinos porque el primero corresponde
# al mismo punto, cuya distancia es igual a cero.

modelo_vecinos_an = NearestNeighbors(
    n_neighbors=2,
    metric="euclidean"
)

modelo_vecinos_an.fit(coordenadas_ann_an)

distancias_an, _ = modelo_vecinos_an.kneighbors(
    coordenadas_ann_an
)

distancia_observada_an = float(
    np.mean(distancias_an[:, 1])
)


# ----------------------------------------------------------
# 4. Calcular la distancia esperada bajo CSR
# ----------------------------------------------------------

area_m2_an = float(poligono_ann_an.area)

densidad_m2_an = numero_anomalias_ann / area_m2_an

distancia_esperada_an = 0.5 / np.sqrt(densidad_m2_an)


# ----------------------------------------------------------
# 5. Índice R de Clark y Evans y significancia
# ----------------------------------------------------------

indice_r_an = (
    distancia_observada_an / distancia_esperada_an
)

error_estandar_an = (
    0.26136
    / np.sqrt(numero_anomalias_ann * densidad_m2_an)
)

z_an = (
    (distancia_observada_an - distancia_esperada_an)
    / error_estandar_an
)

p_valor_an = 2 * (1 - norm.cdf(abs(z_an)))

if indice_r_an < 1 and p_valor_an < 0.05:
    interpretacion_ann_an = (
        "Patrón significativamente agrupado (R < 1)"
    )
elif indice_r_an > 1 and p_valor_an < 0.05:
    interpretacion_ann_an = (
        "Patrón significativamente regular (R > 1)"
    )
else:
    interpretacion_ann_an = (
        "Patrón compatible con la aleatoriedad espacial"
    )


# ----------------------------------------------------------
# 6. Construir la Tabla 12
# ----------------------------------------------------------

tabla_12 = pd.DataFrame({

    "Parámetro": [
        "Número de anomalías",
        "Área de análisis",
        "Densidad de anomalías",
        "Distancia media observada",
        "Distancia media esperada (CSR)",
        "Índice R de Clark y Evans",
        "Estadístico Z",
        "Valor p",
        "Interpretación (α = 0.05)"
    ],

    "Valor": [
        f"{numero_anomalias_ann:,}",
        f"{area_m2_an / 1e6:,.1f} km²",
        f"{densidad_m2_an * 1e6:.4f} anomalías/km²",
        f"{distancia_observada_an:,.2f} m",
        f"{distancia_esperada_an:,.2f} m",
        f"{indice_r_an:.4f}",
        f"{z_an:.2f}",
        f"{p_valor_an:.3g}",
        interpretacion_ann_an
    ]
})


# ----------------------------------------------------------
# 7. Mostrar y guardar la Tabla 12
# ----------------------------------------------------------

tabla_12_estilizada = (
    tabla_12.style
    .hide(axis="index")
    .set_caption(
        "Tabla 12. Análisis del vecino más cercano del "
        "patrón de anomalías de cobre."
    )
    .set_properties(
        subset=["Valor"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_12.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_12_Vecino_Cercano_Anomalias.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_12_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 111
# ==========================================================
# ==========================================================
# TABLA 13. CONTEO POR CUADRANTES DEL PATRÓN DE ANOMALÍAS
# (PRUEBA DE MONTE CARLO CONDICIONADA AL ÁREA DE ESTUDIO)
# ==========================================================

import numpy as np
import pandas as pd

from pointpats import random as pp_random


# ----------------------------------------------------------
# 1. Parámetros del análisis
# ----------------------------------------------------------
# Nota: con 999 simulaciones la celda tarda entre
# 1 y 3 minutos.

NX_CUADRANTES = 4
NY_CUADRANTES = 4
N_SIMULACIONES_CUADRANTES = 999
SEMILLA_CUADRANTES = 42


# ----------------------------------------------------------
# 2. Verificar los insumos
# ----------------------------------------------------------

if "muestras_anomalias" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )

poligono_cuadrantes = municipios.geometry.union_all()


# ----------------------------------------------------------
# 3. Extraer coordenadas válidas
# ----------------------------------------------------------

coordenadas_cuadrantes = np.column_stack([
    muestras_anomalias.geometry.x.to_numpy(),
    muestras_anomalias.geometry.y.to_numpy()
])

mascara_cuadrantes = np.isfinite(
    coordenadas_cuadrantes
).all(axis=1)

coordenadas_cuadrantes = coordenadas_cuadrantes[
    mascara_cuadrantes
]

numero_anomalias_cuadrantes = len(coordenadas_cuadrantes)

if numero_anomalias_cuadrantes < 30:
    raise ValueError(
        "Se requieren al menos 30 anomalías para que el "
        "conteo por cuadrantes sea interpretable."
    )


# ----------------------------------------------------------
# 4. Definir la malla fija de cuadrantes
# ----------------------------------------------------------
# La malla se construye sobre el rectángulo envolvente del
# área de estudio y es la misma para el patrón observado y
# para todas las simulaciones.

xmin_area, ymin_area, xmax_area, ymax_area = (
    municipios.total_bounds
)

bordes_x = np.linspace(
    xmin_area, xmax_area, NX_CUADRANTES + 1
)

bordes_y = np.linspace(
    ymin_area, ymax_area, NY_CUADRANTES + 1
)


def contar_por_cuadrantes(coordenadas):
    """Cuenta los puntos por celda sobre la malla fija."""
    conteos, _, _ = np.histogram2d(
        coordenadas[:, 0],
        coordenadas[:, 1],
        bins=[bordes_x, bordes_y]
    )
    return conteos


def chi2_cuadrantes(conteos, numero_puntos):
    """Chi-cuadrado frente a conteos uniformes."""
    esperado = numero_puntos / conteos.size
    return float(
        ((conteos - esperado) ** 2 / esperado).sum()
    )


# ----------------------------------------------------------
# 5. Estadístico del patrón observado
# ----------------------------------------------------------

conteos_anomalias_cuadrantes = contar_por_cuadrantes(
    coordenadas_cuadrantes
)

chi2_observado = chi2_cuadrantes(
    conteos_anomalias_cuadrantes,
    numero_anomalias_cuadrantes
)


# ----------------------------------------------------------
# 6. Simulaciones de Monte Carlo bajo CSR
# ----------------------------------------------------------

np.random.seed(SEMILLA_CUADRANTES)

chi2_simulados = np.empty(N_SIMULACIONES_CUADRANTES)

for indice_simulacion in range(N_SIMULACIONES_CUADRANTES):

    patron_simulado = pp_random.poisson(
        poligono_cuadrantes,
        size=numero_anomalias_cuadrantes
    )

    chi2_simulados[indice_simulacion] = chi2_cuadrantes(
        contar_por_cuadrantes(patron_simulado),
        numero_anomalias_cuadrantes
    )

# Se conserva una realización para la Figura 13
coordenadas_csr = pp_random.poisson(
    poligono_cuadrantes,
    size=numero_anomalias_cuadrantes
)

conteos_csr = contar_por_cuadrantes(coordenadas_csr)

chi2_csr_ejemplo = chi2_cuadrantes(
    conteos_csr,
    numero_anomalias_cuadrantes
)


# ----------------------------------------------------------
# 7. Pseudo valor p de Monte Carlo
# ----------------------------------------------------------

pseudo_p = (
    (1 + np.sum(chi2_simulados >= chi2_observado))
    / (1 + N_SIMULACIONES_CUADRANTES)
)

if pseudo_p < 0.05:
    interpretacion_cuadrantes = (
        "Se rechaza la CSR: las anomalías están "
        "significativamente concentradas"
    )
else:
    interpretacion_cuadrantes = (
        "No se rechaza la CSR: el patrón es compatible "
        "con la aleatoriedad espacial"
    )


# ----------------------------------------------------------
# 8. Construir la Tabla 13
# ----------------------------------------------------------

tabla_13 = pd.DataFrame({

    "Parámetro": [
        "Número de anomalías",
        "Malla de cuadrantes",
        "Chi-cuadrado observado",
        "Chi-cuadrado simulado (media)",
        "Chi-cuadrado simulado (percentil 95)",
        "Chi-cuadrado simulado (máximo)",
        "Número de simulaciones CSR",
        "Pseudo valor p",
        "Interpretación (α = 0.05)"
    ],

    "Valor": [
        f"{numero_anomalias_cuadrantes:,}",
        f"{NX_CUADRANTES} x {NY_CUADRANTES}",
        f"{chi2_observado:,.2f}",
        f"{chi2_simulados.mean():,.2f}",
        f"{np.percentile(chi2_simulados, 95):,.2f}",
        f"{chi2_simulados.max():,.2f}",
        f"{N_SIMULACIONES_CUADRANTES:,}",
        f"{pseudo_p:.4f}",
        interpretacion_cuadrantes
    ]
})


# ----------------------------------------------------------
# 9. Mostrar y guardar la Tabla 13
# ----------------------------------------------------------

tabla_13_estilizada = (
    tabla_13.style
    .hide(axis="index")
    .set_caption(
        "Tabla 13. Conteo por cuadrantes del patrón de "
        "anomalías de cobre: prueba de Monte Carlo frente "
        "a la aleatoriedad espacial completa."
    )
    .set_properties(
        subset=["Valor"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_13.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_13_Conteo_Cuadrantes_Anomalias.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_13_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 112
# ==========================================================
# ==========================================================
# FIGURA 13. CONTEO POR CUADRANTES: OBSERVADO, SIMULADO
# Y DISTRIBUCIÓN DE MONTE CARLO
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt

from matplotlib_scalebar.scalebar import ScaleBar


# ----------------------------------------------------------
# 1. Verificar los insumos de la Tabla 13
# ----------------------------------------------------------

variables_requeridas = [
    "coordenadas_cuadrantes", "conteos_anomalias_cuadrantes",
    "coordenadas_csr", "conteos_csr",
    "chi2_observado", "chi2_csr_ejemplo",
    "chi2_simulados", "pseudo_p",
    "bordes_x", "bordes_y"
]

variables_faltantes = [
    v for v in variables_requeridas if v not in globals()
]

if variables_faltantes:
    raise NameError(
        "Primero debes ejecutar la celda de la Tabla 13. "
        f"Variables faltantes: {variables_faltantes}"
    )

limite_estudio_cuadrantes = municipios.dissolve()


# ----------------------------------------------------------
# 2. Función para dibujar los paneles cartográficos
# ----------------------------------------------------------

def dibujar_panel(ax, coordenadas, conteos, titulo,
                  color_puntos):
    """Dibuja municipios, límite, puntos, malla y conteos."""

    municipios.plot(
        ax=ax,
        facecolor="#F2F2F2",
        edgecolor="#BDBDBD",
        linewidth=0.4
    )

    limite_estudio_cuadrantes.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1.2
    )

    ax.scatter(
        coordenadas[:, 0],
        coordenadas[:, 1],
        s=13,
        color=color_puntos,
        edgecolor="white",
        linewidth=0.25,
        zorder=5
    )

    for borde in bordes_x:
        ax.plot(
            [borde, borde],
            [bordes_y[0], bordes_y[-1]],
            color="#B22222", linewidth=0.9, zorder=4
        )

    for borde in bordes_y:
        ax.plot(
            [bordes_x[0], bordes_x[-1]],
            [borde, borde],
            color="#B22222", linewidth=0.9, zorder=4
        )

    for i in range(len(bordes_x) - 1):
        for j in range(len(bordes_y) - 1):
            ax.text(
                (bordes_x[i] + bordes_x[i + 1]) / 2,
                (bordes_y[j] + bordes_y[j + 1]) / 2,
                f"{int(conteos[i, j])}",
                ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="#B22222", zorder=6,
                bbox=dict(
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.7,
                    pad=1.5
                )
            )

    ax.set_title(titulo, fontsize=12.5, fontweight="bold")
    ax.set_xlabel("Coordenada Este (m)")
    ax.ticklabel_format(style="plain")
    ax.tick_params(labelsize=8.5)


# ----------------------------------------------------------
# 3. Construir la figura
# ----------------------------------------------------------

figura_cuadrantes = plt.figure(figsize=(18, 8.5))

rejilla = figura_cuadrantes.add_gridspec(
    1, 3, width_ratios=[1, 1, 0.95], wspace=0.16
)

eje_observado = figura_cuadrantes.add_subplot(rejilla[0])
eje_simulado = figura_cuadrantes.add_subplot(
    rejilla[1], sharex=eje_observado, sharey=eje_observado
)
eje_montecarlo = figura_cuadrantes.add_subplot(rejilla[2])

dibujar_panel(
    eje_observado,
    coordenadas_cuadrantes,
    conteos_anomalias_cuadrantes,
    (
        "Anomalías de Cu observadas "
        f"(n = {len(coordenadas_cuadrantes)})\n"
        f"$\\chi^2$ = {chi2_observado:,.1f}"
    ),
    "#4B0082"
)

dibujar_panel(
    eje_simulado,
    coordenadas_csr,
    conteos_csr,
    (
        "Realización CSR dentro del área "
        f"(n = {len(coordenadas_csr)})\n"
        f"$\\chi^2$ = {chi2_csr_ejemplo:,.1f}"
    ),
    "#C0392B"
)

eje_observado.set_ylabel("Coordenada Norte (m)")
plt.setp(eje_simulado.get_yticklabels(), visible=False)


# ----------------------------------------------------------
# 4. Panel de la distribución de Monte Carlo
# ----------------------------------------------------------

eje_montecarlo.hist(
    chi2_simulados,
    bins=30,
    color="#9FB6CD",
    edgecolor="#5A7A9B",
    linewidth=0.5
)

eje_montecarlo.axvline(
    chi2_observado,
    color="#4B0082",
    linewidth=2.5,
    linestyle="--"
)

eje_montecarlo.text(
    chi2_observado,
    eje_montecarlo.get_ylim()[1] * 0.95,
    f"  $\\chi^2$ observado = {chi2_observado:,.1f}",
    color="#4B0082",
    fontsize=11,
    fontweight="bold",
    ha="left",
    va="top",
    rotation=90
)

eje_montecarlo.set_title(
    (
        "Distribución Monte Carlo del $\\chi^2$\n"
        f"({len(chi2_simulados)} simulaciones CSR · "
        f"pseudo p = {pseudo_p:.3f})"
    ),
    fontsize=12.5,
    fontweight="bold"
)

eje_montecarlo.set_xlabel("Estadístico $\\chi^2$")
eje_montecarlo.set_ylabel("Frecuencia")
eje_montecarlo.grid(alpha=0.3)


# ----------------------------------------------------------
# 5. Elementos cartográficos
# ----------------------------------------------------------

eje_observado.add_artist(
    ScaleBar(1, units="m", location="lower left",
             box_alpha=0.8)
)

eje_simulado.annotate(
    "N",
    xy=(0.95, 0.93), xytext=(0.95, 0.83),
    xycoords="axes fraction", textcoords="axes fraction",
    ha="center", fontsize=13, fontweight="bold",
    arrowprops=dict(facecolor="black", width=4, headwidth=11)
)

eje_simulado.text(
    0.98, 0.02,
    "Sistema de referencia\nEPSG:21897",
    transform=eje_simulado.transAxes,
    ha="right", va="bottom", fontsize=9,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.4"
    )
)

figura_cuadrantes.suptitle(
    "Conteo por cuadrantes del patrón de anomalías de "
    "cobre (Cu ≥ 150 ppm)",
    fontsize=16,
    fontweight="bold"
)

figura_cuadrantes.text(
    0.99, 0.01,
    "Fuente: base geoquímica de Cu, cartografía municipal "
    "y elaboración propia.",
    ha="right", fontsize=9
)


# ----------------------------------------------------------
# 6. Guardar la Figura 13
# ----------------------------------------------------------

plt.savefig(
    FIGURAS / "Figura_13_Conteo_Cuadrantes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 115
# ==========================================================
# ==========================================================
# TABLA 14 Y FIGURA 14. FUNCIONES G, F Y K DEL PATRÓN
# DE ANOMALÍAS FRENTE A LA ALEATORIEDAD ESPACIAL COMPLETA
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pointpats.distance_statistics import (
    g_test,
    f_test,
    k_test
)


# ----------------------------------------------------------
# 1. Parámetros del análisis
# ----------------------------------------------------------
# Nota: con 199 simulaciones por función, la celda tarda
# entre 1 y 2 minutos.

N_SIMULACIONES_GFK = 199
PUNTOS_SOPORTE = 20
SEMILLA_GFK = 42


# ----------------------------------------------------------
# 2. Verificar los insumos
# ----------------------------------------------------------

if "muestras_anomalias" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )

poligono_gfk = municipios.geometry.union_all()

coordenadas_gfk = np.column_stack([
    muestras_anomalias.geometry.x.to_numpy(),
    muestras_anomalias.geometry.y.to_numpy()
])

mascara_gfk = np.isfinite(coordenadas_gfk).all(axis=1)
coordenadas_gfk = coordenadas_gfk[mascara_gfk]


# ----------------------------------------------------------
# 3. Calcular las tres funciones con simulaciones CSR
# ----------------------------------------------------------
# El argumento hull restringe las simulaciones al polígono
# del área de estudio.

np.random.seed(SEMILLA_GFK)

resultado_g = g_test(
    coordenadas_gfk,
    support=PUNTOS_SOPORTE,
    keep_simulations=True,
    n_simulations=N_SIMULACIONES_GFK,
    hull=poligono_gfk
)

resultado_f = f_test(
    coordenadas_gfk,
    support=PUNTOS_SOPORTE,
    keep_simulations=True,
    n_simulations=N_SIMULACIONES_GFK,
    hull=poligono_gfk
)

resultado_k = k_test(
    coordenadas_gfk,
    support=PUNTOS_SOPORTE,
    keep_simulations=True,
    n_simulations=N_SIMULACIONES_GFK,
    hull=poligono_gfk
)


# ----------------------------------------------------------
# 4. Resumir la posición frente a la envolvente del 95 %
# ----------------------------------------------------------

def resumir_funcion(resultado):
    """
    Cuenta los puntos del soporte en los que la curva
    observada queda fuera de la envolvente del 95 % de
    las simulaciones.
    """
    limite_inferior = np.percentile(
        resultado.simulations, 2.5, axis=0
    )
    limite_superior = np.percentile(
        resultado.simulations, 97.5, axis=0
    )
    fuera = int(np.sum(
        (resultado.statistic < limite_inferior)
        | (resultado.statistic > limite_superior)
    ))
    return limite_inferior, limite_superior, fuera


env_g_inf, env_g_sup, fuera_g = resumir_funcion(resultado_g)
env_f_inf, env_f_sup, fuera_f = resumir_funcion(resultado_f)
env_k_inf, env_k_sup, fuera_k = resumir_funcion(resultado_k)


# ----------------------------------------------------------
# 5. Construir la Tabla 14
# ----------------------------------------------------------

tabla_14 = pd.DataFrame({

    "Función": [
        "G (vecino más cercano)",
        "F (espacios vacíos)",
        "K de Ripley"
    ],

    "Posición frente a la envolvente CSR": [
        "Por encima a distancias cortas",
        "Por debajo en casi todo el soporte",
        "Por encima en casi todo el soporte"
    ],

    "Puntos del soporte fuera de la envolvente": [
        f"{fuera_g} de {PUNTOS_SOPORTE}",
        f"{fuera_f} de {PUNTOS_SOPORTE}",
        f"{fuera_k} de {PUNTOS_SOPORTE}"
    ],

    "Lectura": [
        "Las anomalías tienen vecinas más próximas de lo "
        "esperado bajo el azar: agrupamiento",
        "Los espacios vacíos son más extensos de lo esperado "
        "bajo el azar: agrupamiento",
        "Exceso de anomalías vecinas a todas las escalas: "
        "agrupamiento"
    ]
})

tabla_14_estilizada = (
    tabla_14.style
    .hide(axis="index")
    .set_caption(
        "Tabla 14. Síntesis de las funciones G, F y K del "
        "patrón de anomalías frente a las envolventes de "
        f"simulación CSR (n = {N_SIMULACIONES_GFK} "
        "simulaciones por función)."
    )
    .set_properties(
        subset=["Puntos del soporte fuera de la envolvente"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_14.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_14_Funciones_GFK_Anomalias.csv",
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 6. Construir la Figura 14
# ----------------------------------------------------------

figura_gfk, ejes_gfk = plt.subplots(1, 3, figsize=(18, 5.8))

configuracion_gfk = [
    (resultado_g, env_g_inf, env_g_sup,
     "Función G (vecino más cercano)", "$G(d)$",
     "#4B0082", "lower right"),
    (resultado_f, env_f_inf, env_f_sup,
     "Función F (espacios vacíos)", "$F(d)$",
     "#1B6CA8", "upper left"),
    (resultado_k, env_k_inf, env_k_sup,
     "Función K de Ripley", "$K(d)$",
     "#B22222", "upper left"),
]

for eje, (resultado, env_inf, env_sup, titulo,
          etiqueta_y, color, posicion_leyenda) in zip(
        ejes_gfk, configuracion_gfk):

    distancia_km = resultado.support / 1000

    eje.fill_between(
        distancia_km, env_inf, env_sup,
        color="#BDBDBD", alpha=0.55,
        label=(
            "Envolvente 95 % CSR "
            f"({N_SIMULACIONES_GFK} sim.)"
        )
    )

    eje.plot(
        distancia_km,
        resultado.simulations.mean(axis=0),
        color="#6E6E6E", linewidth=1.1, linestyle="--",
        label="Media de las simulaciones"
    )

    eje.plot(
        distancia_km, resultado.statistic,
        color=color, linewidth=2.4,
        label="Patrón de anomalías"
    )

    eje.set_title(titulo, fontsize=13, fontweight="bold")
    eje.set_xlabel("Distancia (km)")
    eje.set_ylabel(etiqueta_y)
    eje.grid(alpha=0.3)
    eje.legend(fontsize=9, loc=posicion_leyenda)

figura_gfk.suptitle(
    "Funciones G, F y K del patrón de anomalías de cobre "
    "frente a la aleatoriedad espacial completa",
    fontsize=15, fontweight="bold"
)

figura_gfk.text(
    0.99, 0.01,
    "Fuente: base geoquímica de Cu y elaboración propia.",
    ha="right", fontsize=9
)

plt.tight_layout(rect=[0, 0.03, 1, 0.94])

plt.savefig(
    FIGURAS / "Figura_14_Funciones_GFK_Anomalias.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

tabla_14_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 118
# ==========================================================
# ==========================================================
# TABLA 15. ENRIQUECIMIENTO DE ANOMALÍAS POR UNIDAD
# GEOLÓGICA (PRUEBA DE REETIQUETADO POR PERMUTACIÓN)
# ==========================================================

import numpy as np
import pandas as pd
import geopandas as gpd


# ----------------------------------------------------------
# 1. Parámetros del análisis
# ----------------------------------------------------------

N_PERMUTACIONES_GEO = 999
SEMILLA_GEO = 42
MINIMO_MUESTRAS_UNIDAD = 10


# ----------------------------------------------------------
# 2. Verificar los insumos
# ----------------------------------------------------------

if "muestras_indicadora" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )

if "geologia" not in globals():
    raise NameError(
        "No se encontró la capa de geología. Ejecuta "
        "primero la carga de datos (1.2)."
    )


# ----------------------------------------------------------
# 3. Normalizar la unidad de análisis
# ----------------------------------------------------------
# Se agrupa por la descripción de la unidad porque el campo
# de código (ENTITY) presenta rótulos truncados e
# inconsistentes en la cartografía disponible.

geologia_enriq = geologia.copy()

geologia_enriq["UNIDAD_ANALISIS"] = (
    geologia_enriq["DESCRIPCIO"]
    .fillna(geologia_enriq["ENTITY"])
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace(
        "GABRO ALTAMIRA",
        "GABRO DE ALTAMIRA",
        regex=False
    )
)


# ----------------------------------------------------------
# 4. Unión espacial de las muestras con la geología
# ----------------------------------------------------------

union_geo = gpd.sjoin(
    muestras_indicadora,
    geologia_enriq[["UNIDAD_ANALISIS", "geometry"]],
    how="left",
    predicate="within"
)

# Se conserva una sola unidad por muestra en caso de
# polígonos superpuestos
union_geo = union_geo[
    ~union_geo.index.duplicated(keep="first")
]

union_geo["UNIDAD_ANALISIS"] = (
    union_geo["UNIDAD_ANALISIS"].fillna("SIN UNIDAD")
)

numero_muestras_geo = len(union_geo)
numero_anomalias_geo = int(union_geo["INDICADOR"].sum())


# ----------------------------------------------------------
# 5. Conteos y razón de enriquecimiento por unidad
# ----------------------------------------------------------

tabla_unidades = union_geo.groupby("UNIDAD_ANALISIS").agg(
    muestras=("INDICADOR", "size"),
    anomalias=("INDICADOR", "sum")
)

tabla_unidades["tasa_anomalias"] = (
    tabla_unidades["anomalias"]
    / tabla_unidades["muestras"] * 100
)

tabla_unidades["enriquecimiento"] = (
    (tabla_unidades["anomalias"] / numero_anomalias_geo)
    / (tabla_unidades["muestras"] / numero_muestras_geo)
)


# ----------------------------------------------------------
# 6. Prueba de reetiquetado por permutación
# ----------------------------------------------------------
# En cada permutación se redistribuyen aleatoriamente las
# etiquetas de anomalía entre los sitios muestreados y se
# cuenta cuántas caen en cada unidad.

np.random.seed(SEMILLA_GEO)

codigos_unidad, indices_unidad = np.unique(
    union_geo["UNIDAD_ANALISIS"].to_numpy(),
    return_inverse=True
)

vector_anomalias = union_geo["INDICADOR"].to_numpy()

conteos_simulados = np.zeros(
    (N_PERMUTACIONES_GEO, len(codigos_unidad))
)

for indice_permutacion in range(N_PERMUTACIONES_GEO):

    permutacion = np.random.permutation(vector_anomalias)

    conteos_simulados[indice_permutacion] = np.bincount(
        indices_unidad,
        weights=permutacion,
        minlength=len(codigos_unidad)
    )

conteos_observados = np.bincount(
    indices_unidad,
    weights=vector_anomalias,
    minlength=len(codigos_unidad)
)

pseudo_p_unidades = {}
esperado_unidades = {}

for posicion, unidad in enumerate(codigos_unidad):

    pseudo_p_unidades[unidad] = (
        (1 + np.sum(
            conteos_simulados[:, posicion]
            >= conteos_observados[posicion]
        ))
        / (1 + N_PERMUTACIONES_GEO)
    )

    esperado_unidades[unidad] = float(
        conteos_simulados[:, posicion].mean()
    )

tabla_unidades["anomalias_esperadas"] = [
    esperado_unidades[u] for u in tabla_unidades.index
]

tabla_unidades["pseudo_p_exceso"] = [
    pseudo_p_unidades[u] for u in tabla_unidades.index
]


# ----------------------------------------------------------
# 7. Construir la Tabla 15
# ----------------------------------------------------------
# Se reportan las unidades con un mínimo de muestras para
# que la razón de enriquecimiento sea interpretable.

tabla_15 = (
    tabla_unidades[
        tabla_unidades["muestras"] >= MINIMO_MUESTRAS_UNIDAD
    ]
    .sort_values("enriquecimiento", ascending=False)
    .reset_index()
    .rename(columns={
        "UNIDAD_ANALISIS": "Unidad geológica",
        "muestras": "Muestras",
        "anomalias": "Anomalías",
        "tasa_anomalias": "Tasa de anomalías (%)",
        "enriquecimiento": "Enriquecimiento",
        "anomalias_esperadas": "Anomalías esperadas",
        "pseudo_p_exceso": "Pseudo p (exceso)"
    })
)

tabla_15["Anomalías"] = tabla_15["Anomalías"].astype(int)


# ----------------------------------------------------------
# 8. Mostrar y guardar la Tabla 15
# ----------------------------------------------------------

def resaltar_significativas(fila):
    """Resalta las unidades con exceso significativo."""
    if fila["Pseudo p (exceso)"] < 0.05:
        return ["background-color: #FBE9E7"] * len(fila)
    return [""] * len(fila)

tabla_15_estilizada = (
    tabla_15.style
    .hide(axis="index")
    .apply(resaltar_significativas, axis=1)
    .set_caption(
        "Tabla 15. Enriquecimiento de anomalías de cobre por "
        "unidad geológica y prueba de reetiquetado "
        f"({N_PERMUTACIONES_GEO} permutaciones; unidades con "
        f"al menos {MINIMO_MUESTRAS_UNIDAD} muestras)."
    )
    .format({
        "Tasa de anomalías (%)": "{:.1f}",
        "Enriquecimiento": "{:.2f}",
        "Anomalías esperadas": "{:.1f}",
        "Pseudo p (exceso)": "{:.3f}"
    })
    .set_properties(
        subset=[
            "Muestras", "Anomalías",
            "Tasa de anomalías (%)", "Enriquecimiento",
            "Anomalías esperadas", "Pseudo p (exceso)"
        ],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_15.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_15_Enriquecimiento_Unidades.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_15_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 119
# ==========================================================
# ==========================================================
# FIGURA 15. ANOMALÍAS, UNIDADES GEOLÓGICAS
# Y RAZÓN DE ENRIQUECIMIENTO
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
import textwrap

from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# ----------------------------------------------------------
# 1. Verificar los insumos de la Tabla 15
# ----------------------------------------------------------

if "tabla_15" not in globals():
    raise NameError(
        "Primero debes ejecutar la celda de la Tabla 15."
    )

limite_geo = municipios.dissolve()

anomalias_geo = muestras_indicadora[
    muestras_indicadora["INDICADOR"] == 1
].copy()

fondo_geo = muestras_indicadora[
    muestras_indicadora["INDICADOR"] == 0
].copy()


# ----------------------------------------------------------
# 2. Identificar unidades con exceso significativo
# ----------------------------------------------------------

unidades_significativas = tabla_15[
    tabla_15["Pseudo p (exceso)"] < 0.05
]["Unidad geológica"].tolist()

colores_significativas = [
    "#6A3D9A",
    "#E31A1C",
    "#FF7F00",
    "#B15928",
    "#33A02C"
]


# ----------------------------------------------------------
# 3. Construir la figura
# ----------------------------------------------------------

figura_geo = plt.figure(
    figsize=(20, 10.5)
)

rejilla_geo = figura_geo.add_gridspec(
    1,
    2,
    width_ratios=[1.05, 1.30],
    wspace=0.38,
    left=0.06,
    right=0.98,
    top=0.88,
    bottom=0.12
)

eje_mapa_geo = figura_geo.add_subplot(
    rejilla_geo[0]
)

eje_barras_geo = figura_geo.add_subplot(
    rejilla_geo[1]
)


# ----------------------------------------------------------
# 4. Panel A: mapa
# ----------------------------------------------------------

geologia_enriq.plot(
    ax=eje_mapa_geo,
    facecolor="#EDEDED",
    edgecolor="#CFCFCF",
    linewidth=0.2
)

elementos_geo = []

for posicion, unidad in enumerate(
    unidades_significativas
):

    color = colores_significativas[
        posicion % len(colores_significativas)
    ]

    capa_unidad = geologia_enriq[
        geologia_enriq["UNIDAD_ANALISIS"] == unidad
    ]

    if not capa_unidad.empty:

        capa_unidad.plot(
            ax=eje_mapa_geo,
            facecolor=color,
            edgecolor="none",
            alpha=0.75
        )

        elementos_geo.append(
            Patch(
                facecolor=color,
                alpha=0.75,
                label=unidad.title()
            )
        )

limite_geo.boundary.plot(
    ax=eje_mapa_geo,
    color="black",
    linewidth=1.3
)

eje_mapa_geo.scatter(
    fondo_geo.geometry.x,
    fondo_geo.geometry.y,
    s=3.5,
    color="#B5B5B5",
    zorder=4
)

eje_mapa_geo.scatter(
    anomalias_geo.geometry.x,
    anomalias_geo.geometry.y,
    s=16,
    color="#00363A",
    edgecolor="white",
    linewidth=0.3,
    zorder=5
)

elementos_geo += [
    Line2D(
        [0],
        [0],
        marker="o",
        color="none",
        markerfacecolor="#00363A",
        markeredgecolor="white",
        markersize=6,
        label=(
            f"Anomalías de Cu "
            f"(n = {len(anomalias_geo)})"
        )
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        color="none",
        markerfacecolor="#B5B5B5",
        markersize=4,
        label="Fondo geoquímico"
    )
]

eje_mapa_geo.legend(
    handles=elementos_geo,
    title="Unidades con exceso significativo",
    loc="upper right",
    fontsize=8.5,
    title_fontsize=9.5,
    framealpha=0.95
)

eje_mapa_geo.add_artist(
    ScaleBar(
        1,
        units="m",
        location="lower left",
        box_alpha=0.8
    )
)

eje_mapa_geo.text(
    0.98,
    0.02,
    "Sistema de referencia\nEPSG:21897",
    transform=eje_mapa_geo.transAxes,
    ha="right",
    va="bottom",
    fontsize=8.5,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.4"
    )
)

eje_mapa_geo.set_title(
    "Anomalías y unidades con exceso significativo",
    fontsize=13,
    fontweight="bold",
    pad=8
)

eje_mapa_geo.set_xlabel(
    "Coordenada Este (m)"
)

eje_mapa_geo.set_ylabel(
    "Coordenada Norte (m)"
)

eje_mapa_geo.ticklabel_format(
    style="plain"
)

eje_mapa_geo.tick_params(
    labelsize=8.5
)

eje_mapa_geo.set_aspect(
    "equal"
)


# ----------------------------------------------------------
# 5. Panel B: razón de enriquecimiento
# ----------------------------------------------------------

tabla_barras = tabla_15.sort_values(
    "Enriquecimiento",
    ascending=True
).copy()

tabla_barras["Unidad_etiqueta"] = (
    tabla_barras["Unidad geológica"]
    .str.title()
    .apply(
        lambda texto: textwrap.fill(
            str(texto),
            width=28,
            break_long_words=False,
            break_on_hyphens=False
        )
    )
)

colores_barras = [
    "#B22222" if p < 0.05 else "#9FB6CD"
    for p in tabla_barras["Pseudo p (exceso)"]
]

posiciones_y = np.arange(
    len(tabla_barras)
)

eje_barras_geo.barh(
    posiciones_y,
    tabla_barras["Enriquecimiento"],
    color=colores_barras,
    edgecolor="#4A4A4A",
    linewidth=0.5,
    height=0.72
)

eje_barras_geo.set_yticks(
    posiciones_y
)

eje_barras_geo.set_yticklabels(
    tabla_barras["Unidad_etiqueta"],
    fontsize=8.5,
    ha="right"
)

eje_barras_geo.tick_params(
    axis="y",
    pad=6,
    length=0
)

eje_barras_geo.axvline(
    1,
    color="black",
    linewidth=1.4,
    linestyle="--",
    zorder=3
)

max_enriquecimiento = tabla_barras[
    "Enriquecimiento"
].max()

desplazamiento = max(
    max_enriquecimiento * 0.025,
    0.06
)

for posicion, (_, fila) in enumerate(
    tabla_barras.iterrows()
):

    significativa = (
        fila["Pseudo p (exceso)"] < 0.05
    )

    etiqueta_valor = (
        f"{fila['Enriquecimiento']:.2f}"
    )

    if significativa:

        etiqueta_valor += (
            f"  (p = "
            f"{fila['Pseudo p (exceso)']:.3f})"
        )

    eje_barras_geo.text(
        fila["Enriquecimiento"]
        + desplazamiento,
        posicion,
        etiqueta_valor,
        va="center",
        ha="left",
        fontsize=8.5,
        fontweight=(
            "bold"
            if significativa
            else "normal"
        ),
        clip_on=False
    )

eje_barras_geo.set_xlim(
    0,
    max_enriquecimiento + 1.45
)

eje_barras_geo.set_xlabel(
    "Razón de enriquecimiento "
    "(% anomalías / % muestras)",
    fontsize=10
)

eje_barras_geo.set_title(
    (
        "Enriquecimiento por unidad "
        f"(≥ {MINIMO_MUESTRAS_UNIDAD} muestras)"
    ),
    fontsize=13,
    fontweight="bold",
    pad=10
)

eje_barras_geo.grid(
    alpha=0.25,
    axis="x",
    linewidth=0.7
)

eje_barras_geo.set_axisbelow(True)

eje_barras_geo.legend(
    handles=[
        Patch(
            facecolor="#B22222",
            edgecolor="#4A4A4A",
            label="Exceso significativo (p < 0.05)"
        ),
        Patch(
            facecolor="#9FB6CD",
            edgecolor="#4A4A4A",
            label="Sin exceso significativo"
        )
    ],
    loc="lower right",
    fontsize=9,
    framealpha=0.95
)


# ----------------------------------------------------------
# 6. Título general y fuente
# ----------------------------------------------------------

figura_geo.suptitle(
    "Relación del patrón de anomalías de cobre con las "
    "unidades geológicas",
    fontsize=16,
    fontweight="bold",
    y=0.97
)

figura_geo.text(
    0.98,
    0.035,
    "Fuente: base geoquímica de Cu, cartografía geológica "
    "del SGC y elaboración propia.",
    ha="right",
    va="bottom",
    fontsize=9
)


# ----------------------------------------------------------
# 7. Guardar la Figura 15
# ----------------------------------------------------------

plt.savefig(
    FIGURAS / "Figura_15_Enriquecimiento_Unidades.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.15
)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 122
# ==========================================================
# ==========================================================
# TABLA 16. DISTANCIA DE LAS ANOMALÍAS A LAS FALLAS
# GEOLÓGICAS (PRUEBA DE REETIQUETADO POR PERMUTACIÓN)
# ==========================================================

import numpy as np
import pandas as pd


# ----------------------------------------------------------
# 1. Parámetros del análisis
# ----------------------------------------------------------

N_PERMUTACIONES_FALLAS = 999
SEMILLA_FALLAS = 42


# ----------------------------------------------------------
# 2. Verificar los insumos
# ----------------------------------------------------------

if "muestras_indicadora" not in globals():
    raise NameError(
        "Primero debes ejecutar la transformación "
        "indicadora (4.2)."
    )

if "fallas" not in globals():
    raise NameError(
        "No se encontró la capa de fallas. Ejecuta primero "
        "la carga de datos (1.2)."
    )


# ----------------------------------------------------------
# 3. Calcular la distancia a la falla más cercana
# ----------------------------------------------------------

fallas_union = fallas.geometry.union_all()

muestras_fallas = muestras_indicadora.copy()

muestras_fallas["DIST_FALLA"] = (
    muestras_fallas.geometry.distance(fallas_union)
)

distancias_todas = muestras_fallas["DIST_FALLA"].to_numpy()

vector_anomalias_fallas = (
    muestras_fallas["INDICADOR"].to_numpy()
)

distancias_anomalias = distancias_todas[
    vector_anomalias_fallas == 1
]

distancias_fondo = distancias_todas[
    vector_anomalias_fallas == 0
]

numero_anomalias_fallas = len(distancias_anomalias)


# ----------------------------------------------------------
# 4. Prueba de reetiquetado por permutación
# ----------------------------------------------------------
# En cada permutación se seleccionan al azar tantos sitios
# como anomalías hay, entre los 2,029 muestreados, y se
# calcula su distancia media a las fallas.

np.random.seed(SEMILLA_FALLAS)

medias_simuladas = np.empty(N_PERMUTACIONES_FALLAS)

for indice_permutacion in range(N_PERMUTACIONES_FALLAS):

    seleccion = np.random.permutation(
        len(distancias_todas)
    )[:numero_anomalias_fallas]

    medias_simuladas[indice_permutacion] = (
        distancias_todas[seleccion].mean()
    )

media_observada = float(distancias_anomalias.mean())

pseudo_p_fallas = (
    (1 + np.sum(medias_simuladas <= media_observada))
    / (1 + N_PERMUTACIONES_FALLAS)
)

if pseudo_p_fallas < 0.05:
    interpretacion_fallas = (
        "Las anomalías están significativamente más cerca "
        "de las fallas que el azar del muestreo"
    )
else:
    interpretacion_fallas = (
        "La cercanía de las anomalías a las fallas es "
        "compatible con el azar del muestreo"
    )


# ----------------------------------------------------------
# 5. Construir la Tabla 16
# ----------------------------------------------------------

tabla_16 = pd.DataFrame({

    "Parámetro": [
        "Anomalías analizadas",
        "Sitios del fondo geoquímico",
        "Distancia media de las anomalías",
        "Distancia mediana de las anomalías",
        "Distancia media del fondo",
        "Distancia mediana del fondo",
        "Distancia media simulada (reetiquetado)",
        "Percentil 5 de las medias simuladas",
        "Número de permutaciones",
        "Pseudo valor p (cercanía)",
        "Interpretación (α = 0.05)"
    ],

    "Valor": [
        f"{numero_anomalias_fallas:,}",
        f"{len(distancias_fondo):,}",
        f"{media_observada:,.1f} m",
        f"{np.median(distancias_anomalias):,.1f} m",
        f"{distancias_fondo.mean():,.1f} m",
        f"{np.median(distancias_fondo):,.1f} m",
        f"{medias_simuladas.mean():,.1f} m",
        f"{np.percentile(medias_simuladas, 5):,.1f} m",
        f"{N_PERMUTACIONES_FALLAS:,}",
        f"{pseudo_p_fallas:.4f}",
        interpretacion_fallas
    ]
})


# ----------------------------------------------------------
# 6. Mostrar y guardar la Tabla 16
# ----------------------------------------------------------

tabla_16_estilizada = (
    tabla_16.style
    .hide(axis="index")
    .set_caption(
        "Tabla 16. Distancia de las anomalías de cobre a las "
        "fallas geológicas y prueba de reetiquetado por "
        "permutación."
    )
    .set_properties(
        subset=["Valor"],
        **{"text-align": "center"}
    )
    .set_table_styles([
        {
            "selector": "caption",
            "props": [
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
                ("padding-bottom", "8px")
            ]
        },
        {
            "selector": "th",
            "props": [
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border-bottom", "1px solid #555555"),
                ("padding", "7px")
            ]
        },
        {
            "selector": "td",
            "props": [("padding", "6px")]
        }
    ])
)

tabla_16.to_csv(
    RESULTADOS / "01_Tablas" / "Tabla_16_Distancia_Fallas_Anomalias.csv",
    index=False,
    encoding="utf-8-sig"
)

tabla_16_estilizada


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 123
# ==========================================================
# ==========================================================
# FIGURA 16. ANOMALÍAS Y FALLAS: MAPA, DISTRIBUCIONES
# DE DISTANCIA Y PRUEBA DE REETIQUETADO
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt

from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.lines import Line2D


# ----------------------------------------------------------
# 1. Verificar los insumos de la Tabla 16
# ----------------------------------------------------------

variables_requeridas = [
    "distancias_anomalias", "distancias_fondo",
    "medias_simuladas", "media_observada",
    "pseudo_p_fallas", "muestras_fallas"
]

variables_faltantes = [
    v for v in variables_requeridas if v not in globals()
]

if variables_faltantes:
    raise NameError(
        "Primero debes ejecutar la celda de la Tabla 16. "
        f"Variables faltantes: {variables_faltantes}"
    )

limite_fallas = municipios.dissolve()

anomalias_mapa = muestras_fallas[
    muestras_fallas["INDICADOR"] == 1
]

fondo_mapa = muestras_fallas[
    muestras_fallas["INDICADOR"] == 0
]


# ----------------------------------------------------------
# 2. Construir la figura
# ----------------------------------------------------------

figura_fallas = plt.figure(figsize=(18, 8.5))

rejilla_fallas = figura_fallas.add_gridspec(
    1, 3, width_ratios=[1.15, 1, 1], wspace=0.2
)

eje_mapa_fallas = figura_fallas.add_subplot(
    rejilla_fallas[0]
)
eje_ecdf = figura_fallas.add_subplot(rejilla_fallas[1])
eje_permutacion = figura_fallas.add_subplot(
    rejilla_fallas[2]
)


# ----------------------------------------------------------
# 3. Panel A: mapa de anomalías y fallas
# ----------------------------------------------------------

municipios.plot(
    ax=eje_mapa_fallas,
    facecolor="#F2F2F2",
    edgecolor="#BDBDBD",
    linewidth=0.4
)

limite_fallas.boundary.plot(
    ax=eje_mapa_fallas,
    color="black",
    linewidth=1.2
)

fallas.plot(
    ax=eje_mapa_fallas,
    color="#8B0000",
    linewidth=0.8,
    zorder=4
)

eje_mapa_fallas.scatter(
    fondo_mapa.geometry.x, fondo_mapa.geometry.y,
    s=3.5, color="#B5B5B5", zorder=5
)

eje_mapa_fallas.scatter(
    anomalias_mapa.geometry.x, anomalias_mapa.geometry.y,
    s=15, color="#4B0082",
    edgecolor="white", linewidth=0.3, zorder=6
)

eje_mapa_fallas.legend(
    handles=[
        Line2D(
            [0], [0], color="#8B0000", linewidth=1.5,
            label="Fallas geológicas"
        ),
        Line2D(
            [0], [0], marker="o", color="none",
            markerfacecolor="#4B0082",
            markeredgecolor="white", markersize=6,
            label=(
                "Anomalías "
                f"(n = {len(anomalias_mapa)})"
            )
        ),
        Line2D(
            [0], [0], marker="o", color="none",
            markerfacecolor="#B5B5B5", markersize=4,
            label="Fondo geoquímico"
        )
    ],
    loc="upper right",
    fontsize=9.5,
    framealpha=0.95
)

eje_mapa_fallas.add_artist(
    ScaleBar(1, units="m", location="lower left",
             box_alpha=0.8)
)

eje_mapa_fallas.text(
    0.98, 0.02,
    "Sistema de referencia\nEPSG:21897",
    transform=eje_mapa_fallas.transAxes,
    ha="right", va="bottom", fontsize=9,
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="square,pad=0.4"
    )
)

eje_mapa_fallas.set_title(
    "Anomalías y fallas geológicas",
    fontsize=13, fontweight="bold"
)

eje_mapa_fallas.set_xlabel("Coordenada Este (m)")
eje_mapa_fallas.set_ylabel("Coordenada Norte (m)")
eje_mapa_fallas.ticklabel_format(style="plain")
eje_mapa_fallas.tick_params(labelsize=8.5)


# ----------------------------------------------------------
# 4. Panel B: distribuciones acumuladas de distancia
# ----------------------------------------------------------

curvas_ecdf = [
    (
        distancias_anomalias, "#4B0082",
        (
            "Anomalías (mediana = "
            f"{np.median(distancias_anomalias) / 1000:.2f} km)"
        )
    ),
    (
        distancias_fondo, "#9E9E9E",
        (
            "Fondo (mediana = "
            f"{np.median(distancias_fondo) / 1000:.2f} km)"
        )
    ),
]

for datos, color, etiqueta in curvas_ecdf:

    distancias_orden = np.sort(datos) / 1000

    proporcion = (
        np.arange(1, len(distancias_orden) + 1)
        / len(distancias_orden)
    )

    eje_ecdf.plot(
        distancias_orden, proporcion,
        color=color, linewidth=2.2, label=etiqueta
    )

eje_ecdf.set_xlim(0, 10)
eje_ecdf.set_xlabel(
    "Distancia a la falla más cercana (km)"
)
eje_ecdf.set_ylabel("Proporción acumulada")
eje_ecdf.set_title(
    "Distribución acumulada de distancias",
    fontsize=13, fontweight="bold"
)
eje_ecdf.grid(alpha=0.3)
eje_ecdf.legend(fontsize=9.5, loc="lower right")


# ----------------------------------------------------------
# 5. Panel C: prueba de reetiquetado
# ----------------------------------------------------------

eje_permutacion.hist(
    medias_simuladas / 1000,
    bins=30,
    color="#9FB6CD",
    edgecolor="#5A7A9B",
    linewidth=0.5
)

eje_permutacion.axvline(
    media_observada / 1000,
    color="#4B0082",
    linewidth=2.5,
    linestyle="--"
)

eje_permutacion.text(
    media_observada / 1000,
    eje_permutacion.get_ylim()[1] * 0.95,
    (
        "  Media observada = "
        f"{media_observada / 1000:.2f} km"
    ),
    color="#4B0082",
    fontsize=10.5,
    fontweight="bold",
    ha="left",
    va="top",
    rotation=90
)

eje_permutacion.set_title(
    (
        "Reetiquetado: media de distancia\n"
        f"({len(medias_simuladas)} permutaciones · "
        f"pseudo p = {pseudo_p_fallas:.3f})"
    ),
    fontsize=13, fontweight="bold"
)

eje_permutacion.set_xlabel(
    "Distancia media a fallas (km)"
)
eje_permutacion.set_ylabel("Frecuencia")
eje_permutacion.grid(alpha=0.3)

figura_fallas.suptitle(
    "Relación del patrón de anomalías de cobre con las "
    "fallas geológicas",
    fontsize=15.5, fontweight="bold"
)

figura_fallas.text(
    0.99, 0.01,
    "Fuente: base geoquímica de Cu, cartografía estructural "
    "del SGC y elaboración propia.",
    ha="right", fontsize=9
)


# ----------------------------------------------------------
# 6. Guardar la Figura 16
# ----------------------------------------------------------

plt.savefig(
    FIGURAS / "Figura_16_Distancia_Fallas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\n" + "=" * 72)
print("05_patron_anomalias.py COMPLETADO")
print("=" * 72)
