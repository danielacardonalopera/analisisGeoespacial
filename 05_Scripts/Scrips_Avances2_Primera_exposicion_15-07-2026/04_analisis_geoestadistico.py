# 05_Scripts/04_analisis_geoestadistico.py
import sys
import numpy as np
import skgstat as gs
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from 01_config import obtener_rutas
from 02_carga_y_preprocesamiento import cargar_y_limpiar_datos

def modelar_variograma(muestras, rutas):
    """Calcula y ajusta el semivariograma espacial para la distribución de Cobre."""
    print("Calculando semivariograma espacial...")
    
    # Extraer coordenadas X, Y y valores de Cu
    coords = np.column_stack((muestras.geometry.x, muestras.geometry.y))
    valores = muestras["Cu"].values
    
    # Configurar el variograma experimental
    V = gs.Variogram(coords, valores, model='spherical', n_lags=15, maxlag=20000)
    
    # Guardar gráfico del variograma ajustado
    fig = V.plot(show=False)
    ruta_figura = rutas["FIGURAS"] / "variograma_ajustado_Cu.png"
    plt.savefig(ruta_figura, dpi=300)
    plt.close()
    
    print(f"Variograma modelado exitosamente.")
    print(f"Parámetros óptimos -> Range: {V.parameters[0]:.2f} m, Sill: {V.parameters[1]:.2f}")
    print(f"Gráfico del variograma guardado en: {ruta_figura}")
    return V

if __name__ == "__main__":
    rutas = obtener_rutas()
    muestras, _, _, _ = cargar_y_limpiar_datos(rutas)
    modelar_variograma(muestras, rutas)
