"""
Funciones auxiliares compartidas por los scripts del proyecto.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from config import (
    ESTUDIO,
    FIGURAS,
    PROCESADOS,
    TABLAS,
)


ARCHIVOS_ENTRADA = {
    "muestras": PROCESADOS / "Muestras_Cu.gpkg",
    "geologia": PROCESADOS / "Geologia_Suroeste.gpkg",
    "fallas": PROCESADOS / "Fallas_Suroeste.gpkg",
    "municipios": PROCESADOS / "Municipios_Suroeste.gpkg",
}


def verificar_archivos_entrada() -> dict[str, Path]:
    """Valida la existencia de las cuatro capas mínimas."""
    faltantes = {
        nombre: ruta
        for nombre, ruta in ARCHIVOS_ENTRADA.items()
        if not ruta.exists()
    }

    if faltantes:
        detalle = "\n".join(
            f"- {nombre}: {ruta}"
            for nombre, ruta in faltantes.items()
        )
        raise FileNotFoundError(
            "Faltan archivos en 02_Datos/02_Procesados:\n"
            f"{detalle}"
        )

    return ARCHIVOS_ENTRADA.copy()


def limpiar_geometrias(
    capa: gpd.GeoDataFrame,
    nombre: str = "capa",
) -> gpd.GeoDataFrame:
    """Elimina geometrías nulas/vacías y repara inválidas."""
    salida = capa[
        capa.geometry.notna()
        & ~capa.geometry.is_empty
    ].copy()

    invalidas = int((~salida.geometry.is_valid).sum())
    if invalidas:
        print(f"{nombre}: reparando {invalidas:,} geometrías.")
        salida["geometry"] = salida.geometry.make_valid()

    return salida


def cargar_capas_base(
    *,
    preferir_muestras_estudio: bool = True,
) -> dict[str, gpd.GeoDataFrame]:
    """
    Carga las capas requeridas por los capítulos analíticos.

    Si ya existe la capa delimitada generada por el script 01, se usa
    como `muestras`. En caso contrario se carga la capa procesada.
    """
    verificar_archivos_entrada()

    ruta_estudio = ESTUDIO / "Muestras_Cu_Area_Estudio.gpkg"
    ruta_muestras = (
        ruta_estudio
        if preferir_muestras_estudio and ruta_estudio.exists()
        else ARCHIVOS_ENTRADA["muestras"]
    )

    capas = {
        "muestras": limpiar_geometrias(
            gpd.read_file(ruta_muestras),
            "Muestras",
        ),
        "geologia": limpiar_geometrias(
            gpd.read_file(ARCHIVOS_ENTRADA["geologia"]),
            "Geología",
        ),
        "fallas": limpiar_geometrias(
            gpd.read_file(ARCHIVOS_ENTRADA["fallas"]),
            "Fallas",
        ),
        "municipios": limpiar_geometrias(
            gpd.read_file(ARCHIVOS_ENTRADA["municipios"]),
            "Municipios",
        ),
    }

    crs_destino = capas["municipios"].crs
    if crs_destino is None:
        raise ValueError("La capa de municipios no tiene CRS definido.")

    for nombre, capa in capas.items():
        if capa.crs is None:
            raise ValueError(f"La capa {nombre} no tiene CRS definido.")
        if capa.crs != crs_destino:
            capas[nombre] = capa.to_crs(crs_destino)

    capas["muestras_estudio"] = capas["muestras"]
    return capas


def guardar_figura(
    figura,
    nombre_archivo: str,
    *,
    dpi: int = 300,
    cerrar: bool = False,
) -> Path:
    """Guarda una figura en 03_Figuras."""
    ruta = FIGURAS / nombre_archivo
    figura.savefig(
        ruta,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.15,
    )
    if cerrar:
        plt.close(figura)
    print(f"Figura guardada: {ruta}")
    return ruta


def guardar_tabla(
    tabla: pd.DataFrame,
    nombre_archivo: str,
    *,
    indice: bool = False,
) -> Path:
    """Guarda una tabla CSV en 04_Resultados/01_Tablas."""
    ruta = TABLAS / nombre_archivo
    tabla.to_csv(ruta, index=indice, encoding="utf-8-sig")
    print(f"Tabla guardada: {ruta}")
    return ruta


def publicar_contexto(
    destino: dict[str, Any],
    contexto: dict[str, Any],
) -> None:
    """Publica variables de un diccionario en el espacio global."""
    destino.update(contexto)
