# Ejecución del proyecto en Google Colab

## 1. Copiar el proyecto a Drive

La ruta predeterminada es:

```text
/content/drive/MyDrive/Analisis_Geoespacial_Cobre
```

La carpeta debe estar directamente dentro de `MyDrive`.

## 2. Abrir un notebook de control

Puede usar el notebook principal o crear uno nuevo con estas celdas.

### Celda 1: montar Drive

```python
from google.colab import drive
drive.mount("/content/drive")
```

### Celda 2: instalar dependencias

```python
!pip -q install -r "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/requirements.txt"
```

Después de una instalación importante, Colab puede solicitar reiniciar la sesión.

### Celda 3: ejecutar el proyecto completo

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/05_patron_anomalias.py"
```

## 3. Ejecución diagnóstica

Para identificar el punto exacto de un error, ejecute uno por uno:

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/01_config.py"
```

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/02_preparacion_datos.py"
```

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/03_introduccion_datos_espaciales.py"
```

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/04_patron_muestreo.py"
```

```python
%run "/content/drive/MyDrive/Analisis_Geoespacial_Cobre/05_Scripts/05_patron_anomalias.py"
```

## 4. Verificar archivos

```python
from pathlib import Path

proyecto = Path(
    "/content/drive/MyDrive/Analisis_Geoespacial_Cobre"
)

esperados = [
    proyecto / "02_Datos/02_Procesados/Muestras_Cu.gpkg",
    proyecto / "02_Datos/02_Procesados/Geologia_Suroeste.gpkg",
    proyecto / "02_Datos/02_Procesados/Fallas_Suroeste.gpkg",
    proyecto / "02_Datos/02_Procesados/Municipios_Suroeste.gpkg",
]

for archivo in esperados:
    print("OK" if archivo.exists() else "FALTA", archivo)
```

## 5. Revisar salidas

```python
for carpeta in [
    proyecto / "03_Figuras",
    proyecto / "04_Resultados/01_Tablas",
    proyecto / "02_Datos/03_Estudio",
]:
    print("\n", carpeta)
    for archivo in sorted(carpeta.glob("*")):
        print(" -", archivo.name)
```

## 6. Recomendaciones

- Mantenga el notebook como documento narrativo y los scripts como versión reproducible.
- No cambie nombres de carpetas sin actualizar `01_config.py`.
- Ejecute primero el script 02 cuando cambien los datos de entrada.
- Conserve la semilla para comparar resultados.
- Descargue una copia de figuras y tablas antes de hacer cambios metodológicos importantes.
