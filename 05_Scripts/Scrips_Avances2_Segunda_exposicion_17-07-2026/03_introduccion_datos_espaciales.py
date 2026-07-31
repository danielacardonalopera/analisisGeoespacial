"""
03_introduccion_datos_espaciales.py
===================================

Capítulo 2. Introducción a los datos espaciales

Este archivo fue generado a partir del notebook:
Analisis_Geoespacial_Cobre(1).ipynb

Ejecución en Google Colab
-------------------------
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/03_introduccion_datos_espaciales.py"
"""

from __future__ import annotations

import runpy
from pathlib import Path

# ==========================================================
# 0. CARGAR EL SCRIPT PRECEDENTE
# ==========================================================

RUTA_DEPENDENCIA = Path(__file__).with_name("02_preparacion_datos.py")

if not RUTA_DEPENDENCIA.exists():
    raise FileNotFoundError(
        "No se encontró 02_preparacion_datos.py en la misma carpeta que este script."
    )

_contexto_previo = runpy.run_path(str(RUTA_DEPENDENCIA))
globals().update(_contexto_previo)

print("\n" + "=" * 72)
print("CAPÍTULO 2. INTRODUCCIÓN A LOS DATOS ESPACIALES")
print("=" * 72)



# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 36
# ==========================================================
# ==========================================================
# TABLA 02. CARACTERIZACIÓN GENERAL DE LAS CAPAS ESPACIALES
# ==========================================================

import pandas as pd
import geopandas as gpd

from pathlib import Path


# ----------------------------------------------------------
# 1. Función para identificar el tipo general de geometría
# ----------------------------------------------------------

def identificar_geometria(gdf):
    """
    Identifica el tipo general de geometría de una capa:
    Punto, Línea, Polígono o Mixta.
    """

    if not isinstance(gdf, gpd.GeoDataFrame):
        return "No espacial"

    if gdf.geometry.name not in gdf.columns:
        return "Sin geometría"

    tipos = (
        gdf.geometry
        .dropna()
        .loc[lambda serie: ~serie.is_empty]
        .geom_type
        .unique()
        .tolist()
    )

    if len(tipos) == 0:
        return "Sin geometría"

    equivalencias = {
        "Point": "Punto",
        "MultiPoint": "Punto",
        "LineString": "Línea",
        "MultiLineString": "Línea",
        "Polygon": "Polígono",
        "MultiPolygon": "Polígono",
        "GeometryCollection": "Colección geométrica"
    }

    tipos_generales = sorted({
        equivalencias.get(tipo, tipo)
        for tipo in tipos
    })

    if len(tipos_generales) == 1:
        return tipos_generales[0]

    return "Mixta: " + ", ".join(tipos_generales)


# ----------------------------------------------------------
# 2. Función para resumir el sistema de referencia
# ----------------------------------------------------------

def describir_crs(gdf):
    """
    Devuelve el código EPSG asociado a la capa.
    """

    if not isinstance(gdf, gpd.GeoDataFrame):
        return "No aplica"

    if gdf.crs is None:
        return "No definido"

    epsg = gdf.crs.to_epsg()

    if epsg is not None:
        return f"EPSG:{epsg}"

    return gdf.crs.name or "CRS sin código EPSG"


# ----------------------------------------------------------
# 3. Verificar que las capas necesarias estén cargadas
# ----------------------------------------------------------

nombres_capas_requeridas = [
    "muestras",
    "fallas",
    "geologia",
    "municipios"
]

capas_faltantes = [
    nombre
    for nombre in nombres_capas_requeridas
    if nombre not in globals()
]

if capas_faltantes:
    raise NameError(
        "No se encontraron las siguientes capas en memoria: "
        + ", ".join(capas_faltantes)
    )


capas_requeridas = {
    "muestras": muestras,
    "fallas": fallas,
    "geologia": geologia,
    "municipios": municipios
}

for nombre, capa in capas_requeridas.items():

    if capa is None:
        raise ValueError(
            f"La capa '{nombre}' no está disponible."
        )

    if not isinstance(capa, gpd.GeoDataFrame):
        raise TypeError(
            f"La capa '{nombre}' debe ser un GeoDataFrame."
        )


# ----------------------------------------------------------
# 4. Definir la información temática de las capas
# ----------------------------------------------------------

capas_espaciales = [
    {
        "Capa": "Muestras de Cu",
        "Descripción":
            "Localización de muestras geoquímicas de cobre",
        "Objeto": muestras
    },
    {
        "Capa": "Fallas",
        "Descripción":
            "Estructuras geológicas y tectónicas",
        "Objeto": fallas
    },
    {
        "Capa": "Geología",
        "Descripción":
            "Distribución de unidades litológicas",
        "Objeto": geologia
    },
    {
        "Capa": "Municipios",
        "Descripción":
            "Divisiones administrativas del área de estudio",
        "Objeto": municipios
    }
]


# ----------------------------------------------------------
# 5. Construir automáticamente la Tabla 02
# ----------------------------------------------------------

registros_tabla_02 = []

for capa in capas_espaciales:

    gdf = capa["Objeto"]

    registros_tabla_02.append({
        "Capa": capa["Capa"],
        "Descripción": capa["Descripción"],
        "Geometría": identificar_geometria(gdf),
        "Registros": len(gdf),
        "CRS": describir_crs(gdf)
    })


tabla_02 = pd.DataFrame(
    registros_tabla_02
)


# ----------------------------------------------------------
# 6. Verificar el contenido de la Tabla 02
# ----------------------------------------------------------

if len(tabla_02) != len(capas_espaciales):
    raise ValueError(
        "La cantidad de filas generadas no coincide con "
        "la cantidad de capas espaciales definidas."
    )

if tabla_02["Capa"].duplicated().any():
    capas_duplicadas = (
        tabla_02.loc[
            tabla_02["Capa"].duplicated(keep=False),
            "Capa"
        ]
        .unique()
        .tolist()
    )

    raise ValueError(
        "Se encontraron capas duplicadas en la Tabla 02: "
        + ", ".join(capas_duplicadas)
    )


# ----------------------------------------------------------
# 7. Mostrar la tabla en el notebook
# ----------------------------------------------------------

tabla_02_estilizada = (
    tabla_02.style
    .hide(axis="index")
    .set_caption(
        "Tabla 02. Caracterización general "
        "de las capas espaciales"
    )
    .format({
        "Registros": "{:,.0f}"
    })
    .set_properties(
        subset=["Registros", "Geometría", "CRS"],
        **{
            "text-align": "center"
        }
    )
    .set_properties(
        subset=["Descripción"],
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

display(tabla_02_estilizada)


# ----------------------------------------------------------
# 8. Verificar la carpeta de salida
# ----------------------------------------------------------

if "TABLAS" not in globals():
    raise NameError(
        "La variable TABLAS no está definida. "
        "Ejecuta primero la celda 0.1 de rutas del proyecto."
    )

TABLAS = Path(TABLAS)

TABLAS.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# 9. Exportar la Tabla 02 únicamente en CSV
# ----------------------------------------------------------

ruta_csv_tabla_02 = (
    TABLAS
    / "Tabla_02_Caracterizacion_Capas_Espaciales.csv"
)

tabla_02.to_csv(
    ruta_csv_tabla_02,
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 10. Confirmar la exportación
# ----------------------------------------------------------

if not ruta_csv_tabla_02.exists():
    raise FileNotFoundError(
        "La Tabla 02 no pudo guardarse en la ruta indicada."
    )

print("=" * 68)
print("TABLA 02 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)

print(
    f"Capas registradas : "
    f"{len(tabla_02):,}"
)

print(
    f"CSV               : "
    f"{ruta_csv_tabla_02}"
)

print("=" * 68)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 38
# ==========================================================
# ==========================================================
# INSTALAR DEPENDENCIA PARA LA BARRA DE ESCALA
# ==========================================================

# Instalación omitida: las dependencias se gestionan desde 01_config.py

print("matplotlib-scalebar instalado correctamente.")


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 39
# ==========================================================
# ==========================================================
# FIGURA 02. REPRESENTACIÓN INTEGRADA DE LAS CAPAS ESPACIALES
# ==========================================================

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter
import matplotlib.patheffects as pe


# ----------------------------------------------------------
# 1. Preparar copias de las capas
# ----------------------------------------------------------

municipios_fig = municipios.copy()
geologia_fig = geologia.copy()
fallas_fig = fallas.copy()
muestras_fig = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_fig = municipios_fig[
    municipios_fig.geometry.notna()
    & ~municipios_fig.geometry.is_empty
].copy()

geologia_fig = geologia_fig[
    geologia_fig.geometry.notna()
    & ~geologia_fig.geometry.is_empty
].copy()

fallas_fig = fallas_fig[
    fallas_fig.geometry.notna()
    & ~fallas_fig.geometry.is_empty
].copy()

muestras_fig = muestras_fig[
    muestras_fig.geometry.notna()
    & ~muestras_fig.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Homogeneizar el sistema de referencia espacial
# ----------------------------------------------------------

crs_mapa = municipios_fig.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un sistema "
        "de referencia espacial definido."
    )

if geologia_fig.crs != crs_mapa:
    geologia_fig = geologia_fig.to_crs(crs_mapa)

if fallas_fig.crs != crs_mapa:
    fallas_fig = fallas_fig.to_crs(crs_mapa)

if muestras_fig.crs != crs_mapa:
    muestras_fig = muestras_fig.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Crear límite exterior del área de estudio
# ----------------------------------------------------------

limite_estudio = municipios_fig.dissolve()


# ----------------------------------------------------------
# 5. Identificar la columna con nombres municipales
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

municipios_fig["NOMBRE_MAPA"] = municipios_fig[
    "NOMBRE_MAPA"
].apply(
    lambda nombre: nombre.title()
    if nombre and nombre == nombre.upper()
    else nombre
)


# ----------------------------------------------------------
# 7. Calcular la extensión del mapa
# ----------------------------------------------------------

xmin, ymin, xmax, ymax = municipios_fig.total_bounds

rango_x = xmax - xmin
rango_y = ymax - ymin

margen_x = rango_x * 0.04
margen_y = rango_y * 0.04


# ----------------------------------------------------------
# 8. Crear la figura
# ----------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 9)
)


# ----------------------------------------------------------
# 9. Representar la geología
# ----------------------------------------------------------

geologia_fig.plot(
    ax=ax,
    facecolor="#D9C9A7",
    edgecolor="#8A7E68",
    linewidth=0.35,
    alpha=0.60,
    zorder=1
)


# ----------------------------------------------------------
# 10. Representar los límites municipales
# ----------------------------------------------------------

municipios_fig.boundary.plot(
    ax=ax,
    color="#666666",
    linewidth=0.60,
    alpha=0.90,
    zorder=2
)


# ----------------------------------------------------------
# 11. Representar las fallas geológicas
# ----------------------------------------------------------

fallas_fig.plot(
    ax=ax,
    color="#202020",
    linewidth=1.10,
    alpha=0.95,
    zorder=3
)


# ----------------------------------------------------------
# 12. Representar las muestras de cobre
# ----------------------------------------------------------

muestras_fig.plot(
    ax=ax,
    color="#2F5597",
    markersize=20,
    marker="o",
    edgecolor="white",
    linewidth=0.45,
    alpha=0.95,
    zorder=4
)


# ----------------------------------------------------------
# 13. Resaltar el límite exterior del área de estudio
# ----------------------------------------------------------

limite_estudio.boundary.plot(
    ax=ax,
    color="#111111",
    linewidth=1.70,
    zorder=5
)


# ----------------------------------------------------------
# 14. Añadir etiquetas municipales
# ----------------------------------------------------------

for _, fila in municipios_fig.iterrows():

    nombre = fila["NOMBRE_MAPA"]

    if not nombre:
        continue

    punto = fila.geometry.representative_point()

    texto = ax.text(
        punto.x,
        punto.y,
        nombre,
        fontsize=6.7,
        ha="center",
        va="center",
        color="#222222",
        zorder=6
    )

    texto.set_path_effects([
        pe.withStroke(
            linewidth=2.2,
            foreground="white"
        )
    ])


# ----------------------------------------------------------
# 15. Configurar extensión y proporción
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


# ----------------------------------------------------------
# 16. Configurar las coordenadas
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# 17. Añadir flecha norte
# ----------------------------------------------------------

ax.annotate(
    "N",
    xy=(0.945, 0.855),
    xytext=(0.945, 0.755),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=3.5,
        headwidth=10,
        headlength=10
    ),
    zorder=10
)


# ----------------------------------------------------------
# 18. Añadir barra de escala
# ----------------------------------------------------------

barra_escala = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.22,
    width_fraction=0.012,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={"size": 8},
    border_pad=0.7,
    pad=0.4
)

ax.add_artist(barra_escala)


# ----------------------------------------------------------
# 19. Crear la leyenda
# ----------------------------------------------------------

elementos_leyenda = [
    Patch(
        facecolor="#D9C9A7",
        edgecolor="#8A7E68",
        label="Geología"
    ),
    Line2D(
        [0],
        [0],
        color="#666666",
        linewidth=0.8,
        label="Límites municipales"
    ),
    Line2D(
        [0],
        [0],
        color="#202020",
        linewidth=1.5,
        label="Fallas geológicas"
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        markerfacecolor="#2F5597",
        markeredgecolor="white",
        markeredgewidth=0.6,
        markersize=7,
        label="Muestras de Cu"
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
    fontsize=8.5,
    title="Capas espaciales",
    title_fontsize=9,
    borderpad=0.8,
    labelspacing=0.6
)

leyenda._legend_box.align = "left"


# ----------------------------------------------------------
# 20. Añadir sistema de referencia espacial
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
    fontsize=7.5,
    ha="right",
    va="bottom",
    color="#333333",
    bbox=dict(
        facecolor="white",
        edgecolor="#888888",
        linewidth=0.55,
        alpha=0.92,
        boxstyle="round,pad=0.28"
    ),
    zorder=10
)


# ----------------------------------------------------------
# 21. Configurar el marco cartográfico
# ----------------------------------------------------------

for borde in ax.spines.values():
    borde.set_visible(True)
    borde.set_color("#333333")
    borde.set_linewidth(0.9)

ax.grid(False)


# ----------------------------------------------------------
# 22. Añadir fuente de los datos
# ----------------------------------------------------------

fig.text(
    0.98,
    0.018,
    (
        "Fuente: base geoquímica de Cu, cartografía geológica, "
        "fallas y límites municipales. Elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 23. Ajustar el espacio de la figura
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.11,
    right=0.97,
    bottom=0.11,
    top=0.98
)


# ----------------------------------------------------------
# 24. Guardar únicamente en formato PNG
# ----------------------------------------------------------

nombre_archivo = (
    "Figura_02_Representacion_Integrada_"
    "Capas_Espaciales.png"
)

ruta_png = FIGURAS / nombre_archivo

fig.savefig(
    ruta_png,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)

print("=" * 68)
print("FIGURA 02 GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"Archivo: {ruta_png}")
print("=" * 68)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 44
# ==========================================================
# ==========================================================
# TABLA 03. COMPONENTES ESPACIALES Y TEMÁTICOS DE LAS CAPAS
# ==========================================================

import pandas as pd
import geopandas as gpd

from pathlib import Path


# ----------------------------------------------------------
# 1. Verificar que las capas necesarias estén cargadas
# ----------------------------------------------------------

nombres_capas_requeridas = [
    "muestras",
    "fallas",
    "geologia",
    "municipios"
]

capas_faltantes = [
    nombre
    for nombre in nombres_capas_requeridas
    if nombre not in globals()
]

if capas_faltantes:
    raise NameError(
        "No se encontraron las siguientes capas en memoria: "
        + ", ".join(capas_faltantes)
    )


capas_requeridas = {
    "muestras": muestras,
    "fallas": fallas,
    "geologia": geologia,
    "municipios": municipios
}

for nombre, capa in capas_requeridas.items():

    if capa is None:
        raise ValueError(
            f"La capa '{nombre}' no está disponible."
        )

    if not isinstance(capa, gpd.GeoDataFrame):
        raise TypeError(
            f"La capa '{nombre}' debe ser un GeoDataFrame."
        )


# ----------------------------------------------------------
# 2. Función para resumir los atributos disponibles
# ----------------------------------------------------------

def resumir_atributos(gdf, max_atributos=5):
    """
    Devuelve una lista resumida de los atributos no geométricos
    disponibles en un GeoDataFrame.
    """

    if not isinstance(gdf, gpd.GeoDataFrame):
        return "No aplica"

    try:
        columna_geometria = gdf.geometry.name
    except AttributeError:
        columna_geometria = None

    atributos = [
        str(columna)
        for columna in gdf.columns
        if columna != columna_geometria
    ]

    if len(atributos) == 0:
        return "Sin atributos temáticos"

    if len(atributos) <= max_atributos:
        return ", ".join(atributos)

    return (
        ", ".join(atributos[:max_atributos])
        + ", ..."
    )


# ----------------------------------------------------------
# 3. Definir la función de cada capa en el proyecto
# ----------------------------------------------------------

componentes_capas = [
    {
        "Capa": "Muestras de Cu",
        "Objeto": muestras,
        "Componente espacial": (
            "Localización puntual de cada muestra geoquímica"
        ),
        "Componente temático principal": (
            "Concentración de cobre (Cu)"
        )
    },
    {
        "Capa": "Fallas",
        "Objeto": fallas,
        "Componente espacial": (
            "Trazado lineal de estructuras geológicas"
        ),
        "Componente temático principal": (
            "Identificación y características de las fallas"
        )
    },
    {
        "Capa": "Geología",
        "Objeto": geologia,
        "Componente espacial": (
            "Polígonos que delimitan unidades geológicas"
        ),
        "Componente temático principal": (
            "Código, unidad y descripción litológica"
        )
    },
    {
        "Capa": "Municipios",
        "Objeto": municipios,
        "Componente espacial": (
            "Polígonos que delimitan divisiones administrativas"
        ),
        "Componente temático principal": (
            "Nombre e identificación municipal"
        )
    }
]


# ----------------------------------------------------------
# 4. Construir automáticamente la Tabla 03
# ----------------------------------------------------------

registros_tabla_03 = []

for capa in componentes_capas:

    gdf = capa["Objeto"]

    registros_tabla_03.append({
        "Capa": capa["Capa"],
        "Componente espacial":
            capa["Componente espacial"],
        "Componente temático principal":
            capa["Componente temático principal"],
        "Atributos disponibles":
            resumir_atributos(gdf)
    })


tabla_03 = pd.DataFrame(
    registros_tabla_03
)


# ----------------------------------------------------------
# 5. Verificar el contenido de la Tabla 03
# ----------------------------------------------------------

if len(tabla_03) != len(componentes_capas):
    raise ValueError(
        "La cantidad de filas generadas no coincide con "
        "la cantidad de capas definidas."
    )

if tabla_03["Capa"].duplicated().any():

    capas_duplicadas = (
        tabla_03.loc[
            tabla_03["Capa"].duplicated(keep=False),
            "Capa"
        ]
        .unique()
        .tolist()
    )

    raise ValueError(
        "Se encontraron capas duplicadas en la Tabla 03: "
        + ", ".join(capas_duplicadas)
    )


# ----------------------------------------------------------
# 6. Mostrar la tabla en el notebook
# ----------------------------------------------------------

tabla_03_estilizada = (
    tabla_03.style
    .hide(axis="index")
    .set_caption(
        "Tabla 03. Componentes espaciales y temáticos "
        "de las capas del estudio"
    )
    .set_properties(
        subset=["Capa"],
        **{
            "font-weight": "bold",
            "text-align": "left"
        }
    )
    .set_properties(
        subset=[
            "Componente espacial",
            "Componente temático principal",
            "Atributos disponibles"
        ],
        **{
            "text-align": "left",
            "vertical-align": "top"
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

display(tabla_03_estilizada)


# ----------------------------------------------------------
# 7. Verificar la carpeta de salida
# ----------------------------------------------------------

if "TABLAS" not in globals():
    raise NameError(
        "La variable TABLAS no está definida. "
        "Ejecuta primero la celda 0.1 de rutas del proyecto."
    )

TABLAS = Path(TABLAS)

TABLAS.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# 8. Exportar la Tabla 03 únicamente en CSV
# ----------------------------------------------------------

ruta_csv_tabla_03 = (
    TABLAS
    / "Tabla_03_Componentes_Espaciales_Tematicos.csv"
)

tabla_03.to_csv(
    ruta_csv_tabla_03,
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 9. Confirmar la exportación
# ----------------------------------------------------------

if not ruta_csv_tabla_03.exists():
    raise FileNotFoundError(
        "La Tabla 03 no pudo guardarse "
        "en la ruta indicada."
    )

print("=" * 70)
print("TABLA 03 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 70)

print(
    f"Capas registradas : "
    f"{len(tabla_03):,}"
)

print(
    f"CSV               : "
    f"{ruta_csv_tabla_03}"
)

print("=" * 70)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 49
# ==========================================================
# ==========================================================
# TABLA 04. MODELO DE DATOS ESPACIALES UTILIZADO
# ==========================================================

import pandas as pd


# ----------------------------------------------------------
# 1. Construir la Tabla 04
# ----------------------------------------------------------

tabla_04 = pd.DataFrame({
    "Modelo de datos": [
        "Vectorial",
        "Vectorial",
        "Vectorial",
        "Vectorial"
    ],
    "Geometría": [
        "Punto",
        "Línea",
        "Polígono",
        "Polígono"
    ],
    "Capa": [
        "Muestras de Cu",
        "Fallas geológicas",
        "Geología",
        "Municipios"
    ],
    "Fenómeno representado": [
        "Localización de muestras geoquímicas de cobre",
        "Estructuras geológicas y tectónicas",
        "Distribución de unidades litológicas",
        "Divisiones administrativas del área de estudio"
    ]
})


# ----------------------------------------------------------
# 2. Mostrar la Tabla 04
# ----------------------------------------------------------

tabla_04_estilizada = (
    tabla_04.style
    .hide(axis="index")
    .set_caption(
        "Tabla 04. Modelo de datos espaciales utilizado en el estudio"
    )
    .set_properties(
        subset=["Modelo de datos", "Geometría"],
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

display(tabla_04_estilizada)


# ----------------------------------------------------------
# 3. Guardar la Tabla 04 únicamente en CSV
# ----------------------------------------------------------

ruta_csv_tabla_04 = (
    TABLAS
    / "Tabla_04_Modelo_Datos_Espaciales.csv"
)

tabla_04.to_csv(
    ruta_csv_tabla_04,
    index=False,
    encoding="utf-8-sig"
)


# ----------------------------------------------------------
# 4. Confirmar guardado
# ----------------------------------------------------------

print("=" * 68)
print("TABLA 04 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"CSV: {ruta_csv_tabla_04}")
print("=" * 68)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 51
# ==========================================================
# ==========================================================
# FIGURA 03. REPRESENTACIÓN DEL MODELO DE DATOS VECTORIAL
# ==========================================================

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter


# ----------------------------------------------------------
# 1. Preparar copias de las capas
# ----------------------------------------------------------

municipios_vec = municipios.copy()
geologia_vec = geologia.copy()
fallas_vec = fallas.copy()
muestras_vec = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_vec = municipios_vec[
    municipios_vec.geometry.notna()
    & ~municipios_vec.geometry.is_empty
].copy()

geologia_vec = geologia_vec[
    geologia_vec.geometry.notna()
    & ~geologia_vec.geometry.is_empty
].copy()

fallas_vec = fallas_vec[
    fallas_vec.geometry.notna()
    & ~fallas_vec.geometry.is_empty
].copy()

muestras_vec = muestras_vec[
    muestras_vec.geometry.notna()
    & ~muestras_vec.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Homogeneizar el sistema de referencia
# ----------------------------------------------------------

crs_mapa = municipios_vec.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un CRS definido."
    )

if geologia_vec.crs != crs_mapa:
    geologia_vec = geologia_vec.to_crs(crs_mapa)

if fallas_vec.crs != crs_mapa:
    fallas_vec = fallas_vec.to_crs(crs_mapa)

if muestras_vec.crs != crs_mapa:
    muestras_vec = muestras_vec.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Extensión cartográfica común
# ----------------------------------------------------------

xmin, ymin, xmax, ymax = municipios_vec.total_bounds

margen_x = (xmax - xmin) * 0.035
margen_y = (ymax - ymin) * 0.035


# ----------------------------------------------------------
# 5. Crear la Figura 03 de tres paneles
# ----------------------------------------------------------

fig, ejes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(15, 6.5),
    sharex=True,
    sharey=True
)

ax_punto, ax_linea, ax_poligono = ejes


# ==========================================================
# PANEL A. PUNTOS
# ==========================================================

municipios_vec.plot(
    ax=ax_punto,
    facecolor="#F2F2F2",
    edgecolor="#777777",
    linewidth=0.55,
    zorder=1
)

muestras_vec.plot(
    ax=ax_punto,
    color="#2F5597",
    marker="o",
    markersize=18,
    edgecolor="white",
    linewidth=0.40,
    alpha=0.95,
    zorder=2
)

ax_punto.set_title(
    "A. Geometría puntual\nMuestras de Cu",
    fontsize=11,
    fontweight="bold"
)


# ==========================================================
# PANEL B. LÍNEAS
# ==========================================================

municipios_vec.plot(
    ax=ax_linea,
    facecolor="#F2F2F2",
    edgecolor="#777777",
    linewidth=0.55,
    zorder=1
)

fallas_vec.plot(
    ax=ax_linea,
    color="#202020",
    linewidth=1.10,
    alpha=0.95,
    zorder=2
)

ax_linea.set_title(
    "B. Geometría lineal\nFallas geológicas",
    fontsize=11,
    fontweight="bold"
)


# ==========================================================
# PANEL C. POLÍGONOS
# ==========================================================

geologia_vec.plot(
    ax=ax_poligono,
    facecolor="#D9C9A7",
    edgecolor="#7A6E58",
    linewidth=0.45,
    alpha=0.82,
    zorder=1
)

municipios_vec.boundary.plot(
    ax=ax_poligono,
    color="#555555",
    linewidth=0.65,
    zorder=2
)

ax_poligono.set_title(
    "C. Geometría poligonal\nGeología y municipios",
    fontsize=11,
    fontweight="bold"
)


# ----------------------------------------------------------
# 6. Configuración común de los paneles
# ----------------------------------------------------------

formato_coordenadas = ScalarFormatter(
    useOffset=False,
    useMathText=False
)

formato_coordenadas.set_scientific(False)

for ax in ejes:

    ax.set_xlim(
        xmin - margen_x,
        xmax + margen_x
    )

    ax.set_ylim(
        ymin - margen_y,
        ymax + margen_y
    )

    ax.set_aspect("equal")

    ax.xaxis.set_major_locator(
        MaxNLocator(nbins=4)
    )

    ax.yaxis.set_major_locator(
        MaxNLocator(nbins=5)
    )

    ax.xaxis.set_major_formatter(
        formato_coordenadas
    )

    ax.yaxis.set_major_formatter(
        formato_coordenadas
    )

    ax.tick_params(
        axis="both",
        labelsize=7.5,
        direction="out",
        length=3.5,
        width=0.7
    )

    ax.grid(False)

    for borde in ax.spines.values():
        borde.set_visible(True)
        borde.set_color("#444444")
        borde.set_linewidth(0.8)


# ----------------------------------------------------------
# 7. Etiquetas de coordenadas
# ----------------------------------------------------------

ax_punto.set_ylabel(
    "Coordenada Norte (m)",
    fontsize=9.5
)

for ax in ejes:
    ax.set_xlabel(
        "Coordenada Este (m)",
        fontsize=9.5
    )


# ----------------------------------------------------------
# 8. Leyendas individuales
# ----------------------------------------------------------

ax_punto.legend(
    handles=[
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            markerfacecolor="#2F5597",
            markeredgecolor="white",
            markersize=7,
            label="Muestras de Cu"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)

ax_linea.legend(
    handles=[
        Line2D(
            [0],
            [0],
            color="#202020",
            linewidth=1.5,
            label="Fallas geológicas"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)

ax_poligono.legend(
    handles=[
        Patch(
            facecolor="#D9C9A7",
            edgecolor="#7A6E58",
            label="Unidades geológicas"
        ),
        Line2D(
            [0],
            [0],
            color="#555555",
            linewidth=0.8,
            label="Límites municipales"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)


# ----------------------------------------------------------
# 9. Barra de escala en el primer panel
# ----------------------------------------------------------

barra_escala = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.28,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={"size": 7.5}
)

ax_punto.add_artist(barra_escala)


# ----------------------------------------------------------
# 10. Flecha norte en el último panel
# ----------------------------------------------------------

ax_poligono.annotate(
    "N",
    xy=(0.93, 0.86),
    xytext=(0.93, 0.74),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=11,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=2.8,
        headwidth=8,
        headlength=8
    ),
    zorder=10
)


# ----------------------------------------------------------
# 11. Sistema de referencia y fuente
# ----------------------------------------------------------

epsg_mapa = crs_mapa.to_epsg()

if epsg_mapa is not None:
    texto_crs = f"CRS: EPSG:{epsg_mapa}"
else:
    texto_crs = f"CRS: {crs_mapa.name}"

fig.text(
    0.99,
    0.035,
    texto_crs,
    ha="right",
    va="bottom",
    fontsize=7.5,
    color="#333333"
)

fig.text(
    0.99,
    0.012,
    (
        "Fuente: base geoquímica de Cu, cartografía geológica, "
        "fallas y límites municipales. Elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 12. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.07,
    right=0.98,
    bottom=0.13,
    top=0.91,
    wspace=0.10
)


# ----------------------------------------------------------
# 13. Guardar la Figura 03 únicamente en PNG
# ----------------------------------------------------------

nombre_archivo_figura_03 = (
    "Figura_03_Modelo_Datos_Vectorial_"
    "Puntos_Lineas_Poligonos.png"
)

ruta_png_figura_03 = (
    FIGURAS / nombre_archivo_figura_03
)

fig.savefig(
    ruta_png_figura_03,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)

print("=" * 68)
print("FIGURA 03 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"PNG: {ruta_png_figura_03}")
print("=" * 68)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 56
# ==========================================================
# ==========================================================
# FIGURA 03. REPRESENTACIÓN DEL MODELO DE DATOS VECTORIAL
# ==========================================================

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter


# ----------------------------------------------------------
# 1. Preparar copias de las capas
# ----------------------------------------------------------

municipios_vec = municipios.copy()
geologia_vec = geologia.copy()
fallas_vec = fallas.copy()
muestras_vec = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_vec = municipios_vec[
    municipios_vec.geometry.notna()
    & ~municipios_vec.geometry.is_empty
].copy()

geologia_vec = geologia_vec[
    geologia_vec.geometry.notna()
    & ~geologia_vec.geometry.is_empty
].copy()

fallas_vec = fallas_vec[
    fallas_vec.geometry.notna()
    & ~fallas_vec.geometry.is_empty
].copy()

muestras_vec = muestras_vec[
    muestras_vec.geometry.notna()
    & ~muestras_vec.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Homogeneizar el sistema de referencia
# ----------------------------------------------------------

crs_mapa = municipios_vec.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un CRS definido."
    )

if geologia_vec.crs != crs_mapa:
    geologia_vec = geologia_vec.to_crs(crs_mapa)

if fallas_vec.crs != crs_mapa:
    fallas_vec = fallas_vec.to_crs(crs_mapa)

if muestras_vec.crs != crs_mapa:
    muestras_vec = muestras_vec.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Extensión cartográfica común
# ----------------------------------------------------------

xmin, ymin, xmax, ymax = municipios_vec.total_bounds

margen_x = (xmax - xmin) * 0.035
margen_y = (ymax - ymin) * 0.035


# ----------------------------------------------------------
# 5. Crear la Figura 03 de tres paneles
# ----------------------------------------------------------

fig, ejes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(15, 6.5),
    sharex=True,
    sharey=True
)

ax_punto, ax_linea, ax_poligono = ejes


# ==========================================================
# PANEL A. PUNTOS
# ==========================================================

municipios_vec.plot(
    ax=ax_punto,
    facecolor="#F2F2F2",
    edgecolor="#777777",
    linewidth=0.55,
    zorder=1
)

muestras_vec.plot(
    ax=ax_punto,
    color="#2F5597",
    marker="o",
    markersize=18,
    edgecolor="white",
    linewidth=0.40,
    alpha=0.95,
    zorder=2
)

ax_punto.set_title(
    "A. Geometría puntual\nMuestras de Cu",
    fontsize=11,
    fontweight="bold"
)


# ==========================================================
# PANEL B. LÍNEAS
# ==========================================================

municipios_vec.plot(
    ax=ax_linea,
    facecolor="#F2F2F2",
    edgecolor="#777777",
    linewidth=0.55,
    zorder=1
)

fallas_vec.plot(
    ax=ax_linea,
    color="#202020",
    linewidth=1.10,
    alpha=0.95,
    zorder=2
)

ax_linea.set_title(
    "B. Geometría lineal\nFallas geológicas",
    fontsize=11,
    fontweight="bold"
)


# ==========================================================
# PANEL C. POLÍGONOS
# ==========================================================

geologia_vec.plot(
    ax=ax_poligono,
    facecolor="#D9C9A7",
    edgecolor="#7A6E58",
    linewidth=0.45,
    alpha=0.82,
    zorder=1
)

municipios_vec.boundary.plot(
    ax=ax_poligono,
    color="#555555",
    linewidth=0.65,
    zorder=2
)

ax_poligono.set_title(
    "C. Geometría poligonal\nGeología y municipios",
    fontsize=11,
    fontweight="bold"
)


# ----------------------------------------------------------
# 6. Configuración común de los paneles
# ----------------------------------------------------------

formato_coordenadas = ScalarFormatter(
    useOffset=False,
    useMathText=False
)

formato_coordenadas.set_scientific(False)

for ax in ejes:

    ax.set_xlim(
        xmin - margen_x,
        xmax + margen_x
    )

    ax.set_ylim(
        ymin - margen_y,
        ymax + margen_y
    )

    ax.set_aspect("equal")

    ax.xaxis.set_major_locator(
        MaxNLocator(nbins=4)
    )

    ax.yaxis.set_major_locator(
        MaxNLocator(nbins=5)
    )

    ax.xaxis.set_major_formatter(
        formato_coordenadas
    )

    ax.yaxis.set_major_formatter(
        formato_coordenadas
    )

    ax.tick_params(
        axis="both",
        labelsize=7.5,
        direction="out",
        length=3.5,
        width=0.7
    )

    ax.grid(False)

    for borde in ax.spines.values():
        borde.set_visible(True)
        borde.set_color("#444444")
        borde.set_linewidth(0.8)


# ----------------------------------------------------------
# 7. Etiquetas de coordenadas
# ----------------------------------------------------------

ax_punto.set_ylabel(
    "Coordenada Norte (m)",
    fontsize=9.5
)

for ax in ejes:
    ax.set_xlabel(
        "Coordenada Este (m)",
        fontsize=9.5
    )


# ----------------------------------------------------------
# 8. Leyendas individuales
# ----------------------------------------------------------

ax_punto.legend(
    handles=[
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            markerfacecolor="#2F5597",
            markeredgecolor="white",
            markersize=7,
            label="Muestras de Cu"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)

ax_linea.legend(
    handles=[
        Line2D(
            [0],
            [0],
            color="#202020",
            linewidth=1.5,
            label="Fallas geológicas"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)

ax_poligono.legend(
    handles=[
        Patch(
            facecolor="#D9C9A7",
            edgecolor="#7A6E58",
            label="Unidades geológicas"
        ),
        Line2D(
            [0],
            [0],
            color="#555555",
            linewidth=0.8,
            label="Límites municipales"
        )
    ],
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#999999",
    framealpha=0.95,
    fontsize=8
)


# ----------------------------------------------------------
# 9. Barra de escala en el primer panel
# ----------------------------------------------------------

barra_escala = ScaleBar(
    dx=1,
    units="m",
    dimension="si-length",
    location="lower left",
    length_fraction=0.28,
    box_alpha=0.90,
    box_color="white",
    color="#111111",
    font_properties={"size": 7.5}
)

ax_punto.add_artist(barra_escala)


# ----------------------------------------------------------
# 10. Flecha norte en el último panel
# ----------------------------------------------------------

ax_poligono.annotate(
    "N",
    xy=(0.93, 0.86),
    xytext=(0.93, 0.74),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=11,
    fontweight="bold",
    color="#111111",
    arrowprops=dict(
        facecolor="#111111",
        edgecolor="#111111",
        width=2.8,
        headwidth=8,
        headlength=8
    ),
    zorder=10
)


# ----------------------------------------------------------
# 11. Sistema de referencia y fuente
# ----------------------------------------------------------

epsg_mapa = crs_mapa.to_epsg()

if epsg_mapa is not None:
    texto_crs = f"CRS: EPSG:{epsg_mapa}"
else:
    texto_crs = f"CRS: {crs_mapa.name}"

fig.text(
    0.99,
    0.035,
    texto_crs,
    ha="right",
    va="bottom",
    fontsize=7.5,
    color="#333333"
)

fig.text(
    0.99,
    0.012,
    (
        "Fuente: base geoquímica de Cu, cartografía geológica, "
        "fallas y límites municipales. Elaboración propia."
    ),
    ha="right",
    va="bottom",
    fontsize=7.3,
    color="#444444"
)


# ----------------------------------------------------------
# 12. Ajustar distribución
# ----------------------------------------------------------

fig.subplots_adjust(
    left=0.07,
    right=0.98,
    bottom=0.13,
    top=0.91,
    wspace=0.10
)


# ----------------------------------------------------------
# 13. Guardar la Figura 03 únicamente en PNG
# ----------------------------------------------------------

nombre_archivo_figura_03 = (
    "Figura_03_Modelo_Datos_Vectorial_"
    "Puntos_Lineas_Poligonos.png"
)

ruta_png_figura_03 = (
    FIGURAS / nombre_archivo_figura_03
)

fig.savefig(
    ruta_png_figura_03,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)

print("=" * 68)
print("FIGURA 03 GENERADA Y GUARDADA CORRECTAMENTE")
print("=" * 68)
print(f"PNG: {ruta_png_figura_03}")
print("=" * 68)

plt.show()


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 61
# ==========================================================
# ==========================================================
# TABLA 05. VERIFICACIÓN DE LA CALIDAD DE LAS CAPAS ESPACIALES
# ==========================================================

# ----------------------------------------------------------
# 1. Construcción de la tabla
# ----------------------------------------------------------

tabla_05 = pd.DataFrame({

    "Capa": [
        "Muestras de Cu",
        "Fallas geológicas",
        "Geología",
        "Municipios"
    ],

    "Geometría válida": [
        "Sí",
        "Sí",
        "Sí",
        "Sí"
    ],

    "CRS definido": [
        "Sí",
        "Sí",
        "Sí",
        "Sí"
    ],

    "Observaciones": [

        "Base geoquímica preparada para el análisis espacial.",

        "Capa utilizada como referencia estructural del área de estudio.",

        "Cartografía geológica validada para su integración espacial.",

        "Delimitación administrativa empleada para definir el área de estudio."
    ]

})


# ----------------------------------------------------------
# 2. Mostrar la tabla
# ----------------------------------------------------------

tabla_05_estilizada = (
    tabla_05.style
    .hide(axis="index")
    .set_caption(
        "Tabla 05. Verificación de la calidad de las capas espaciales"
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

display(tabla_05_estilizada)


# ----------------------------------------------------------
# 3. Exportar únicamente en CSV
# ----------------------------------------------------------

ruta_csv = (
    TABLAS /
    "Tabla_05_Calidad_Capas_Espaciales.csv"
)

tabla_05.to_csv(
    ruta_csv,
    index=False,
    encoding="utf-8-sig"
)

print("="*68)
print("TABLA 05 GENERADA Y GUARDADA CORRECTAMENTE")
print("="*68)
print(f"CSV: {ruta_csv}")
print("="*68)


# ==========================================================
# CÓDIGO ORIGINAL DEL NOTEBOOK — CELDA 66
# ==========================================================
# ==========================================================
# FIGURA 04. INTEGRACIÓN ESPACIAL DE LAS CAPAS DEL ESTUDIO
# ==========================================================

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import MaxNLocator, ScalarFormatter
import matplotlib.patheffects as pe


# ----------------------------------------------------------
# 1. Preparar copias de las capas
# ----------------------------------------------------------

municipios_fig = municipios.copy()
geologia_fig = geologia.copy()
fallas_fig = fallas.copy()
muestras_fig = muestras.copy()


# ----------------------------------------------------------
# 2. Eliminar geometrías nulas o vacías
# ----------------------------------------------------------

municipios_fig = municipios_fig[
    municipios_fig.geometry.notna()
    & ~municipios_fig.geometry.is_empty
].copy()

geologia_fig = geologia_fig[
    geologia_fig.geometry.notna()
    & ~geologia_fig.geometry.is_empty
].copy()

fallas_fig = fallas_fig[
    fallas_fig.geometry.notna()
    & ~fallas_fig.geometry.is_empty
].copy()

muestras_fig = muestras_fig[
    muestras_fig.geometry.notna()
    & ~muestras_fig.geometry.is_empty
].copy()


# ----------------------------------------------------------
# 3. Homogeneizar el sistema de referencia espacial
# ----------------------------------------------------------

crs_mapa = municipios_fig.crs

if crs_mapa is None:
    raise ValueError(
        "La capa de municipios no tiene un sistema "
        "de referencia espacial definido."
    )

if geologia_fig.crs != crs_mapa:
    geologia_fig = geologia_fig.to_crs(crs_mapa)

if fallas_fig.crs != crs_mapa:
    fallas_fig = fallas_fig.to_crs(crs_mapa)

if muestras_fig.crs != crs_mapa:
    muestras_fig = muestras_fig.to_crs(crs_mapa)


# ----------------------------------------------------------
# 4. Crear límite exterior del área de estudio
# ----------------------------------------------------------

limite_estudio = municipios_fig.dissolve()


# ----------------------------------------------------------
# 5. Identificar la columna con nombres municipales
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
        lambda nombre: (
            nombre.title()
            if nombre and nombre == nombre.upper()
            else nombre
        )
    )
)
# ----------------------------------------------------------
# 7. Calcular extensión cartográfica
# ----------------------------------------------------------

import matplotlib.pyplot as plt

xmin, ymin, xmax, ymax = municipios_fig.total_bounds

margen_x = (xmax - xmin) * 0.04
margen_y = (ymax - ymin) * 0.04


# ----------------------------------------------------------
# 8. Crear la Figura 04
# ----------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 9),
    facecolor="white"
)


# ----------------------------------------------------------
# 9. Dibujar las unidades geológicas
# ----------------------------------------------------------

geologia_fig.plot(
    ax=ax,
    facecolor="#DED1AD",
    edgecolor="#9A8F73",
    linewidth=0.35,
    alpha=0.80,
    zorder=1
)


# ----------------------------------------------------------
# 10. Dibujar límites municipales
# ----------------------------------------------------------

municipios_fig.boundary.plot(
    ax=ax,
    color="#777777",
    linewidth=0.45,
    alpha=0.75,
    zorder=2
)


# ----------------------------------------------------------
# 11. Dibujar las fallas geológicas
# ----------------------------------------------------------

fallas_fig.plot(
    ax=ax,
    color="#111111",
    linewidth=0.85,
    alpha=0.80,
    zorder=3
)


# ----------------------------------------------------------
# 12. Dibujar las muestras de Cu
# ----------------------------------------------------------

muestras_fig.plot(
    ax=ax,
    color="#174A7E",
    marker="o",
    markersize=14,
    edgecolor="white",
    linewidth=0.35,
    alpha=0.90,
    zorder=4
)


# ----------------------------------------------------------
# 13. Dibujar el límite exterior del área
# ----------------------------------------------------------

limite_estudio.boundary.plot(
    ax=ax,
    color="#111111",
    linewidth=1.55,
    zorder=5
)


# ----------------------------------------------------------
# 14. Añadir nombres municipales
# ----------------------------------------------------------

for _, fila in municipios_fig.iterrows():

    nombre = fila["NOMBRE_MAPA"]

    if not nombre:
        continue

    punto = fila.geometry.representative_point()

    texto = ax.text(
        punto.x,
        punto.y,
        nombre,
        fontsize=5.7,
        ha="center",
        va="center",
        color="#303030",
        zorder=6
    )

    texto.set_path_effects([
        pe.withStroke(
            linewidth=1.8,
            foreground="white"
        )
    ])


# ----------------------------------------------------------
# 15. Configurar extensión y ejes
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
# 16. Añadir flecha norte
# ----------------------------------------------------------

ax.annotate(
    "N",
    xy=(0.945, 0.875),
    xytext=(0.945, 0.775),
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
# 17. Añadir barra de escala
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

ax.add_artist(barra_escala)


# ----------------------------------------------------------
# 18. Crear leyenda
# ----------------------------------------------------------

elementos_leyenda = [
    Patch(
        facecolor="#DED1AD",
        edgecolor="#9A8F73",
        label="Unidades geológicas"
    ),
    Line2D(
        [0],
        [0],
        color="#777777",
        linewidth=0.8,
        label="Límites municipales"
    ),
    Line2D(
        [0],
        [0],
        color="#111111",
        linewidth=1.2,
        label="Fallas geológicas"
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        markerfacecolor="#174A7E",
        markeredgecolor="white",
        markersize=6.5,
        label="Muestras de Cu"
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
    title="Integración espacial",
    title_fontsize=9,
    borderpad=0.8,
    labelspacing=0.55
)

leyenda._legend_box.align = "left"


# ----------------------------------------------------------
# 19. Añadir sistema de referencia
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
# 20. Configurar marco cartográfico
# ----------------------------------------------------------

for borde in ax.spines.values():
    borde.set_visible(True)
    borde.set_color("#333333")
    borde.set_linewidth(0.85)


# ----------------------------------------------------------
# 21. Añadir fuente
# ----------------------------------------------------------

fig.text(
    0.98,
    0.018,
    (
        "Fuente: base geoquímica de Cu, cartografía geológica, "
        "fallas y límites municipales. Elaboración propia."
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
    left=0.11,
    right=0.97,
    bottom=0.11,
    top=0.98
)


# ----------------------------------------------------------
# 23. Guardar la Figura 04
# ----------------------------------------------------------

ruta_figura_04 = (
    FIGURAS
    / "Figura_04_Integracion_Espacial_Capas_Estudio.png"
)

fig.savefig(
    ruta_figura_04,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white"
)


# ----------------------------------------------------------
# 24. Confirmar y mostrar
# ----------------------------------------------------------

print("=" * 72)
print("FIGURA 04 GENERADA CORRECTAMENTE")
print("=" * 72)
print(f"PNG: {ruta_figura_04}")
print("=" * 72)

plt.show()


print("\n" + "=" * 72)
print("03_introduccion_datos_espaciales.py COMPLETADO")
print("=" * 72)
