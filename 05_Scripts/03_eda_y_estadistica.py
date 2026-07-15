# 05_Scripts/03_eda_y_estadistica.py
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path(__file__).resolve().parent))
from 01_config import obtener_rutas
from 02_carga_y_preprocesamiento import cargar_y_limpiar_datos

def analizar_estadisticas_cobre(muestras, rutas):
    """Calcula estadísticas y guarda los gráficos localmente."""
    print("=== Análisis Descriptivo de Cu (ppm) ===")
    resumen = muestras["Cu"].describe()
    print(resumen)
    
    # Exportar resultados
    resumen.to_csv(rutas["RESULTADOS"] / "resumen_estadistico_Cu.csv")
    print(f"Resumen guardado en: {rutas['RESULTADOS'] / 'resumen_estadistico_Cu.csv'}")
    
    # Gráficos
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(muestras["Cu"], kde=True, ax=axes[0], color="teal")
    axes[0].set_title("Distribución de Concentración de Cobre (Cu)")
    axes[0].set_xlabel("Cu (ppm)")
    
    sns.boxplot(x=muestras["Cu"], ax=axes[1], color="lightseagreen")
    axes[1].set_title("Diagrama de Caja de Concentración de Cobre (Cu)")
    axes[1].set_xlabel("Cu (ppm)")
    
    plt.tight_layout()
    ruta_figura = rutas["FIGURAS"] / "eda_distribucion_Cu.png"
    plt.savefig(ruta_figura, dpi=300)
    plt.close()
    print(f"Gráfico guardado en: {ruta_figura}")

if __name__ == "__main__":
    rutas = obtener_rutas()
    muestras, _, _, _ = cargar_y_limpiar_datos(rutas)
    analizar_estadisticas_cobre(muestras, rutas)
