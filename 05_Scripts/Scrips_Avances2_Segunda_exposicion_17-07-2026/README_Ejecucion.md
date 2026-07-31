# Guía técnica de ejecución

## Nueva arquitectura

La ejecución ya no utiliza `runpy` ni rutas de Google Drive.

```text
config.py       → rutas y parámetros
utils.py        → funciones compartidas
01_...py        → preparación
02_...py        → datos espaciales
03_...py        → patrón de muestreo
04_...py        → anomalías
run_all.py      → orquestación completa
```

## Principio de portabilidad

`config.py` identifica la raíz del repositorio con:

```python
RUTA_PROYECTO = Path(__file__).resolve().parents[1]
```

Por ello, cualquier persona puede clonar el repositorio en cualquier
carpeta y ejecutar el proyecto sin editar rutas.

## Ejecución completa

Abra una terminal en la raíz del repositorio:

```bash
python 05_Scripts/run_all.py
```

`run_all.py` ejecuta cada etapa en un proceso independiente. Si una etapa
falla, el proceso se detiene y conserva el mensaje de error original.

## Ejecución por etapas

```bash
python 05_Scripts/01_preparacion_datos.py
```

Genera las capas delimitadas, la primera tabla y la primera figura.

```bash
python 05_Scripts/02_datos_espaciales.py
```

Ejecuta la exploración estadística y espacial introductoria.

```bash
python 05_Scripts/03_patron_muestreo.py
```

Analiza el patrón de las muestras.

```bash
python 05_Scripts/04_patron_anomalias.py
```

Analiza el patrón espacial de las anomalías y sus relaciones geológicas.

## Verificación previa

```bash
python -c "from pathlib import Path; print(Path.cwd())"
```

Compruebe que se encuentra en la raíz del repositorio y que existen:

```text
02_Datos/02_Procesados/Muestras_Cu.gpkg
02_Datos/02_Procesados/Geologia_Suroeste.gpkg
02_Datos/02_Procesados/Fallas_Suroeste.gpkg
02_Datos/02_Procesados/Municipios_Suroeste.gpkg
```

## Errores frecuentes

### `ModuleNotFoundError`

Active el entorno virtual e instale:

```bash
pip install -r requirements.txt
```

### No se encuentra una capa

Revise nombres y ubicación en `02_Datos/02_Procesados`.

### No existe el campo `Cu`

El nombre es sensible a mayúsculas y espacios.

### Error de CRS

Asigne o reproyecte correctamente las capas en QGIS.

### Error de memoria

Ejecute las etapas por separado y cierre figuras anteriores.

## Reproducibilidad

Los parámetros generales se centralizan en `config.py`:

- CRS;
- semilla;
- simulaciones;
- significancia;
- percentil de anomalía;
- mínimo de muestras por unidad.
