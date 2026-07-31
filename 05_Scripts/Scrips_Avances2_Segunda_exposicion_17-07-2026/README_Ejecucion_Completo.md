# Guía técnica de ejecución de los scripts

Esta guía describe cómo instalar, organizar, verificar y ejecutar el proyecto modular ubicado en `05_Scripts`.

## 1. Orden de dependencia

Los scripts forman una cadena:

```text
01_config.py
      ↓
02_preparacion_datos.py
      ↓
03_introduccion_datos_espaciales.py
      ↓
04_patron_muestreo.py
      ↓
05_patron_anomalias.py
```

Cada archivo carga el anterior mediante `runpy`. Por ello, ejecutar `05_patron_anomalias.py` inicia el flujo completo.

## 2. Estructura obligatoria

```text
Analisis_Geoespacial_Cobre/
├── requirements.txt
├── 02_Datos/
│   ├── 02_Procesados/
│   │   ├── Muestras_Cu.gpkg
│   │   ├── Geologia_Suroeste.gpkg
│   │   ├── Fallas_Suroeste.gpkg
│   │   └── Municipios_Suroeste.gpkg
│   └── 03_Estudio/
├── 03_Figuras/
├── 04_Resultados/
│   ├── 01_Tablas/
│   ├── 02_Modelos/
│   └── 03_Validacion/
└── 05_Scripts/
    ├── 01_config.py
    ├── 02_preparacion_datos.py
    ├── 03_introduccion_datos_espaciales.py
    ├── 04_patron_muestreo.py
    └── 05_patron_anomalias.py
```

`01_config.py` crea automáticamente las carpetas de salida, pero no crea los cuatro archivos espaciales de entrada.

## 3. Instalación

En Colab:

```python
!pip -q install -r "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/requirements.txt"
```

En terminal local:

```bash
python -m venv .venv
```

Activación en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activación en macOS o Linux:

```bash
source .venv/bin/activate
```

Instalación:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Comprobaciones previas

Antes de ejecutar:

- confirme que los cinco scripts están en la misma carpeta;
- confirme que los cuatro GeoPackage tienen los nombres esperados;
- confirme que `Muestras_Cu.gpkg` contiene la columna `Cu`;
- confirme que las capas tienen CRS definido;
- confirme que la carpeta raíz se llama `Analisis_Geoespacial_Cobre` cuando se use la configuración predeterminada de Colab.

## 5. Ejecución completa

En Colab:

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/05_patron_anomalias.py"
```

Desde una terminal local, una vez ajustada `RUTA_PROYECTO`:

```bash
python 05_Scripts/05_patron_anomalias.py
```

## 6. Ejecución por etapas

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/01_config.py"
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/02_preparacion_datos.py"
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/03_introduccion_datos_espaciales.py"
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/04_patron_muestreo.py"
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/05_patron_anomalias.py"
```

Ejecutar por etapas facilita localizar errores y revisar resultados intermedios.

## 7. Qué produce cada script

### `01_config.py`

- monta Google Drive en Colab;
- crea directorios;
- importa librerías comunes;
- define `CRS_PROYECTO`, semilla, simulaciones y significancia;
- define funciones generales de exportación.

### `02_preparacion_datos.py`

- carga muestras, geología, fallas y municipios;
- elimina geometrías nulas o vacías;
- repara geometrías inválidas;
- homogeneiza CRS;
- convierte `Cu` a numérico;
- separa muestras dentro y fuera del área;
- genera y exporta Tabla 01 y Figura 01.

### `03_introduccion_datos_espaciales.py`

Ejecuta las celdas correspondientes al capítulo introductorio y conserva los nombres de variables del notebook original.

### `04_patron_muestreo.py`

Ejecuta los análisis del patrón de las 2.029 muestras: distribución, centro, dispersión, densidad y vecino más cercano.

### `05_patron_anomalias.py`

Ejecuta los análisis de las anomalías: indicador, densidad, vecino más cercano, contrastes Monte Carlo, funciones espaciales y relación con geología y fallas.

## 8. Reejecución

Los archivos de salida con el mismo nombre pueden sobrescribirse. Para conservar versiones anteriores:

1. copie las carpetas `03_Figuras` y `04_Resultados`;
2. cambie el nombre de la copia con fecha o versión;
3. ejecute nuevamente.

## 9. Errores frecuentes

### No se encontró `01_config.py`

Los cinco scripts deben permanecer juntos dentro de `05_Scripts`.

### No se encontró un GeoPackage

Revise nombres y ubicación en `02_Datos/02_Procesados`.

### La columna `Cu` no existe

Compruebe mayúsculas, espacios y nombre exacto del campo.

### Error de CRS

Abra las capas en QGIS, asigne o reproyecte correctamente el sistema de referencia y vuelva a exportarlas.

### No aparece el mapa base

Puede deberse a falta de conexión a internet. El análisis espacial puede continuar; solo afecta la cartografía de contexto.

### Error de memoria

Reinicie el entorno, ejecute por etapas y cierre figuras anteriores con:

```python
import matplotlib.pyplot as plt
plt.close("all")
```

### Resultados distintos entre ejecuciones

Revise que la semilla y el número de simulaciones no hayan sido modificados en `01_config.py`.

## 10. Validación final

La ejecución se considera satisfactoria cuando:

- no hay excepciones;
- se crean las capas de estudio;
- se actualizan tablas y figuras;
- los conteos de muestras son coherentes;
- aparecen los mensajes `COMPLETADO` de cada script.
