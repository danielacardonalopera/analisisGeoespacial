# 05_Scripts/01_config.py
from pathlib import Path

def obtener_rutas():
    """
    Define y retorna las rutas del proyecto de forma relativa.
    Asume que este script se encuentra en '[raiz_proyecto]/05_Scripts/01_config.py'.
    """
    RUTA_PROYECTO = Path(__file__).resolve().parent.parent
    
    rutas = {
        "PROYECTO": RUTA_PROYECTO,
        "DATOS": RUTA_PROYECTO / "02_Datos",
        "ORIGINALES": RUTA_PROYECTO / "02_Datos" / "01_Originales",
        "PROCESADOS": RUTA_PROYECTO / "02_Datos" / "02_Procesados",
        "ESTUDIO": RUTA_PROYECTO / "02_Datos" / "03_Estudio",
        "FIGURAS": RUTA_PROYECTO / "03_Figuras",
        "RESULTADOS": RUTA_PROYECTO / "04_Resultados",
        "SCRIPTS": RUTA_PROYECTO / "05_Scripts",
        "DOCUMENTACION": RUTA_PROYECTO / "06_Documentacion"
    }
    
    # Crear carpetas de salida automáticamente si no existen
    rutas["FIGURAS"].mkdir(parents=True, exist_ok=True)
    rutas["RESULTADOS"].mkdir(parents=True, exist_ok=True)
            
    return rutas

if __name__ == "__main__":
    rutas = obtener_rutas()
    print("Rutas configuradas para entorno local:")
    for k, v in rutas.items():
        print(f"  {k}: {v}")
