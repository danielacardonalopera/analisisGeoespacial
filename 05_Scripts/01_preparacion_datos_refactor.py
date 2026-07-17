"""
01_preparacion_datos.py

Carga, validación, limpieza y delimitación espacial de las muestras.
"""

from __future__ import annotations

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, ScalarFormatter
from matplotlib_scalebar.scalebar import ScaleBar

from config import (
    CRS_PROYECTO,
    ESTUDIO,
    FIGURAS,
    PROCESADOS,
    TABLAS,
)
from utils import verificar_archivos_entrada

RUTA_MUESTRAS = PROCESADOS / "Muestras_Cu.gpkg"
RUTA_GEOLOGIA = PROCESADOS / "Geologia_Suroeste.gpkg"
RUTA_FALLAS = PROCESADOS / "Fallas_Suroeste.gpkg"
RUTA_MUNICIPIOS = PROCESADOS / "Municipios_Suroeste.gpkg"

RUTA_MUESTRAS_ESTUDIO = ESTUDIO / "Muestras_Cu_Area_Estudio.gpkg"
RUTA_MUESTRAS_FUERA = ESTUDIO / "Muestras_Cu_Fuera_Area.gpkg"
RUTA_FIGURA_01 = FIGURAS / "Figura_01_Delimitacion_Espacial_Area_Analisis.png"
RUTA_TABLA_01 = TABLAS / "Tabla_01_Seleccion_Muestras_Area_Analisis.csv"

# ==========================================================
# 2. FUNCIONES DE APOYO

# ==========================================================

def verificar_archivos_entrada() -> None:
    """Comprueba que existan las cuatro capas requeridas."""
    rutas = {
        "muestras": RUTA_MUESTRAS,
        "geología": RUTA_GEOLOGIA,
        "fallas": RUTA_FALLAS,
        "municipios": RUTA_MUNICIPIOS,
    }

    faltantes = [
        f"{nombre}: {ruta}"
        for nombre, ruta in rutas.items()
        if not ruta.exists()
    ]

    if faltantes:
        detalle = "\n".join(faltantes)
        raise FileNotFoundError(
            "No se encontraron los siguientes archivos de entrada:\n"
            f"{detalle}"
        )


def limpiar_geometrias(
    capa: gpd.GeoDataFrame,
    nombre: str,
) -> gpd.GeoDataFrame:
    """Elimina geometrías nulas o vacías y repara geometrías inválidas."""
    salida = capa.copy()

    salida = salida[
        salida.geometry.notna()
        & ~salida.geometry.is_empty
    ].copy()

    invalidas = (~salida.geometry.is_valid).sum()

    if invalidas > 0:
        print(
            f"{nombre}: se repararán {invalidas:,} "
            "geometrías inválidas."
        )
        salida["geometry"] = salida.geometry.make_valid()

    return salida


def verificar_crs(
    capas: dict[str, gpd.GeoDataFrame],
) -> None:
    """Verifica que todas las capas tengan un CRS definido."""
    sin_crs = [
        nombre
        for nombre, capa in capas.items()
        if capa.crs is None
    ]

    if sin_crs:
        raise ValueError(
            "Las siguientes capas no tienen CRS definido: "
            + ", ".join(sin_crs)
        )


def homogeneizar_crs(
    capas: dict[str, gpd.GeoDataFrame],
    crs_destino,
) -> dict[str, gpd.GeoDataFrame]:
    """Reproyecta todas las capas al CRS de destino."""
    resultado = {}

    for nombre, capa in capas.items():
        if capa.crs != crs_destino:
            print(
                f"Reproyectando {nombre}: "
                f"{capa.crs} → {crs_destino}"
            )
            resultado[nombre] = capa.to_crs(crs_destino)
        else:
            resultado[nombre] = capa.copy()

    return resultado


# ==========================================================
# 3. CARGA Y PREPARACIÓN DE LAS CAPAS
# ==========================================================

def cargar_y_preparar_capas():
    """Carga, limpia y homogeneiza las capas espaciales."""
    verificar_archivos_entrada()

    muestras_originales = gpd.read_file(RUTA_MUESTRAS)
    geologia = gpd.read_file(RUTA_GEOLOGIA)
    fallas = gpd.read_file(RUTA_FALLAS)
    municipios = gpd.read_file(RUTA_MUNICIPIOS)

    capas = {
        "muestras": limpiar_geometrias(
            muestras_originales,
            "Muestras",
        ),
        "geología": limpiar_geometrias(
            geologia,
            "Geología",
        ),
        "fallas": limpiar_geometrias(
            fallas,
            "Fallas",
        ),
        "municipios": limpiar_geometrias(
            municipios,
            "Municipios",
        ),
    }

    verificar_crs(capas)

    # Se adopta el CRS de municipios como referencia espacial.
    crs_destino = capas["municipios"].crs

    capas = homogeneizar_crs(
        capas,
        crs_destino,
    )

    muestras_originales = capas["muestras"]
    geologia = capas["geología"]
    fallas = capas["fallas"]
    municipios = capas["municipios"]

    print("\n" + "=" * 68)
    print("CAPAS CARGADAS Y VERIFICADAS")
    print("=" * 68)
    print(f"Muestras originales : {len(muestras_originales):,}")
    print(f"Municipios           : {len(municipios):,}")
    print(f"Geología             : {len(geologia):,}")
    print(f"Fallas               : {len(fallas):,}")
    print(f"CRS común            : {crs_destino}")
    print("=" * 68)

    return muestras_originales, geologia, fallas, municipios


# ==========================================================
# 4. CONVERSIÓN Y REVISIÓN DE LA VARIABLE Cu
# ==========================================================

def preparar_variable_cu(
    muestras_originales: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Convierte Cu a numérica y reporta problemas de calidad."""
    muestras_originales = muestras_originales.copy()

    if "Cu" not in muestras_originales.columns:
        raise KeyError(
            "La capa de muestras no contiene una columna llamada 'Cu'."
        )

    muestras_originales["Cu"] = pd.to_numeric(
        muestras_originales["Cu"],
        errors="coerce",
    )

    nulos = int(muestras_originales["Cu"].isna().sum())
    negativos = int((muestras_originales["Cu"] < 0).sum())

    print("\n" + "=" * 68)
    print("VERIFICACIÓN DE LA VARIABLE Cu")
    print("=" * 68)
    print(f"Valores nulos     : {nulos:,}")
    print(f"Valores negativos : {negativos:,}")
    print("-" * 68)
    display(muestras_originales["Cu"].describe())
    print("=" * 68)

    if negativos > 0:
        print(
            "Advertencia: existen concentraciones negativas. "
            "Revísalas antes de continuar con el análisis."
        )

    return muestras_originales


# ==========================================================
# 5. DELIMITACIÓN ESPACIAL DEL ÁREA DE ANÁLISIS
# ==========================================================

def delimitar_muestras(
    muestras_originales: gpd.GeoDataFrame,
    municipios: gpd.GeoDataFrame,
):
    """
    Clasifica las muestras dentro y fuera del polígono de estudio.

    Se utiliza covers() para incluir los puntos localizados
    exactamente sobre el límite.
    """
    poligono_estudio = municipios.geometry.union_all()

    mascara_dentro = muestras_originales.geometry.apply(
        lambda geometria: poligono_estudio.covers(geometria)
    )

    muestras_estudio = muestras_originales[
        mascara_dentro
    ].copy()

    muestras_fuera = muestras_originales[
        ~mascara_dentro
    ].copy()

    total_original = len(muestras_originales)
    total_dentro = len(muestras_estudio)
    total_fuera = len(muestras_fuera)

    if total_dentro + total_fuera != total_original:
        raise ValueError(
            "La clasificación espacial no conserva el total "
            "original de muestras."
        )

    print("\n" + "=" * 68)
    print("DELIMITACIÓN ESPACIAL COMPLETADA")
    print("=" * 68)
    print(f"Total original          : {total_original:,}")
    print(f"Dentro del área         : {total_dentro:,}")
    print(f"Fuera del área          : {total_fuera:,}")
    print(f"Conjunto oficial        : {total_dentro:,}")
    print("=" * 68)

    if total_original != 2103:
        print(
            f"Advertencia: se esperaban 2.103 muestras originales, "
            f"pero se encontraron {total_original:,}."
        )

    if total_dentro != 2029:
        print(
            f"Advertencia: se esperaban 2.029 muestras dentro, "
            f"pero se encontraron {total_dentro:,}."
        )

    if total_fuera != 74:
        print(
            f"Advertencia: se esperaban 74 muestras fuera, "
            f"pero se encontraron {total_fuera:,}."
        )

    return muestras_estudio, muestras_fuera, poligono_estudio


def guardar_capas_estudio(
    muestras_estudio: gpd.GeoDataFrame,
    muestras_fuera: gpd.GeoDataFrame,
) -> None:
    """Guarda los subconjuntos dentro y fuera del área."""
    muestras_estudio.to_file(
        RUTA_MUESTRAS_ESTUDIO,
        driver="GPKG",
    )

    muestras_fuera.to_file(
        RUTA_MUESTRAS_FUERA,
        driver="GPKG",
    )

    print(f"Capa de estudio guardada: {RUTA_MUESTRAS_ESTUDIO}")
    print(f"Capa excluida guardada  : {RUTA_MUESTRAS_FUERA}")


# ==========================================================
# 6. TABLA 01
# ==========================================================

def generar_tabla_01(
    muestras_originales: gpd.GeoDataFrame,
    muestras_estudio: gpd.GeoDataFrame,
    muestras_fuera: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """Genera la tabla del proceso de selección espacial."""
    total_inicial = len(muestras_originales)
    total_conservadas = len(muestras_estudio)
    total_excluidas = len(muestras_fuera)

    tabla_01 = pd.DataFrame(
        {
            "Etapa de selección": [
                "Total inicial de muestras",
                "Muestras excluidas del análisis",
                "Muestras conservadas para el análisis",
            ],
            "Criterio": [
                "Base geoquímica original",
                "Ubicación fuera del polígono del área de análisis",
                "Ubicación dentro del polígono del área de análisis",
            ],
            "Cantidad": [
                total_inicial,
                total_excluidas,
                total_conservadas,
            ],
            "Porcentaje del total (%)": [
                100.00,
                total_excluidas / total_inicial * 100,
                total_conservadas / total_inicial * 100,
            ],
        }
    )

    tabla_01_estilizada = (
        tabla_01.style
        .hide(axis="index")
        .set_caption(
            "Tabla 01. Selección de muestras para el área de análisis"
        )
        .format(
            {
                "Cantidad": "{:,.0f}",
                "Porcentaje del total (%)": "{:.2f}",
            }
        )
        .set_properties(
            subset=[
                "Cantidad",
                "Porcentaje del total (%)",
            ],
            **{"text-align": "center"},
        )
    )

    display(tabla_01_estilizada)

    tabla_01.to_csv(
        RUTA_TABLA_01,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"Tabla 01 guardada: {RUTA_TABLA_01}")
    return tabla_01


# ==========================================================
# 7. FIGURA 01
# ==========================================================

def generar_figura_01(
    muestras_originales: gpd.GeoDataFrame,
    muestras_estudio: gpd.GeoDataFrame,
    muestras_fuera: gpd.GeoDataFrame,
    municipios: gpd.GeoDataFrame,
) -> None:
    """Genera el mapa de delimitación espacial del área."""
    try:
        import contextily as ctx
    except ImportError:
        ctx = None
        print(
            "Advertencia: contextily no está instalado. "
            "La figura se generará sin mapa base."
        )

    limite_estudio = municipios.dissolve()

    total_inicial = len(muestras_originales)
    total_dentro = len(muestras_estudio)
    total_fuera = len(muestras_fuera)

    porcentaje_dentro = total_dentro / total_inicial * 100
    porcentaje_fuera = total_fuera / total_inicial * 100

    xmin, ymin, xmax, ymax = municipios.total_bounds
    margen_x = (xmax - xmin) * 0.05
    margen_y = (ymax - ymin) * 0.05

    fig, ax = plt.subplots(
        figsize=(10, 10),
        facecolor="white",
    )

    municipios.plot(
        ax=ax,
        facecolor="#F2F2F2",
        edgecolor="#888888",
        linewidth=0.55,
        alpha=0.72,
        zorder=2,
    )

    extension_x = (
        xmin - margen_x,
        xmax + margen_x,
    )
    extension_y = (
        ymin - margen_y,
        ymax + margen_y,
    )

    ax.set_xlim(*extension_x)
    ax.set_ylim(*extension_y)

    if ctx is not None:
        try:
            ctx.add_basemap(
                ax,
                source=ctx.providers.CartoDB.Positron,
                crs=municipios.crs,
                zoom=9,
                attribution=False,
                alpha=0.65,
                zorder=1,
            )
        except Exception as error:
            print(
                "Advertencia: no fue posible cargar el mapa base."
            )
            print(error)

    # Restaurar la extensión después del mapa base.
    ax.set_xlim(*extension_x)
    ax.set_ylim(*extension_y)

    muestras_estudio.plot(
        ax=ax,
        color="#2E86DE",
        marker="o",
        markersize=14,
        edgecolor="white",
        linewidth=0.30,
        alpha=0.88,
        zorder=4,
    )

    muestras_fuera.plot(
        ax=ax,
        color="#E31A1C",
        marker="x",
        markersize=55,
        linewidth=1.6,
        alpha=0.98,
        zorder=7,
    )

    limite_estudio.boundary.plot(
        ax=ax,
        color="#111111",
        linewidth=1.75,
        zorder=6,
    )

    ax.set_aspect("equal")
    ax.set_xlabel("Coordenada Este (m)", fontsize=10)
    ax.set_ylabel("Coordenada Norte (m)", fontsize=10)

    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    formato = ScalarFormatter(
        useOffset=False,
        useMathText=False,
    )
    formato.set_scientific(False)

    ax.xaxis.set_major_formatter(formato)
    ax.yaxis.set_major_formatter(formato)

    ax.tick_params(
        axis="both",
        labelsize=8.5,
        direction="out",
        length=4,
        width=0.8,
    )
    ax.ticklabel_format(
        style="plain",
        axis="both",
        useOffset=False,
    )
    ax.grid(False)

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
        arrowprops={
            "facecolor": "#111111",
            "edgecolor": "#111111",
            "width": 3.3,
            "headwidth": 9.5,
            "headlength": 9.5,
        },
        zorder=10,
    )

    ax.add_artist(
        ScaleBar(
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
            pad=0.4,
        )
    )

    epsg = municipios.crs.to_epsg()
    texto_crs = (
        f"CRS: EPSG:{epsg}"
        if epsg is not None
        else f"CRS: {municipios.crs.name}"
    )

    ax.text(
        0.985,
        0.018,
        texto_crs,
        transform=ax.transAxes,
        fontsize=7.3,
        ha="right",
        va="bottom",
        color="#333333",
        bbox={
            "facecolor": "white",
            "edgecolor": "#888888",
            "linewidth": 0.50,
            "alpha": 0.92,
            "boxstyle": "round,pad=0.25",
        },
        zorder=10,
    )

    elementos_leyenda = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            markerfacecolor="#2E86DE",
            markeredgecolor="white",
            markersize=7,
            label=(
                f"Dentro del área: {total_dentro:,} "
                f"({porcentaje_dentro:.2f} %)"
            ),
        ),
        Line2D(
            [0],
            [0],
            marker="x",
            linestyle="none",
            color="#E31A1C",
            markeredgewidth=1.7,
            markersize=8,
            label=(
                f"Fuera del área: {total_fuera:,} "
                f"({porcentaje_fuera:.2f} %)"
            ),
        ),
        Line2D(
            [],
            [],
            linestyle="none",
            label=f"Total inicial: {total_inicial:,}",
        ),
    ]

    leyenda = ax.legend(
        handles=elementos_leyenda,
        loc="upper right",
        bbox_to_anchor=(0.88, 0.985),
        frameon=True,
        facecolor="white",
        edgecolor="#888888",
        framealpha=0.96,
        fontsize=8.5,
        title="Clasificación espacial",
        title_fontsize=9,
        borderpad=0.8,
        labelspacing=0.6,
    )
    leyenda._legend_box.align = "left"

    for borde in ax.spines.values():
        borde.set_visible(True)
        borde.set_color("#333333")
        borde.set_linewidth(0.85)

    fig.text(
        0.98,
        0.018,
        (
            "Fuente: base geoquímica de Cu y cartografía municipal. "
            "Clasificación y elaboración propia."
        ),
        ha="right",
        va="bottom",
        fontsize=7.3,
        color="#444444",
    )

    fig.subplots_adjust(
        left=0.10,
        right=0.97,
        bottom=0.11,
        top=0.98,
    )

    fig.savefig(
        RUTA_FIGURA_01,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )

    print(f"Figura 01 guardada: {RUTA_FIGURA_01}")
    plt.show()


# ==========================================================
# 8. FLUJO PRINCIPAL
# ==========================================================

def main():
    """Ejecuta el capítulo completo de preparación de datos."""
    (
        muestras_originales,
        geologia,
        fallas,
        municipios,
    ) = cargar_y_preparar_capas()

    muestras_originales = preparar_variable_cu(
        muestras_originales
    )

    (
        muestras,
        muestras_fuera,
        poligono_estudio,
    ) = delimitar_muestras(
        muestras_originales,
        municipios,
    )

    guardar_capas_estudio(
        muestras,
        muestras_fuera,
    )

    tabla_01 = generar_tabla_01(
        muestras_originales,
        muestras,
        muestras_fuera,
    )

    generar_figura_01(
        muestras_originales,
        muestras,
        muestras_fuera,
        municipios,
    )

    print("\n" + "=" * 72)
    print("SCRIPT 02 COMPLETADO CORRECTAMENTE")
    print("=" * 72)

    # Se devuelven los objetos principales para uso interactivo.
    return {
        "muestras_originales": muestras_originales,
        "muestras": muestras,
        "muestras_estudio": muestras,
        "muestras_fuera": muestras_fuera,
        "geologia": geologia,
        "fallas": fallas,
        "municipios": municipios,
        "poligono_estudio": poligono_estudio,
        "tabla_01": tabla_01,
    }


RESULTADOS_SCRIPT = main()

# Publicar las variables en el espacio global cuando se usa %run.
globals().update(RESULTADOS_SCRIPT)

