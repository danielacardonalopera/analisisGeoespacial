# Instalación y ejecución local

## 1. Descargar o clonar

```bash
git clone URL_DEL_REPOSITORIO
cd Analisis_Geoespacial_Cobre
```

También puede descargar el ZIP de GitHub y descomprimirlo.

## 2. Crear entorno

```bash
python -m venv .venv
```

Active el entorno según su sistema operativo e instale:

```bash
pip install -r requirements.txt
```

## 3. Añadir los datos

Copie los cuatro GeoPackage a:

```text
02_Datos/02_Procesados/
```

## 4. Ejecutar

```bash
python 05_Scripts/run_all.py
```

No es necesario editar rutas.

## 5. Ejecutar desde VS Code

1. Abra la carpeta raíz del repositorio.
2. Seleccione el intérprete `.venv`.
3. Abra `05_Scripts/run_all.py`.
4. Use **Run Python File**.

## 6. Ejecutar desde Jupyter

Desde una celda ubicada en la raíz:

```python
%run 05_Scripts/run_all.py
```

Para una etapa específica:

```python
%run 05_Scripts/03_patron_muestreo.py
```
