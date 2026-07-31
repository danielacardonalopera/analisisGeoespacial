# Análisis Geoestadístico de la Distribución Espacial del Cobre en el Suroeste de Antioquia

## Descripción

Este repositorio contiene el desarrollo del proyecto de **Análisis
Geoespacial** realizado en Google Colab como parte de la Maestría en
Ingeniería -- Recursos Minerales.

El objetivo del estudio es analizar la distribución espacial de las
concentraciones de cobre (Cu) mediante técnicas de análisis exploratorio
espacial y geoestadística, utilizando interpolación por **Kriging
Ordinario** para generar un modelo continuo de distribución y su
correspondiente mapa de incertidumbre.

------------------------------------------------------------------------

# Estado del proyecto

Actualmente el proyecto se encuentra en desarrollo.

## Avance metodológico

-   ✅ Preparación de la información
-   ✅ Análisis exploratorio de los datos
-   ✅ Exploración espacial
-   ✅ Evaluación de la anisotropía
-   ✅ Variograma experimental
-   ✅ Ajuste del modelo variográfico
-   🔄 Validación cruzada (en desarrollo)
-   ⏳ Kriging ordinario
-   ⏳ Mapa de incertidumbre
-   ⏳ Conclusiones

------------------------------------------------------------------------

# Metodología

## 1. Preparación de la información

**Objetivo:** organizar, depurar y validar la información espacial y
geoquímica antes del análisis estadístico y geoestadístico.

### 1.1 Organización de la información

### 1.2 Carga de datos

### 1.3 Verificación de las capas espaciales

### 1.4 Conversión y revisión de la variable Cu

### 1.5 Verificación de geometrías

------------------------------------------------------------------------

## 2. Análisis exploratorio de los datos

**Objetivo:** caracterizar estadísticamente la distribución de la
concentración de cobre y evaluar el comportamiento de la variable antes
del análisis espacial.

### 2.1 Estadística descriptiva

### 2.2 Estadísticos complementarios

### 2.3 Histograma

### 2.4 Gráfico Q-Q

### 2.5 Prueba de normalidad de Anderson-Darling

### 2.6 Diagrama de caja (Boxplot)

------------------------------------------------------------------------

## 3. Exploración espacial

**Objetivo:** analizar la distribución espacial de las muestras de cobre
y su relación con el contexto geológico y estructural del área de
estudio.

### 3.1 Preparación de la base cartográfica

### 3.2 Localización del área de estudio

### 3.3 Distribución espacial de las muestras de cobre

### 3.4 Verificación de la cobertura espacial

### 3.5 Distribución de las muestras sobre las unidades geológicas

#### 3.5.1 Preparación de la cartografía geológica

#### 3.5.2 Distribución espacial de las muestras sobre las unidades geológicas

#### 3.5.3 Distribución de las muestras geoquímicas por unidad geológica

### 3.6 Distribución de las muestras de cobre respecto a las fallas geológicas

#### 3.6.1 Preparación de la cartografía estructural

#### 3.6.2 Distribución espacial de las muestras respecto a las fallas geológicas

#### 3.6.3 Proximidad de las muestras de cobre a las fallas geológicas

------------------------------------------------------------------------

## 4. Análisis geoestadístico

**Objetivo:** modelar la variabilidad espacial de la concentración de
cobre mediante técnicas geoestadísticas y generar una superficie
continua de interpolación.

### 4.1 Análisis exploratorio de la variable Cu en el área de estudio

### 4.2 Evaluación de la anisotropía

### 4.3 Variograma experimental

### 4.4 Ajuste del modelo variográfico

### 4.5 Validación cruzada

### 4.6 Interpolación espacial mediante Kriging Ordinario

### 4.7 Evaluación de la incertidumbre de la interpolación

------------------------------------------------------------------------

## 5. Conclusiones

En desarrollo.

------------------------------------------------------------------------

# Estructura del repositorio

``` text
Analisis_Geoespacial_Cobre_Antioquia
│
├── 01_Notebook/
├── 02_Datos/
│   ├── 01_Brutos/
│   ├── 02_Procesados/
│   └── 03_Capas_Base/
├── 03_Figuras/
├── 04_Tablas/
├── 05_Resultados/
│   ├── Variogramas/
│   ├── Validacion_Cruzada/
│   ├── Kriging/
│   ├── Incertidumbre/
│   └── Raster/
├── 06_Scripts/
├── 07_Documentacion/
├── README.md
├── requirements.txt
└── LICENSE
```

------------------------------------------------------------------------

# Herramientas utilizadas

-   Python 3
-   Google Colab
-   GeoPandas
-   NumPy
-   Pandas
-   Matplotlib
-   SciPy
-   GSTools
-   PyKrige
-   Rasterio
-   Shapely
-   Contextily

------------------------------------------------------------------------

# Productos generados

-   Estadísticos descriptivos
-   Histogramas
-   Gráficos Q-Q
-   Diagramas de caja (Boxplot)
-   Cartografía temática
-   Análisis geológico y estructural
-   Variogramas experimentales
-   Modelos variográficos
-   Validación cruzada
-   Mapas interpolados mediante Kriging Ordinario
-   Mapas de incertidumbre

------------------------------------------------------------------------

# Estado de actualización

**Versión actual:** v0.5

**Última actualización:** Julio de 2026

**Estado:** En desarrollo
