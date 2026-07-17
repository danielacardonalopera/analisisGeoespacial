# 05_Scripts/02_carga_y_preprocesamiento.py
import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd

# Asegurar que Python reconozca la carpeta 05_Scripts para las importaciones
sys.path.append(str(Path(__file__).resolve().parent))
from 01_config import obtener_rutas

def cargar_y_limpiar_datos(rutas):
    """Carga las capas vectoriales locales y limpia la variable Cu."""
    print("Cargando capas espaciales desde '02_Datos/02_Procesados'...")
    
    # Carga de archivos locales (.gpkg)
    muestras = gpd.read_file(rutas["PROCESADOS"] / "Muestras_Cu.gpkg")
    geologia = gpd.read_file(rutas["PROCESADOS"] / "Geologia_Suroeste.gpkg")
    fallas = gpd.read_file(rutas["PROCESADOS"] / "Fallas_Suroeste.gpkg")
    municipios = gpd.read_file(rutas["PROCESADOS"] / "Municipios_Suroeste.gpkg")
    
    # Validación de CRS
    assert muestras.crs == geologia.crs == fallas.crs == municipios.crs, "¡Alerta! Los CRS no coinciden."
    print(f"Sistemas de coordenadas verificados (CRS común: {muestras.crs})")
    
    # Limpieza
    muestras["Cu"] = pd.to_numeric(muestras["Cu"], errors="coerce")
    muestras = muestras.dropna(subset=["Cu"])
    
    print(f"Datos cargados con éxito. Muestras válidas: {len(muestras)}")
    return muestras, geologia, fallas, municipios

if __name__ == "__main__":
    rutas = obtener_rutas()
    muestras, geologia, fallas, municipios = cargar_y_limpiar_datos(rutas)
