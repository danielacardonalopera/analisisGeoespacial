# Análisis Geoespacial de la Distribución del Cobre en el Suroeste Antioqueño

Repositorio del proyecto desarrollado para el curso **Análisis Geoespacial** de la **Facultad de Minas – Universidad Nacional de Colombia**.

Este proyecto aplica técnicas de análisis espacial a una base de **2.029 muestras geoquímicas de cobre (Cu)** con el objetivo de comprender su distribución espacial y estimar la concentración del metal en zonas donde no existen mediciones directas.

La metodología sigue la estructura del curso, desarrollando progresivamente el análisis desde los **datos puntuales**, pasando por los **datos de área**, hasta la construcción de **superficies continuas** mediante técnicas de interpolación y modelos probabilísticos.

---

# Objetivo

Analizar la distribución espacial del cobre en el Suroeste antioqueño mediante técnicas modernas de análisis geoespacial y comparar diferentes métodos para estimar la concentración de cobre y su incertidumbre en todo el territorio de estudio.

---

# Estructura del proyecto

## 1. Planteamiento del problema

- Contexto geológico del área de estudio.
- Definición del problema de investigación.
- Justificación.
- Objetivos.
- Relevancia para la exploración minera.

---

## 2. Análisis de datos puntuales

Estudio del patrón espacial de las muestras y de las anomalías geoquímicas.

### Temas desarrollados

- Preparación de datos espaciales
- Exploración de datos
- Centrografía
- Densidad Kernel
- Vecino más cercano (Clark & Evans)
- Definición de anomalías geoquímicas
- Funciones G, F y K de Ripley
- Conteo por cuadrantes
- Simulación Monte Carlo
- Relación entre anomalías, geología y fallas

---

## 3. Análisis de datos de área

Conversión de información puntual en unidades espaciales agregadas para estudiar la dependencia espacial.

### Métodos implementados

- Construcción de malla regular
- Estadísticos zonales
- Mapas coropléticos
- Índice de Moran
- Indicadores Locales de Asociación Espacial (LISA)
- Regresión lineal (OLS)
- Modelos autorregresivos espaciales (SAR)
- Regresión Geográficamente Ponderada (GWR)
- Regresión Geográficamente Ponderada Multiescala (MGWR)

---

## 4. Análisis de superficies

Estimación continua de la concentración de cobre mediante métodos determinísticos, geoestadísticos y probabilísticos.

### Métodos determinísticos

- Vecino más cercano
- Inverse Distance Weighting (IDW)
- Triangulación de Delaunay
- Polígonos de Thiessen (Voronoi)

### Geoestadística

- Semivariograma experimental
- Ajuste de modelos teóricos
- Kriging Ordinario
- Kriging Universal

### Procesos Gaussianos

- Fundamentos probabilísticos
- Comparación de kernels
- Procesos Gaussianos espaciales
- Incorporación de covariables
- Mapas de incertidumbre
- Validación cruzada espacial

---

# Datos utilizados

El proyecto integra diferentes fuentes de información espacial:

- 2.029 muestras geoquímicas de cobre (Cu)
- Cartografía geológica
- Red de fallas geológicas
- Límites municipales del Suroeste antioqueño
- Modelo Digital de Elevación (DEM)

**Sistema de referencia:** EPSG:21897 (Bogotá 1975 / Colombia West Zone).

---

# Herramientas utilizadas

- Python
- Jupyter Notebook
- GeoPandas
- NumPy
- Pandas
- SciPy
- Matplotlib
- Scikit-Learn
- Scikit-GStat
- PyKrige
- PySAL
- MGWR
- Rasterio
- QGIS

---

# Resultados

El proyecto permitió:

- Caracterizar el patrón espacial del muestreo.
- Identificar anomalías geoquímicas de cobre.
- Analizar la autocorrelación espacial de las concentraciones.
- Evaluar la influencia de variables geológicas y topográficas.
- Comparar distintos métodos de interpolación espacial.
- Generar mapas continuos de concentración e incertidumbre.
- Validar el desempeño de cada modelo mediante validación cruzada espacial.

---

# Contenido del repositorio

```
├── data/                  # Datos espaciales utilizados
├── notebooks/             # Notebook principal del proyecto
├── figures/               # Mapas y figuras generadas
├── outputs/               # Resultados del análisis
├── presentations/         # Entregables y exposiciones del curso
├── article/               # Artículo científico derivado del proyecto
└── README.md
```

---

# Publicación asociada

Como resultado del proyecto se desarrolló un artículo científico que integra todos los análisis realizados durante el curso bajo un enfoque metodológico progresivo para la representación espacial de variables geoquímicas.

---

# Autora

**Daniela Cardona Lopera**

Facultad de Minas  
Universidad Nacional de Colombia

Curso de Análisis Geoespacial