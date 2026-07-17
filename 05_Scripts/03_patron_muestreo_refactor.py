"""
03_patron_muestreo.py

Capítulo 3. Análisis espacial del patrón de muestreo

Carga las capas directamente desde el repositorio local y ejecuta el
código analítico correspondiente al notebook original.
"""

from __future__ import annotations

from config import *
from utils import cargar_capas_base

_contexto = cargar_capas_base(preferir_muestras_estudio=True)
muestras = _contexto["muestras"]
muestras_estudio = _contexto["muestras_estudio"]
geologia = _contexto["geologia"]
fallas = _contexto["fallas"]
municipios = _contexto["municipios"]

print("\n" + "=" * 72)
print("CAPÍTULO 3. ANÁLISIS ESPACIAL DEL PATRÓN DE MUESTREO")
print("=" * 72)

# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 73
# ==========================================================
# ==========================================================
# FIGURA 05. COMPARACIÓN ENTRE MUESTREO REGULAR E IRREGULAR
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# 1. Preparar las muestras reales
# ----------------------------------------------------------

if "muestras_estudio" in globals():
    muestras_fig = muestras_estudio.copy()
else:
    muestras_fig = muestras.copy()

muestras_fig = muestras_fig[
    muestras_fig.geometry.notna()
    & ~muestras_fig.geometry.is_empty
].copy()

# Extraer coordenadas
x_real = muestras_fig.geometry.x.to_numpy()
y_real = muestras_fig.geometry.y.to_numpy()

mascara_valida = (
    np.isfinite(x_real)
    & np.isfinite(y_real)
)

x_real = x_real[mascara_valida]
y_real = y_real[mascara_valida]


# ----------------------------------------------------------
# 2. Normalizar las coordenadas reales
#    para comparar únicamente la disposición espacial
# ----------------------------------------------------------

x_real_norm = (
    (x_real - x_real.min())
    / (x_real.max() - x_real.min())
)

y_real_norm = (
    (y_real - y_real.min())
    / (y_real.max() - y_real.min())
)


# ----------------------------------------------------------
# 3. Crear una malla regular sintética
# ----------------------------------------------------------

n_columnas = 8
n_filas = 8

x_regular = np.linspace(
    0.08,
    0.92,
    n_columnas
)

y_regular = np.linspace(
    0.08,
    0.92,
    n_filas
)

xx_regular, yy_regular = np.meshgrid(
    x_regular,
    y_regular
)

x_regular = xx_regular.ravel()
y_regular = yy_regular.ravel()


# ----------------------------------------------------------
# 4. Crear la Figura 05
# ----------------------------------------------------------

fig, ejes = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(12, 5.8),
    facecolor="white"
)

ax_regular, ax_irregular = ejes


# ----------------------------------------------------------
# 5. Panel A. Muestreo regular
# ----------------------------------------------------------

# Dibujar líneas de la malla
for x in np.unique(x_regular):
    ax_regular.plot(
        [x, x],
        [y_regular.min(), y_regular.max()],
        color="#D0D0D0",
        linewidth=0.8,
        zorder=1
    )

for y in np.unique(y_regular):
    ax_regular.plot(
        [x_regular.min(), x_regular.max()],
        [y, y],
        color="#D0D0D0",
        linewidth=0.8,
        zorder=1
    )

# Dibujar puntos
ax_regular.scatter(
    x_regular,
    y_regular,
    s=42,
    color="#2F5597",
    edgecolor="white",
    linewidth=0.6,
    zorder=2
)

ax_regular.set_title(
    "A. Muestreo regular",
    fontsize=11,
    fontweight="bold",
    pad=10
)

ax_regular.text(
    0.5,
    -0.08,
    "Separación uniforme del muestreo",
    transform=ax_regular.transAxes,
    ha="center",
    va="top",
    fontsize=8.5,
    color="#444444"
)


# ----------------------------------------------------------
# 6. Panel B. Muestreo irregular del estudio
# ----------------------------------------------------------

# Dibujar la misma malla regular del panel izquierdo
for x in np.unique(x_regular):
    ax_irregular.plot(
        [x, x],
        [0, 1],
        color="#D0D0D0",
        linewidth=0.8,
        zorder=1
    )

for y in np.unique(y_regular):
    ax_irregular.plot(
        [0, 1],
        [y, y],
        color="#D0D0D0",
        linewidth=0.8,
        zorder=1
    )

# Dibujar las muestras reales
ax_irregular.scatter(
    x_real_norm,
    y_real_norm,
    s=16,
    color="#2F5597",
    edgecolor="white",
    linewidth=0.35,
    alpha=0.90,
    zorder=2
)

ax_irregular.set_title(
    "B. Muestreo del estudio",
    fontsize=11,
    fontweight="bold",
    pad=10
)

ax_irregular.text(
    0.5,
    -0.08,
    "Separación no uniforme del muestreo",
    transform=ax_irregular.transAxes,
    ha="center",
    va="top",
    fontsize=8.5,
    color="#444444"
)


# ----------------------------------------------------------
# 7. Configuración común de los paneles
# ----------------------------------------------------------

for ax in ejes:

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")

    ax.set_xticks([])
    ax.set_yticks([])

    for borde in ax.spines.values():
        borde.set_visible(True)
        borde.set_color("#444444")
        borde.set_linewidth(0.8)

    ax.set_facecolor("#FCFCFC")


# ----------------------------------------------------------
# 8. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.06,
    right=0.98,
    bottom=0.18,
    top=0.90,
    wspace=0.14
)


# ----------------------------------------------------------
# 9. Añadir fuente
# ----------------------------------------------------------

fig.text(
    0.98,
    0.035,
    (
        "Fuente: esquema regular de elaboración propia y "
        "base geoquímica de Cu para el patrón real."
    ),
    ha="right",
    va="bottom",
    fontsize=7.5,
    color="#444444"
)


# ----------------------------------------------------------
# 10. Guardar únicamente en PNG
# ----------------------------------------------------------

nombre_archivo = (
    "Figura_05_Comparacion_Muestreo_"
    "Regular_Irregular.png"
)

ruta_png_figura_05 = FIGURAS / nombre_archivo

fig.savefig(
    ruta_png_figura_05,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)

print("=" * 68)
print("FIGURA 05 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"PNG: {ruta_png_figura_05}")
print(f"Muestras reales representadas: {len(x_real_norm):,}")
print("=" * 68)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 78
# ==========================================================
# ==========================================================
# FIGURA 06. DISTRIBUCIÓN ESPACIAL DE LAS MUESTRAS
# CON HISTOGRAMAS MARGINALES
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter
import matplotlib.patheffects as pe


# ----------------------------------------------------------
# 1. Preparar copias de trabajo
# ----------------------------------------------------------

municipios_fig = municipios.copy()

# Utilizar las muestras recortadas al área de estudio,
# si esa variable ya fue creada anteriormente.
if "muestras_estudio" in globals():
    muestras_fig = muestras_estudio.copy()
else:
    muestras_fig = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_fig = municipios_fig[
    municipios_fig.geometry.notna()
    & ~municipios_fig.geometry.is_empty
].copy()

muestras_fig = muestras_fig[
    muestras_fig.geometry.notna()
    & ~muestras_fig.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Homogeneizar el sistema de referencia
# ----------------------------------------------------------

crs_mapa = municipios_fig.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un sistema "
        "de referencia espacial definido."
    )

if muestras_fig.crs is None:
    raise ValueError(
        "La capa de muestras no tiene un sistema "
        "de referencia espacial definido."
    )

if muestras_fig.crs != crs_mapa:
    muestras_fig = muestras_fig.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Extraer coordenadas de las muestras
# ----------------------------------------------------------

coordenada_este = muestras_fig.geometry.x.to_numpy()
coordenada_norte = muestras_fig.geometry.y.to_numpy()

mascara_valida = (
    np.isfinite(coordenada_este)
    & np.isfinite(coordenada_norte)
)

coordenada_este = coordenada_este[mascara_valida]
coordenada_norte = coordenada_norte[mascara_valida]


# ----------------------------------------------------------
# 5. Identificar nombres municipales
# ----------------------------------------------------------

columnas_nombre = [
    "NOMBRE",
    "NOMBRE_MPIO",
    "MPIO_CNMBR",
    "MUNICIPIO",
    "NOM_MPIO",
    "NOM_MUNIC"
]

columna_nombre = next(
    (
        columna
        for columna in columnas_nombre
        if columna in municipios_fig.columns
    ),
    None
)

if columna_nombre is not None:

    municipios_fig["NOMBRE_MAPA"] = (
        municipios_fig[columna_nombre]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

else:

    municipios_fig["NOMBRE_MAPA"] = ""


# ----------------------------------------------------------
# 6. Corregir nombres municipales abreviados
# ----------------------------------------------------------

nombres_corregidos = {
    "S.BARBA": "Santa Bárbara",
    "C.BOLIV": "Ciudad Bolívar",
    "P.RICO": "Pueblorrico",
    "MONTEBE": "Montebello",
    "TITIRIB": "Titiribí",
    "TAMESIS": "Támesis",
    "JERICO": "Jericó",
    "HISPANI": "Hispania",
    "FREDONI": "Fredonia",
    "ANGELOP": "Angelópolis",
    "CARAMAN": "Caramanta",
    "VALPARA": "Valparaíso",
    "CONCORD": "Concordia",
    "PINTADA": "La Pintada"
}

municipios_fig["NOMBRE_MAPA"] = (
    municipios_fig["NOMBRE_MAPA"]
    .replace(nombres_corregidos)
)

municipios_fig["NOMBRE_MAPA"] = (
    municipios_fig["NOMBRE_MAPA"]
    .apply(
        lambda nombre: nombre.title()
        if nombre and nombre == nombre.upper()
        else nombre
    )
)


# ----------------------------------------------------------
# 7. Crear límite exterior y extensión
# ----------------------------------------------------------

limite_estudio = municipios_fig.dissolve()

xmin, ymin, xmax, ymax = municipios_fig.total_bounds

rango_x = xmax - xmin
rango_y = ymax - ymin

margen_x = rango_x * 0.035
margen_y = rango_y * 0.035

limite_x = (
    xmin - margen_x,
    xmax + margen_x
)

limite_y = (
    ymin - margen_y,
    ymax + margen_y
)


# ----------------------------------------------------------
# 8. Calcular número de intervalos de los histogramas
#    mediante la regla de Freedman-Diaconis
# ----------------------------------------------------------

def calcular_numero_bins(valores, minimo=10, maximo=45):
    """
    Calcula el número de intervalos mediante la regla de
    Freedman-Diaconis, estableciendo límites razonables.
    """

    valores = np.asarray(valores)
    valores = valores[np.isfinite(valores)]

    if len(valores) < 2:
        return minimo

    q1, q3 = np.percentile(valores, [25, 75])
    iqr = q3 - q1

    if iqr == 0:
        return int(
            np.clip(
                np.sqrt(len(valores)),
                minimo,
                maximo
            )
        )

    ancho = 2 * iqr / np.cbrt(len(valores))

    if ancho <= 0:
        return int(
            np.clip(
                np.sqrt(len(valores)),
                minimo,
                maximo
            )
        )

    numero_bins = int(
        np.ceil(
            (valores.max() - valores.min()) / ancho
        )
    )

    return int(
        np.clip(
            numero_bins,
            minimo,
            maximo
        )
    )


bins_este = 25
bins_norte = 25


# ----------------------------------------------------------
# 9. Crear la Figura 06 mediante GridSpec
# ----------------------------------------------------------

fig = plt.figure(
    figsize=(10.5, 9.5),
    facecolor="white"
)

rejilla = GridSpec(
    nrows=2,
    ncols=2,
    figure=fig,
    width_ratios=[5.6, 1.25],
    height_ratios=[1.15, 5.8],
    hspace=0.04,
    wspace=0.04
)

ax_hist_este = fig.add_subplot(
    rejilla[0, 0]
)

ax_mapa = fig.add_subplot(
    rejilla[1, 0],
    sharex=ax_hist_este
)

ax_hist_norte = fig.add_subplot(
    rejilla[1, 1],
    sharey=ax_mapa
)


# ----------------------------------------------------------
# 10. Histograma marginal de la coordenada Este
# ----------------------------------------------------------

ax_hist_este.hist(
    coordenada_este,
    bins=bins_este,
    color="#3F78A8",
    edgecolor="#1F3F5B",
    linewidth=0.45,
    alpha=0.90
)

ax_hist_este.set_xlim(limite_x)

ax_hist_este.tick_params(
    axis="x",
    bottom=False,
    labelbottom=False
)

ax_hist_este.tick_params(
    axis="y",
    left=False,
    labelleft=False
)

ax_hist_este.spines["top"].set_visible(False)
ax_hist_este.spines["right"].set_visible(False)
ax_hist_este.spines["left"].set_visible(False)
ax_hist_este.spines["bottom"].set_color("#333333")
ax_hist_este.spines["bottom"].set_linewidth(0.8)

ax_hist_este.set_title(
    "Distribución de la coordenada Este",
    fontsize=9,
    pad=8
)


# ----------------------------------------------------------
# 11. Histograma marginal de la coordenada Norte
# ----------------------------------------------------------

ax_hist_norte.hist(
    coordenada_norte,
    bins=bins_norte,
    orientation="horizontal",
    color="#3F78A8",
    edgecolor="#1F3F5B",
    linewidth=0.45,
    alpha=0.90
)

ax_hist_norte.set_ylim(limite_y)

ax_hist_norte.tick_params(
    axis="x",
    bottom=False,
    labelbottom=False
)

ax_hist_norte.tick_params(
    axis="y",
    left=False,
    labelleft=False
)

ax_hist_norte.spines["top"].set_visible(False)
ax_hist_norte.spines["right"].set_visible(False)
ax_hist_norte.spines["bottom"].set_visible(False)
ax_hist_norte.spines["left"].set_color("#333333")
ax_hist_norte.spines["left"].set_linewidth(0.8)

ax_hist_norte.set_ylabel(
    "Distribución de la coordenada Norte",
    fontsize=9,
    rotation=270,
    labelpad=18
)


# ----------------------------------------------------------
# 12. Representar municipios en el mapa central
# ----------------------------------------------------------

municipios_fig.plot(
    ax=ax_mapa,
    facecolor="#FAFAF7",
    edgecolor="#888888",
    linewidth=0.50,
    alpha=1.0,
    zorder=1
)


# ----------------------------------------------------------
# 13. Representar las muestras
# ----------------------------------------------------------

muestras_fig.plot(
    ax=ax_mapa,
    color="#2F5597",
    marker="o",
    markersize=15,
    edgecolor="white",
    linewidth=0.40,
    alpha=0.92,
    zorder=3
)


# ----------------------------------------------------------
# 14. Resaltar el límite del área de estudio
# ----------------------------------------------------------

limite_estudio.boundary.plot(
    ax=ax_mapa,
    color="#111111",
    linewidth=1.55,
    zorder=4
)


# ----------------------------------------------------------
# 15. Añadir etiquetas municipales
# ----------------------------------------------------------

for _, fila in municipios_fig.iterrows():

    nombre = fila["NOMBRE_MAPA"]

    if not nombre:
        continue

    punto = fila.geometry.representative_point()

    texto = ax_mapa.text(
        punto.x,
        punto.y,
        nombre,
        fontsize=5.8,
        ha="center",
        va="center",
        color="#303030",
        zorder=5
    )

    texto.set_path_effects([
        pe.withStroke(
            linewidth=2.0,
            foreground="white"
        )
    ])


# ----------------------------------------------------------
# 16. Configurar extensión, proporción y coordenadas
# ----------------------------------------------------------

ax_mapa.set_xlim(limite_x)
ax_mapa.set_ylim(limite_y)
ax_mapa.set_aspect("equal")

ax_mapa.set_xlabel(
    "Coordenada Este (m)",
    fontsize=10
)

ax_mapa.set_ylabel(
    "Coordenada Norte (m)",
    fontsize=10
)

ax_mapa.xaxis.set_major_locator(
    MaxNLocator(nbins=5)
)

ax_mapa.yaxis.set_major_locator(
    MaxNLocator(nbins=6)
)

formato_coordenadas = ScalarFormatter(
    useOffset=False,
    useMathText=False
)

formato_coordenadas.set_scientific(False)

ax_mapa.xaxis.set_major_formatter(
    formato_coordenadas
)

ax_mapa.yaxis.set_major_formatter(
    formato_coordenadas
)

ax_mapa.tick_params(
    axis="both",
    labelsize=8.5,
    direction="out",
    length=4,
    width=0.8
)

ax_mapa.ticklabel_format(
    style="plain",
    axis="both",
    useOffset=False
)

ax_mapa.grid(False)


# ----------------------------------------------------------
# 17. Flecha norte
# ----------------------------------------------------------

ax_mapa.annotate(
    "N",
    xy=(0.945, 0.915),
    xytext=(0.945, 0.800),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=12,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=3.2,
        headwidth=9,
        headlength=9
    ),
    zorder=10
)


# ----------------------------------------------------------
# 18. Barra de escala
# ----------------------------------------------------------

barra_escala = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.23,
    width_fraction=0.008,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={"size": 8},
    border_pad=0.7,
    pad=0.4
)

ax_mapa.add_artist(barra_escala)


# ----------------------------------------------------------
# 19. Sistema de referencia espacial
# ----------------------------------------------------------

epsg_mapa = crs_mapa.to_epsg()

if epsg_mapa is not None:
    texto_crs = f"CRS: EPSG:{epsg_mapa}"
else:
    texto_crs = f"CRS: {crs_mapa.name}"

ax_mapa.text(
    0.985,
    0.018,
    texto_crs,
    transform=ax_mapa.transAxes,
    fontsize=7.3,
    ha="right",
    va="bottom",
    color="#333333",
    bbox=dict(
        facecolor="white",
        edgecolor="#888888",
        linewidth=0.50,
        alpha=0.92,
        boxstyle="round,pad=0.25"
    ),
    zorder=10
)


# ----------------------------------------------------------
# 20. Marco cartográfico
# ----------------------------------------------------------

for borde in ax_mapa.spines.values():
    borde.set_visible(True)
    borde.set_color("#333333")
    borde.set_linewidth(0.85)


# ----------------------------------------------------------
# 21. Fuente de los datos
# ----------------------------------------------------------

fig.text(
    0.985,
    0.018,
    (
        "Fuente: base geoquímica de Cu y límites municipales. "
        "Elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 22. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.10,
    right=0.93,
    bottom=0.10,
    top=0.97
)


# ----------------------------------------------------------
# 23. Guardar únicamente en PNG
# ----------------------------------------------------------

nombre_archivo = (
    "Figura_06_Distribucion_Espacial_Muestras_"
    "Histogramas_Marginales.png"
)

ruta_png_figura_06 = FIGURAS / nombre_archivo

fig.savefig(
    ruta_png_figura_06,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)

print("=" * 68)
print("FIGURA 06 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"PNG: {ruta_png_figura_06}")
print(f"Número de muestras representadas: {len(muestras_fig):,}")
print(f"Intervalos histograma Este: {bins_este}")
print(f"Intervalos histograma Norte: {bins_norte}")
print("=" * 68)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 83
# ==========================================================


# ==========================================================
# TABLA 06 Y FIGURA 07.
# CENTROGRAFÍA DEL PATRÓN DE MUESTREO
# ==========================================================

# Instalación omitida: las dependencias se gestionan desde 01_config.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from pointpats import centrography
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Circle
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter


# ----------------------------------------------------------
# 1. Preparar las capas
# ----------------------------------------------------------

municipios_centro = municipios.copy()

# Usar preferentemente las 2.029 muestras del área de estudio
if "muestras_estudio" in globals():
    muestras_centro = muestras_estudio.copy()
else:
    muestras_centro = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_centro = municipios_centro[
    municipios_centro.geometry.notna()
    & ~municipios_centro.geometry.is_empty
].copy()

muestras_centro = muestras_centro[
    muestras_centro.geometry.notna()
    & ~muestras_centro.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Verificar y homologar el CRS
# ----------------------------------------------------------

crs_mapa = municipios_centro.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un CRS definido."
    )

if muestras_centro.crs is None:
    raise ValueError(
        "La capa de muestras no tiene un CRS definido."
    )

if not crs_mapa.is_projected:
    raise ValueError(
        "La centrografía debe calcularse en un CRS proyectado."
    )

if muestras_centro.crs != crs_mapa:
    muestras_centro = muestras_centro.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Extraer coordenadas XY
# ----------------------------------------------------------

coordenadas = np.column_stack([
    muestras_centro.geometry.x.to_numpy(),
    muestras_centro.geometry.y.to_numpy()
])

mascara_valida = np.isfinite(
    coordenadas
).all(axis=1)

coordenadas = coordenadas[
    mascara_valida
]

if len(coordenadas) < 3:
    raise ValueError(
        "Se requieren al menos tres muestras válidas "
        "para calcular la centrografía."
    )


# ----------------------------------------------------------
# 5. Calcular las medidas de centrografía
# ----------------------------------------------------------

centro_medio = centrography.mean_center(
    coordenadas
)

centro_mediano = centrography.euclidean_median(
    coordenadas
)

distancia_estandar = centrography.std_distance(
    coordenadas
)

semieje_mayor, semieje_menor, rotacion_radianes = (
    centrography.ellipse(coordenadas)
)

rotacion_grados = np.rad2deg(
    rotacion_radianes
)


# ==========================================================
# TABLA 06. MEDIDAS DE CENTROGRAFÍA
# ==========================================================

# ----------------------------------------------------------
# 6. Construir la Tabla 06
# ----------------------------------------------------------

tabla_06 = pd.DataFrame({
    "Indicador": [
        "Centro medio - Este",
        "Centro medio - Norte",
        "Centro mediano - Este",
        "Centro mediano - Norte",
        "Distancia estándar",
        "Semieje mayor de la elipse",
        "Semieje menor de la elipse",
        "Rotación de la elipse"
    ],
    "Valor": [
        centro_medio[0],
        centro_medio[1],
        centro_mediano[0],
        centro_mediano[1],
        distancia_estandar,
        semieje_mayor,
        semieje_menor,
        rotacion_grados
    ],
    "Unidad": [
        "m",
        "m",
        "m",
        "m",
        "m",
        "m",
        "m",
        "grados"
    ]
})


# ----------------------------------------------------------
# 7. Mostrar la Tabla 06
# ----------------------------------------------------------

tabla_06_estilizada = (
    tabla_06.style
    .hide(axis="index")
    .set_caption(
        "Tabla 06. Medidas de centrografía "
        "del patrón de muestreo"
    )
    .format({
        "Valor": "{:,.2f}"
    })
    .set_properties(
        subset=["Valor", "Unidad"],
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
            "props": [
                ("padding", "7px"),
                ("border-bottom", "1px solid #D9D9D9")
            ]
        }
    ])
)

display(tabla_06_estilizada)


# ----------------------------------------------------------
# 8. Guardar la Tabla 06
# ----------------------------------------------------------

ruta_tabla_06 = (
    TABLAS
    / "Tabla_06_Medidas_Centrografia_Muestreo.csv"
)

tabla_06.to_csv(
    ruta_tabla_06,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================================
# FIGURA 07. CENTROGRAFÍA DEL PATRÓN DE MUESTREO
# ==========================================================

# ----------------------------------------------------------
# 9. Preparar nombres municipales
# ----------------------------------------------------------

columnas_nombre = [
    "NOMBRE",
    "NOMBRE_MPIO",
    "MPIO_CNMBR",
    "MUNICIPIO",
    "NOM_MPIO",
    "NOM_MUNIC"
]

columna_nombre = next(
    (
        columna
        for columna in columnas_nombre
        if columna in municipios_centro.columns
    ),
    None
)

if columna_nombre is not None:

    municipios_centro["NOMBRE_MAPA"] = (
        municipios_centro[columna_nombre]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

else:

    municipios_centro["NOMBRE_MAPA"] = ""


# ----------------------------------------------------------
# 10. Corregir nombres abreviados
# ----------------------------------------------------------

nombres_corregidos = {
    "S.BARBA": "Santa Bárbara",
    "C.BOLIV": "Ciudad Bolívar",
    "P.RICO": "Pueblorrico",
    "MONTEBE": "Montebello",
    "TITIRIB": "Titiribí",
    "TAMESIS": "Támesis",
    "JERICO": "Jericó",
    "HISPANI": "Hispania",
    "FREDONI": "Fredonia",
    "ANGELOP": "Angelópolis",
    "CARAMAN": "Caramanta",
    "VALPARA": "Valparaíso",
    "CONCORD": "Concordia",
    "PINTADA": "La Pintada"
}

municipios_centro["NOMBRE_MAPA"] = (
    municipios_centro["NOMBRE_MAPA"]
    .replace(nombres_corregidos)
)

municipios_centro["NOMBRE_MAPA"] = (
    municipios_centro["NOMBRE_MAPA"]
    .apply(
        lambda nombre: (
            nombre.title()
            if nombre and nombre == nombre.upper()
            else nombre
        )
    )
)


# ----------------------------------------------------------
# 11. Calcular límite y extensión
# ----------------------------------------------------------

limite_estudio = municipios_centro.dissolve()

xmin, ymin, xmax, ymax = (
    municipios_centro.total_bounds
)

margen_x = (
    xmax - xmin
) * 0.04

margen_y = (
    ymax - ymin
) * 0.04


# ----------------------------------------------------------
# 12. Crear la Figura 07
# ----------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 9),
    facecolor="white"
)


# ----------------------------------------------------------
# 13. Dibujar municipios
# ----------------------------------------------------------

municipios_centro.plot(
    ax=ax,
    facecolor="#FAFAF7",
    edgecolor="#999999",
    linewidth=0.45,
    zorder=1
)


# ----------------------------------------------------------
# 14. Dibujar las muestras
# ----------------------------------------------------------

muestras_centro.plot(
    ax=ax,
    color="#2F5597",
    marker="o",
    markersize=14,
    edgecolor="white",
    linewidth=0.35,
    alpha=0.82,
    zorder=3
)


# ----------------------------------------------------------
# 15. Dibujar la distancia estándar
# ----------------------------------------------------------

circulo_distancia = Circle(
    xy=centro_medio,
    radius=distancia_estandar,
    facecolor="#D95F5F",
    edgecolor="#B22222",
    linewidth=1.4,
    linestyle=":",
    alpha=0.10,
    zorder=2
)

ax.add_patch(
    circulo_distancia
)


# ----------------------------------------------------------
# 16. Dibujar la elipse estándar
# ----------------------------------------------------------

elipse_estandar = Ellipse(
    xy=centro_medio,
    width=semieje_mayor * 2,
    height=semieje_menor * 2,
    angle=rotacion_grados,
    facecolor="#F4A261",
    edgecolor="#C44E00",
    linewidth=2.0,
    linestyle="--",
    alpha=0.18,
    zorder=4
)

ax.add_patch(
    elipse_estandar
)


# ----------------------------------------------------------
# 17. Dibujar el centro medio
# ----------------------------------------------------------

ax.scatter(
    centro_medio[0],
    centro_medio[1],
    marker="X",
    s=125,
    color="#C00000",
    edgecolor="white",
    linewidth=0.9,
    zorder=7
)


# ----------------------------------------------------------
# 18. Dibujar el centro mediano
# ----------------------------------------------------------

ax.scatter(
    centro_mediano[0],
    centro_mediano[1],
    marker="D",
    s=70,
    color="#2E8B57",
    edgecolor="white",
    linewidth=0.8,
    zorder=7
)


# ----------------------------------------------------------
# 19. Dibujar límite exterior
# ----------------------------------------------------------

limite_estudio.boundary.plot(
    ax=ax,
    color="#111111",
    linewidth=1.55,
    zorder=5
)


# ----------------------------------------------------------
# 20. Añadir nombres municipales
# ----------------------------------------------------------

for _, fila in municipios_centro.iterrows():

    nombre = fila["NOMBRE_MAPA"]

    if not nombre:
        continue

    punto = fila.geometry.representative_point()

    texto = ax.text(
        punto.x,
        punto.y,
        nombre,
        fontsize=5.8,
        ha="center",
        va="center",
        color="#303030",
        zorder=6
    )

    texto.set_path_effects([
        pe.withStroke(
            linewidth=1.9,
            foreground="white"
        )
    ])


# ----------------------------------------------------------
# 21. Configurar extensión y ejes
# ----------------------------------------------------------

ax.set_xlim(
    xmin - margen_x,
    xmax + margen_x
)

ax.set_ylim(
    ymin - margen_y,
    ymax + margen_y
)

ax.set_aspect("equal")

ax.set_xlabel(
    "Coordenada Este (m)",
    fontsize=10
)

ax.set_ylabel(
    "Coordenada Norte (m)",
    fontsize=10
)

ax.xaxis.set_major_locator(
    MaxNLocator(nbins=5)
)

ax.yaxis.set_major_locator(
    MaxNLocator(nbins=6)
)

formato_coordenadas = ScalarFormatter(
    useOffset=False,
    useMathText=False
)

formato_coordenadas.set_scientific(False)

ax.xaxis.set_major_formatter(
    formato_coordenadas
)

ax.yaxis.set_major_formatter(
    formato_coordenadas
)

ax.tick_params(
    axis="both",
    labelsize=8.5,
    direction="out",
    length=4,
    width=0.8
)

ax.ticklabel_format(
    style="plain",
    axis="both",
    useOffset=False
)

ax.grid(False)


# ----------------------------------------------------------
# 22. Añadir flecha norte
# ----------------------------------------------------------

ax.annotate(
    "N",
    xy=(0.945, 0.855),
    xytext=(0.945, 0.745),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=3.3,
        headwidth=9.5,
        headlength=9.5
    ),
    zorder=10
)


# ----------------------------------------------------------
# 23. Añadir barra de escala
# ----------------------------------------------------------

barra_escala = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.22,
    width_fraction=0.008,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={"size": 8},
    border_pad=0.7,
    pad=0.4
)

ax.add_artist(
    barra_escala
)


# ----------------------------------------------------------
# 24. Crear leyenda
# ----------------------------------------------------------

elementos_leyenda = [
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        markerfacecolor="#2F5597",
        markeredgecolor="white",
        markersize=6.5,
        label=f"Muestras (n = {len(muestras_centro):,})"
    ),
    Line2D(
        [0],
        [0],
        marker="X",
        linestyle="none",
        markerfacecolor="#C00000",
        markeredgecolor="white",
        markersize=8,
        label="Centro medio"
    ),
    Line2D(
        [0],
        [0],
        marker="D",
        linestyle="none",
        markerfacecolor="#2E8B57",
        markeredgecolor="white",
        markersize=6.5,
        label="Centro mediano"
    ),
    Line2D(
        [0],
        [0],
        color="#B22222",
        linewidth=1.5,
        linestyle=":",
        label="Distancia estándar"
    ),
    Line2D(
        [0],
        [0],
        color="#C44E00",
        linewidth=2.0,
        linestyle="--",
        label="Elipse estándar"
    )
]

leyenda = ax.legend(
    handles=elementos_leyenda,
    loc="upper right",
    bbox_to_anchor=(0.985, 0.995),
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.96,
    fontsize=8.3,
    title="Medidas de centrografía",
    title_fontsize=9,
    borderpad=0.8,
    labelspacing=0.55
)

leyenda._legend_box.align = "left"


# ----------------------------------------------------------
# 25. Añadir CRS
# ----------------------------------------------------------

epsg_mapa = crs_mapa.to_epsg()

if epsg_mapa is not None:
    texto_crs = f"CRS: EPSG:{epsg_mapa}"
else:
    texto_crs = f"CRS: {crs_mapa.name}"

ax.text(
    0.985,
    0.018,
    texto_crs,
    transform=ax.transAxes,
    fontsize=7.3,
    ha="right",
    va="bottom",
    color="#333333",
    bbox=dict(
        facecolor="white",
        edgecolor="#888888",
        linewidth=0.50,
        alpha=0.92,
        boxstyle="round,pad=0.25"
    ),
    zorder=10
)


# ----------------------------------------------------------
# 26. Configurar marco
# ----------------------------------------------------------

for borde in ax.spines.values():

    borde.set_visible(True)
    borde.set_color("#333333")
    borde.set_linewidth(0.85)


# ----------------------------------------------------------
# 27. Añadir fuente
# ----------------------------------------------------------

fig.text(
    0.98,
    0.018,
    (
        "Fuente: base geoquímica de Cu y límites municipales. "
        "Cálculos y elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 28. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.11,
    right=0.97,
    bottom=0.11,
    top=0.98
)


# ----------------------------------------------------------
# 29. Guardar la Figura 07
# ----------------------------------------------------------

ruta_figura_07 = (
    FIGURAS
    / "Figura_07_Centrografia_Patron_Muestreo.png"
)

fig.savefig(
    ruta_figura_07,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)


# ----------------------------------------------------------
# 30. Confirmar resultados
# ----------------------------------------------------------

print("=" * 72)
print("TABLA 06 Y FIGURA 07 GENERADAS CORRECTAMENTE")
print("=" * 72)

print(
    f"Muestras utilizadas: "
    f"{len(muestras_centro):,}"
)

print(
    f"Centro medio: "
    f"E={centro_medio[0]:,.2f} m | "
    f"N={centro_medio[1]:,.2f} m"
)

print(
    f"Centro mediano: "
    f"E={centro_mediano[0]:,.2f} m | "
    f"N={centro_mediano[1]:,.2f} m"
)

print(
    f"Distancia estándar: "
    f"{distancia_estandar:,.2f} m"
)

print(
    f"Rotación de la elipse: "
    f"{rotacion_grados:,.2f}°"
)

print("-" * 72)
print(f"CSV: {ruta_tabla_06}")
print(f"PNG: {ruta_figura_07}")
print("=" * 72)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 88
# ==========================================================
# ==========================================================
# TABLA 07. PARÁMETROS DE LA ESTIMACIÓN KERNEL
# ==========================================================

import numpy as np
import pandas as pd
import geopandas as gpd

from scipy.stats import gaussian_kde


# ----------------------------------------------------------
# 1. Preparar las capas
# ----------------------------------------------------------

muestras_kernel = muestras.copy()
municipios_kernel = municipios.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

muestras_kernel = muestras_kernel[
    muestras_kernel.geometry.notna()
    & ~muestras_kernel.geometry.is_empty
].copy()

municipios_kernel = municipios_kernel[
    municipios_kernel.geometry.notna()
    & ~municipios_kernel.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Verificar y homologar el CRS
# ----------------------------------------------------------

crs_kernel = municipios_kernel.crs

if crs_kernel is None:
    raise ValueError(
        "La capa de municipios no tiene un CRS definido."
    )

if muestras_kernel.crs is None:
    raise ValueError(
        "La capa de muestras no tiene un CRS definido."
    )

if not crs_kernel.is_projected:
    raise ValueError(
        "La densidad Kernel debe calcularse en un CRS "
        "proyectado con unidades lineales."
    )

if muestras_kernel.crs != crs_kernel:
    muestras_kernel = muestras_kernel.to_crs(
        crs_kernel
    )


# ----------------------------------------------------------
# 4. Crear el polígono del área de análisis
# ----------------------------------------------------------

poligono_kernel = (
    municipios_kernel
    .geometry
    .union_all()
)


# ----------------------------------------------------------
# 5. Verificar que las muestras estén dentro del polígono
# ----------------------------------------------------------

mascara_kernel = muestras_kernel.geometry.apply(
    lambda geometria: poligono_kernel.covers(geometria)
)

if not mascara_kernel.all():

    cantidad_externa = int(
        (~mascara_kernel).sum()
    )

    print(
        f"Advertencia: se excluyeron {cantidad_externa} "
        "muestras externas al polígono."
    )

    muestras_kernel = muestras_kernel[
        mascara_kernel
    ].copy()


# ----------------------------------------------------------
# 6. Extraer las coordenadas
# ----------------------------------------------------------

x_kernel = muestras_kernel.geometry.x.to_numpy()
y_kernel = muestras_kernel.geometry.y.to_numpy()

mascara_coordenadas = (
    np.isfinite(x_kernel)
    & np.isfinite(y_kernel)
)

x_kernel = x_kernel[
    mascara_coordenadas
]

y_kernel = y_kernel[
    mascara_coordenadas
]

if len(x_kernel) < 3:
    raise ValueError(
        "Se requieren al menos tres muestras válidas "
        "para calcular la densidad Kernel."
    )

coordenadas_kernel = np.vstack([
    x_kernel,
    y_kernel
])


# ----------------------------------------------------------
# 7. Ajustar el modelo Kernel
# ----------------------------------------------------------
# Kernel gaussiano y regla de Scott para seleccionar
# automáticamente el ancho de banda.

modelo_kernel = gaussian_kde(
    coordenadas_kernel,
    bw_method="scott"
)

factor_banda_kernel = float(
    modelo_kernel.factor
)

desviacion_este = np.std(
    x_kernel,
    ddof=1
)

desviacion_norte = np.std(
    y_kernel,
    ddof=1
)

banda_este_kernel = (
    factor_banda_kernel
    * desviacion_este
)

banda_norte_kernel = (
    factor_banda_kernel
    * desviacion_norte
)

banda_promedio_kernel = np.sqrt(
    banda_este_kernel
    * banda_norte_kernel
)


# ----------------------------------------------------------
# 8. Definir la resolución de la malla
# ----------------------------------------------------------

RESOLUCION_KERNEL = 300

xmin_kernel, ymin_kernel, xmax_kernel, ymax_kernel = (
    municipios_kernel.total_bounds
)

tamano_celda_este = (
    xmax_kernel - xmin_kernel
) / (RESOLUCION_KERNEL - 1)

tamano_celda_norte = (
    ymax_kernel - ymin_kernel
) / (RESOLUCION_KERNEL - 1)

tamano_celda_promedio = (
    tamano_celda_este
    + tamano_celda_norte
) / 2


# ----------------------------------------------------------
# 9. Construir la Tabla 07
# ----------------------------------------------------------

tabla_07 = pd.DataFrame({
    "Parámetro": [
        "Número de muestras",
        "Tipo de Kernel",
        "Método de selección de banda",
        "Factor de banda",
        "Banda efectiva Este",
        "Banda efectiva Norte",
        "Banda efectiva promedio",
        "Resolución de la malla",
        "Tamaño aproximado de celda",
        "Variable representada"
    ],

    "Valor": [
        len(muestras_kernel),
        "Gaussiano",
        "Regla de Scott",
        factor_banda_kernel,
        banda_este_kernel,
        banda_norte_kernel,
        banda_promedio_kernel,
        f"{RESOLUCION_KERNEL} × {RESOLUCION_KERNEL}",
        tamano_celda_promedio,
        "Densidad relativa de ubicaciones de muestreo"
    ],

    "Unidad": [
        "muestras",
        "—",
        "—",
        "adimensional",
        "m",
        "m",
        "m",
        "celdas",
        "m",
        "0–1"
    ]
})


# ----------------------------------------------------------
# 10. Mostrar la Tabla 07
# ----------------------------------------------------------

def formato_valor_kernel(valor):

    if isinstance(
        valor,
        (int, float, np.integer, np.floating)
    ):
        return f"{valor:,.2f}"

    return str(valor)


tabla_07_estilizada = (
    tabla_07.style
    .hide(axis="index")
    .set_caption(
        "Tabla 07. Parámetros de la estimación Kernel "
        "del patrón de muestreo"
    )
    .format({
        "Valor": formato_valor_kernel
    })
    .set_properties(
        subset=[
            "Valor",
            "Unidad"
        ],
        **{
            "text-align": "center"
        }
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
            "props": [
                ("padding", "7px"),
                ("border-bottom", "1px solid #D9D9D9"),
                ("vertical-align", "top")
            ]
        }
    ])
)

display(tabla_07_estilizada)


# ----------------------------------------------------------
# 11. Guardar únicamente en CSV
# ----------------------------------------------------------

ruta_tabla_07 = (
    TABLAS
    / "Tabla_07_Parametros_Densidad_Kernel.csv"
)

tabla_07.to_csv(
    ruta_tabla_07,
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 12. Confirmar resultados
# ----------------------------------------------------------

print("=" * 72)
print("TABLA 07 GENERADA CORRECTAMENTE")
print("=" * 72)

print(
    f"Muestras utilizadas        : "
    f"{len(muestras_kernel):,}"
)

print(
    f"Factor de banda de Scott   : "
    f"{factor_banda_kernel:.6f}"
)

print(
    f"Banda efectiva Este        : "
    f"{banda_este_kernel:,.2f} m"
)

print(
    f"Banda efectiva Norte       : "
    f"{banda_norte_kernel:,.2f} m"
)

print(
    f"Banda efectiva promedio    : "
    f"{banda_promedio_kernel:,.2f} m"
)

print(
    f"Tamaño aproximado de celda : "
    f"{tamano_celda_promedio:,.2f} m"
)

print("-" * 72)
print(f"CSV: {ruta_tabla_07}")
print("=" * 72)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 89
# ==========================================================
# ==========================================================
# FIGURA 09. DENSIDAD KERNEL DEL PATRÓN DE MUESTREO
# ==========================================================

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter


# ----------------------------------------------------------
# 1. Verificar que se ejecutó previamente la Tabla 09
# ----------------------------------------------------------

variables_kernel_requeridas = [
    "muestras_kernel",
    "municipios_kernel",
    "poligono_kernel",
    "modelo_kernel",
    "x_kernel",
    "y_kernel",
    "RESOLUCION_KERNEL",
    "crs_kernel"
]

variables_faltantes = [
    variable
    for variable in variables_kernel_requeridas
    if variable not in globals()
]

if variables_faltantes:
    raise NameError(
        "Primero debes ejecutar la celda de la Tabla 07. "
        f"Variables faltantes: {variables_faltantes}"
    )


# ----------------------------------------------------------
# 2. Crear la malla de evaluación
# ----------------------------------------------------------

xmin_kernel, ymin_kernel, xmax_kernel, ymax_kernel = (
    municipios_kernel.total_bounds
)

x_malla_kernel = np.linspace(
    xmin_kernel,
    xmax_kernel,
    RESOLUCION_KERNEL
)

y_malla_kernel = np.linspace(
    ymin_kernel,
    ymax_kernel,
    RESOLUCION_KERNEL
)

xx_kernel, yy_kernel = np.meshgrid(
    x_malla_kernel,
    y_malla_kernel
)

posiciones_kernel = np.vstack([
    xx_kernel.ravel(),
    yy_kernel.ravel()
])


# ----------------------------------------------------------
# 3. Evaluar la densidad Kernel
# ----------------------------------------------------------

densidad_kernel = modelo_kernel(
    posiciones_kernel
).reshape(
    xx_kernel.shape
)


# ----------------------------------------------------------
# 4. Crear máscara exacta del área de análisis
# ----------------------------------------------------------

try:

    from shapely import intersects_xy

    mascara_poligono_kernel = intersects_xy(
        poligono_kernel,
        xx_kernel,
        yy_kernel
    )

except ImportError:

    puntos_malla_kernel = gpd.GeoSeries(
        gpd.points_from_xy(
            xx_kernel.ravel(),
            yy_kernel.ravel()
        ),
        crs=crs_kernel
    )

    mascara_poligono_kernel = (
        puntos_malla_kernel.within(
            poligono_kernel
        )
        | puntos_malla_kernel.touches(
            poligono_kernel
        )
    ).to_numpy().reshape(
        xx_kernel.shape
    )


# ----------------------------------------------------------
# 5. Recortar la superficie al polígono
# ----------------------------------------------------------

densidad_kernel_recortada = np.where(
    mascara_poligono_kernel,
    densidad_kernel,
    np.nan
)


# ----------------------------------------------------------
# 6. Normalizar entre 0 y 1
# ----------------------------------------------------------
# La normalización facilita la comparación visual dentro
# del área y no representa concentraciones de cobre.

densidad_kernel_maxima = np.nanmax(
    densidad_kernel_recortada
)

if (
    not np.isfinite(densidad_kernel_maxima)
    or densidad_kernel_maxima <= 0
):
    raise ValueError(
        "No fue posible obtener una densidad Kernel válida."
    )

densidad_kernel_relativa = (
    densidad_kernel_recortada
    / densidad_kernel_maxima
)


# ----------------------------------------------------------
# 7. Preparar nombres municipales
# ----------------------------------------------------------

columnas_nombre = [
    "NOMBRE",
    "NOMBRE_MPIO",
    "MPIO_CNMBR",
    "MUNICIPIO",
    "NOM_MPIO",
    "NOM_MUNIC"
]

columna_nombre = next(
    (
        columna
        for columna in columnas_nombre
        if columna in municipios_kernel.columns
    ),
    None
)

if columna_nombre is not None:

    municipios_kernel["NOMBRE_MAPA"] = (
        municipios_kernel[columna_nombre]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

else:

    municipios_kernel["NOMBRE_MAPA"] = ""


nombres_corregidos = {
    "S.BARBA": "Santa Bárbara",
    "C.BOLIV": "Ciudad Bolívar",
    "P.RICO": "Pueblorrico",
    "MONTEBE": "Montebello",
    "TITIRIB": "Titiribí",
    "TAMESIS": "Támesis",
    "JERICO": "Jericó",
    "HISPANI": "Hispania",
    "FREDONI": "Fredonia",
    "ANGELOP": "Angelópolis",
    "CARAMAN": "Caramanta",
    "VALPARA": "Valparaíso",
    "CONCORD": "Concordia",
    "PINTADA": "La Pintada"
}

municipios_kernel["NOMBRE_MAPA"] = (
    municipios_kernel["NOMBRE_MAPA"]
    .replace(
        nombres_corregidos
    )
)

municipios_kernel["NOMBRE_MAPA"] = (
    municipios_kernel["NOMBRE_MAPA"]
    .apply(
        lambda nombre: nombre.title()
        if nombre and nombre == nombre.upper()
        else nombre
    )
)


# ----------------------------------------------------------
# 8. Crear límite exterior
# ----------------------------------------------------------

limite_kernel = gpd.GeoDataFrame(
    geometry=[
        poligono_kernel
    ],
    crs=crs_kernel
)


# ----------------------------------------------------------
# 9. Crear la figura
# ----------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 9),
    facecolor="white"
)


# ----------------------------------------------------------
# 10. Representar la densidad Kernel
# ----------------------------------------------------------

imagen_kernel = ax.imshow(
    densidad_kernel_relativa,
    origin="lower",
    extent=[
        xmin_kernel,
        xmax_kernel,
        ymin_kernel,
        ymax_kernel
    ],
    cmap="YlOrRd",
    interpolation="bilinear",
    vmin=0,
    vmax=1,
    alpha=0.88,
    zorder=1
)


# ----------------------------------------------------------
# 11. Dibujar límites municipales
# ----------------------------------------------------------

municipios_kernel.boundary.plot(
    ax=ax,
    color="#555555",
    linewidth=0.50,
    alpha=0.82,
    zorder=3
)


# ----------------------------------------------------------
# 12. Dibujar las muestras utilizadas
# ----------------------------------------------------------

muestras_kernel.plot(
    ax=ax,
    color="#303030",
    marker="o",
    markersize=5,
    edgecolor="none",
    alpha=0.35,
    zorder=4
)


# ----------------------------------------------------------
# 13. Dibujar el límite exterior
# ----------------------------------------------------------

limite_kernel.boundary.plot(
    ax=ax,
    color="#111111",
    linewidth=1.60,
    zorder=5
)


# ----------------------------------------------------------
# 14. Añadir nombres municipales
# ----------------------------------------------------------

for _, fila in municipios_kernel.iterrows():

    nombre = fila["NOMBRE_MAPA"]

    if not nombre:
        continue

    punto_etiqueta = (
        fila.geometry
        .representative_point()
    )

    texto = ax.text(
        punto_etiqueta.x,
        punto_etiqueta.y,
        nombre,
        fontsize=5.5,
        ha="center",
        va="center",
        color="#202020",
        zorder=6
    )

    texto.set_path_effects([
        pe.withStroke(
            linewidth=1.9,
            foreground="white"
        )
    ])


# ----------------------------------------------------------
# 15. Configurar extensión y coordenadas
# ----------------------------------------------------------

margen_x_kernel = (
    xmax_kernel - xmin_kernel
) * 0.025

margen_y_kernel = (
    ymax_kernel - ymin_kernel
) * 0.025

ax.set_xlim(
    xmin_kernel - margen_x_kernel,
    xmax_kernel + margen_x_kernel
)

ax.set_ylim(
    ymin_kernel - margen_y_kernel,
    ymax_kernel + margen_y_kernel
)

ax.set_aspect("equal")

ax.set_xlabel(
    "Coordenada Este (m)",
    fontsize=10
)

ax.set_ylabel(
    "Coordenada Norte (m)",
    fontsize=10
)

ax.xaxis.set_major_locator(
    MaxNLocator(nbins=5)
)

ax.yaxis.set_major_locator(
    MaxNLocator(nbins=6)
)

formato_coordenadas = ScalarFormatter(
    useOffset=False,
    useMathText=False
)

formato_coordenadas.set_scientific(
    False
)

ax.xaxis.set_major_formatter(
    formato_coordenadas
)

ax.yaxis.set_major_formatter(
    formato_coordenadas
)

ax.tick_params(
    axis="both",
    labelsize=8.5,
    direction="out",
    length=4,
    width=0.8
)

ax.ticklabel_format(
    style="plain",
    axis="both",
    useOffset=False
)

ax.grid(False)


# ----------------------------------------------------------
# 16. Añadir barra de colores
# ----------------------------------------------------------

barra_color_kernel = fig.colorbar(
    imagen_kernel,
    ax=ax,
    fraction=0.038,
    pad=0.025,
    shrink=0.82
)

barra_color_kernel.set_label(
    "Intensidad relativa del muestreo",
    fontsize=9
)

barra_color_kernel.ax.tick_params(
    labelsize=8
)


# ----------------------------------------------------------
# 17. Añadir leyenda
# ----------------------------------------------------------

leyenda_kernel = ax.legend(
    handles=[
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            markerfacecolor="#303030",
            markeredgecolor="none",
            markersize=6.5,
            label=(
                f"Ubicaciones de muestreo: "
                f"{len(muestras_kernel):,}"
            )
        )
    ],
    loc="upper right",
    bbox_to_anchor=(0.985, 0.995),
    frameon=True,
    facecolor="white",
    edgecolor="#888888",
    framealpha=0.96,
    fontsize=8.3,
    title="Patrón de muestreo",
    title_fontsize=9
)

leyenda_kernel._legend_box.align = "left"


# ----------------------------------------------------------
# 18. Añadir flecha norte
# ----------------------------------------------------------

ax.annotate(
    "N",
    xy=(0.945, 0.855),
    xytext=(0.945, 0.745),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=3.3,
        headwidth=9.5,
        headlength=9.5
    ),
    zorder=10
)


# ----------------------------------------------------------
# 19. Añadir barra de escala
# ----------------------------------------------------------

barra_escala_kernel = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.22,
    width_fraction=0.008,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={
        "size": 8
    },
    border_pad=0.7,
    pad=0.4
)

ax.add_artist(
    barra_escala_kernel
)


# ----------------------------------------------------------
# 20. Añadir CRS
# ----------------------------------------------------------

epsg_kernel = crs_kernel.to_epsg()

if epsg_kernel is not None:

    texto_crs_kernel = (
        f"CRS: EPSG:{epsg_kernel}"
    )

else:

    texto_crs_kernel = (
        f"CRS: {crs_kernel.name}"
    )

ax.text(
    0.985,
    0.018,
    texto_crs_kernel,
    transform=ax.transAxes,
    fontsize=7.3,
    ha="right",
    va="bottom",
    color="#333333",
    bbox=dict(
        facecolor="white",
        edgecolor="#888888",
        linewidth=0.50,
        alpha=0.92,
        boxstyle="round,pad=0.25"
    ),
    zorder=10
)


# ----------------------------------------------------------
# 21. Configurar marco
# ----------------------------------------------------------

for borde in ax.spines.values():

    borde.set_visible(True)
    borde.set_color("#333333")
    borde.set_linewidth(0.85)


# ----------------------------------------------------------
# 22. Añadir fuente
# ----------------------------------------------------------

fig.text(
    0.98,
    0.018,
    (
        "Fuente: muestras geoquímicas seleccionadas dentro "
        "del área de análisis y cartografía municipal. "
        "Estimación y elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 23. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.10,
    right=0.91,
    bottom=0.11,
    top=0.98
)


# ----------------------------------------------------------
# 24. Guardar únicamente en PNG
# ----------------------------------------------------------

ruta_figura_08 = (
    FIGURAS
    / "Figura_09_Densidad_Kernel_Patron_Muestreo.png"
)

fig.savefig(
    ruta_figura_08,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)


# ----------------------------------------------------------
# 25. Confirmar resultado
# ----------------------------------------------------------

print("=" * 72)
print("FIGURA 09 GENERADA CORRECTAMENTE")
print("=" * 72)

print(
    f"Muestras utilizadas: "
    f"{len(muestras_kernel):,}"
)

print(
    f"Densidad mínima relativa: "
    f"{np.nanmin(densidad_kernel_relativa):.4f}"
)

print(
    f"Densidad máxima relativa: "
    f"{np.nanmax(densidad_kernel_relativa):.4f}"
)

print("-" * 72)
print(f"PNG: {ruta_figura_08}")
print("=" * 72)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 92
# ==========================================================
# ==========================================================
# TABLA 08. ANÁLISIS DEL VECINO MÁS CERCANO
# ==========================================================

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from scipy.stats import norm


# ----------------------------------------------------------
# 1. Preparar las capas
# ----------------------------------------------------------

muestras_ann = muestras.copy()
municipios_ann = municipios.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

muestras_ann = muestras_ann[
    muestras_ann.geometry.notna()
    & ~muestras_ann.geometry.is_empty
].copy()

municipios_ann = municipios_ann[
    municipios_ann.geometry.notna()
    & ~municipios_ann.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Verificar y homologar el CRS
# ----------------------------------------------------------

crs_ann = municipios_ann.crs

if crs_ann is None:
    raise ValueError(
        "La capa de municipios no tiene un CRS definido."
    )

if muestras_ann.crs is None:
    raise ValueError(
        "La capa de muestras no tiene un CRS definido."
    )

if not crs_ann.is_projected:
    raise ValueError(
        "El análisis del vecino más cercano debe realizarse "
        "en un CRS proyectado con unidades lineales."
    )

if muestras_ann.crs != crs_ann:
    muestras_ann = muestras_ann.to_crs(crs_ann)


# ----------------------------------------------------------
# 4. Crear el polígono del área de análisis
# ----------------------------------------------------------

poligono_ann = municipios_ann.geometry.union_all()


# ----------------------------------------------------------
# 5. Confirmar que las muestras estén dentro del polígono
# ----------------------------------------------------------

mascara_dentro_ann = muestras_ann.geometry.apply(
    lambda geometria: poligono_ann.covers(geometria)
)

if not mascara_dentro_ann.all():

    cantidad_externa = int(
        (~mascara_dentro_ann).sum()
    )

    print(
        f"Advertencia: se excluyeron {cantidad_externa} "
        "muestras ubicadas fuera del área."
    )

    muestras_ann = muestras_ann[
        mascara_dentro_ann
    ].copy()


# ----------------------------------------------------------
# 6. Extraer coordenadas válidas
# ----------------------------------------------------------

coordenadas_ann = np.column_stack([
    muestras_ann.geometry.x.to_numpy(),
    muestras_ann.geometry.y.to_numpy()
])

mascara_valida_ann = np.isfinite(
    coordenadas_ann
).all(axis=1)

coordenadas_ann = coordenadas_ann[
    mascara_valida_ann
]

numero_muestras_ann = len(coordenadas_ann)

if numero_muestras_ann < 2:
    raise ValueError(
        "Se requieren al menos dos muestras válidas "
        "para calcular el vecino más cercano."
    )


# ----------------------------------------------------------
# 7. Calcular la distancia al vecino más cercano
# ----------------------------------------------------------
# Se solicitan dos vecinos porque el primero corresponde
# al mismo punto, cuya distancia es igual a cero.

modelo_vecinos = NearestNeighbors(
    n_neighbors=2,
    metric="euclidean"
)

modelo_vecinos.fit(
    coordenadas_ann
)

distancias_ann, indices_ann = modelo_vecinos.kneighbors(
    coordenadas_ann
)

# Segunda columna: distancia al vecino distinto más cercano
distancias_vecino = distancias_ann[:, 1]

distancia_media_observada = float(
    np.mean(distancias_vecino)
)


# ----------------------------------------------------------
# 8. Calcular área y densidad del patrón
# ----------------------------------------------------------

area_m2_ann = float(
    poligono_ann.area
)

area_km2_ann = (
    area_m2_ann / 1_000_000
)

densidad_m2_ann = (
    numero_muestras_ann / area_m2_ann
)

densidad_km2_ann = (
    numero_muestras_ann / area_km2_ann
)


# ----------------------------------------------------------
# 9. Calcular distancia esperada bajo CSR
# ----------------------------------------------------------
# Para un patrón espacial completamente aleatorio:
#
# E(r) = 1 / (2 * sqrt(lambda))
#
# donde lambda es la densidad de puntos por unidad de área.

distancia_media_esperada = (
    0.5 / np.sqrt(densidad_m2_ann)
)


# ----------------------------------------------------------
# 10. Calcular índice R de Clark y Evans
# ----------------------------------------------------------

indice_r = (
    distancia_media_observada
    / distancia_media_esperada
)


# ----------------------------------------------------------
# 11. Calcular error estándar, Z y valor p
# ----------------------------------------------------------
# Error estándar clásico del análisis ANN:
#
# SE = 0.26136 * sqrt(A) / n

error_estandar_ann = (
    0.26136
    * np.sqrt(area_m2_ann)
    / numero_muestras_ann
)

z_score_ann = (
    distancia_media_observada
    - distancia_media_esperada
) / error_estandar_ann

valor_p_ann = float(
    2 * norm.sf(
        abs(z_score_ann)
    )
)


# ----------------------------------------------------------
# 12. Clasificar el patrón espacial
# ----------------------------------------------------------

nivel_significancia = 0.05

if valor_p_ann >= nivel_significancia:

    clasificacion_ann = (
        "No diferente de un patrón aleatorio"
    )

    interpretacion_ann = (
        "No existe evidencia estadística suficiente "
        "para diferenciar el patrón observado de CSR."
    )

elif indice_r < 1:

    clasificacion_ann = "Agrupado"

    interpretacion_ann = (
        "La distancia observada es menor que la esperada "
        "bajo aleatoriedad espacial."
    )

else:

    clasificacion_ann = "Regular o disperso"

    interpretacion_ann = (
        "La distancia observada es mayor que la esperada "
        "bajo aleatoriedad espacial."
    )


# ----------------------------------------------------------
# 13. Construir la Tabla 08
# ----------------------------------------------------------

tabla_08 = pd.DataFrame({
    "Parámetro": [
        "Número de muestras",
        "Área de análisis",
        "Densidad media del muestreo",
        "Distancia media observada",
        "Distancia media esperada bajo CSR",
        "Índice del vecino más cercano (R)",
        "Error estándar",
        "Estadístico Z",
        "Valor p",
        "Clasificación del patrón"
    ],

    "Valor": [
        numero_muestras_ann,
        area_km2_ann,
        densidad_km2_ann,
        distancia_media_observada,
        distancia_media_esperada,
        indice_r,
        error_estandar_ann,
        z_score_ann,
        valor_p_ann,
        clasificacion_ann
    ],

    "Unidad": [
        "muestras",
        "km²",
        "muestras/km²",
        "m",
        "m",
        "adimensional",
        "m",
        "adimensional",
        "adimensional",
        "—"
    ],

    "Interpretación": [
        "Total de muestras utilizadas en el análisis.",
        "Superficie del polígono del área de estudio.",
        "Número promedio de muestras por km².",
        "Distancia promedio entre cada muestra y su vecino más cercano.",
        "Distancia esperada si las muestras estuvieran distribuidas aleatoriamente.",
        "R < 1: agrupado; R ≈ 1: aleatorio; R > 1: regular.",
        "Medida utilizada para calcular el estadístico Z.",
        "Indica qué tan diferente es el patrón observado respecto al aleatorio.",
        "Permite establecer si la diferencia es estadísticamente significativa.",
        interpretacion_ann
    ]
})


# ----------------------------------------------------------
# 14. Mostrar la Tabla 08
# ----------------------------------------------------------

def formato_valor_ann(valor):

    if isinstance(
        valor,
        (int, np.integer)
    ):
        return f"{valor:,}"

    if isinstance(
        valor,
        (float, np.floating)
    ):

        if abs(valor) < 0.001 and valor != 0:
            return f"{valor:.3e}"

        return f"{valor:,.4f}"

    return str(valor)


tabla_08_estilizada = (
    tabla_08.style
    .hide(axis="index")
    .set_caption(
        "Tabla 08. Resultados del análisis "
        "del vecino más cercano"
    )
    .format({
        "Valor": formato_valor_ann
    })
    .set_properties(
        subset=[
            "Valor",
            "Unidad"
        ],
        **{
            "text-align": "center"
        }
    )
    .set_properties(
        subset=[
            "Interpretación"
        ],
        **{
            "text-align": "left"
        }
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
            "props": [
                ("padding", "7px"),
                ("border-bottom", "1px solid #D9D9D9"),
                ("vertical-align", "top")
            ]
        }
    ])
)

display(tabla_08_estilizada)


# ----------------------------------------------------------
# 15. Guardar la Tabla 08 únicamente en CSV
# ----------------------------------------------------------

ruta_tabla_08 = (
    TABLAS
    / "Tabla_08_Analisis_Vecino_Mas_Cercano.csv"
)

tabla_08.to_csv(
    ruta_tabla_08,
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 16. Mostrar resumen del resultado
# ----------------------------------------------------------

print("=" * 74)
print("TABLA 08 GENERADA CORRECTAMENTE")
print("=" * 74)

print(
    f"Muestras analizadas          : "
    f"{numero_muestras_ann:,}"
)

print(
    f"Área de análisis             : "
    f"{area_km2_ann:,.2f} km²"
)

print(
    f"Distancia media observada    : "
    f"{distancia_media_observada:,.2f} m"
)

print(
    f"Distancia media esperada     : "
    f"{distancia_media_esperada:,.2f} m"
)

print(
    f"Índice R                     : "
    f"{indice_r:.4f}"
)

print(
    f"Estadístico Z                : "
    f"{z_score_ann:.4f}"
)

print(
    f"Valor p                      : "
    f"{valor_p_ann:.6g}"
)

print(
    f"Clasificación                : "
    f"{clasificacion_ann}"
)

print("-" * 74)
print(f"CSV: {ruta_tabla_08}")
print("=" * 74)


print("\n" + "=" * 72)
print("04_patron_muestreo.py COMPLETADO")
print("=" * 72)
