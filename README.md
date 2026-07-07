# Análisis Geoespacial de la Distribución de Cobre en el Suroeste Antioqueño

## Autora
**Daniela Cardona Lopera**

Maestría en Ingeniería – Recursos Minerales  
Universidad Nacional de Colombia

---

# Descripción del proyecto

Este proyecto tiene como objetivo analizar la distribución espacial de las concentraciones de cobre (Cu) en el suroeste antioqueño mediante técnicas de análisis geoespacial y geoestadística.

La investigación parte de una base de datos geoquímica con aproximadamente **2.103 muestras puntuales**, cada una con coordenadas X, Y y concentración de cobre (Cu).

Además del conjunto de datos geoquímicos, el proyecto integra información geológica oficial del Servicio Geológico Colombiano (SGC):

- Geología regional
- Fallas geológicas
- Municipios
- Modelo Digital de Elevación (DEM) (pendiente)

---

# Planteamiento del problema

Aunque el cobre es una variable continua en el espacio, únicamente se dispone de mediciones puntuales distribuidas de manera heterogénea. Esto genera incertidumbre sobre el comportamiento de la concentración de cobre en zonas donde no existen muestras.

Se propone aplicar herramientas SIG y geoestadísticas para construir una superficie continua que permita interpretar la distribución espacial del cobre e identificar áreas de interés prospectivo.

---

# Objetivo General

Modelar la distribución espacial de la concentración de cobre mediante herramientas SIG y técnicas geoestadísticas para identificar zonas con potencial mineral y reducir la incertidumbre en áreas no muestreadas.

---

# Objetivos específicos

1. Caracterizar estadística y espacialmente la base de datos.
2. Analizar la distribución espacial de las muestras.
3. Integrar geología y fallas.
4. Generar modelos de interpolación (IDW y Kriging).
5. Validar los modelos.
6. Interpretar los resultados desde un enfoque geológico.

---

# Datos disponibles

## Base geoquímica

- ~2.103 muestras
- Coordenadas X
- Coordenadas Y
- Concentración de Cu

## Información cartográfica

- Geología (SGC)
- Fallas geológicas
- Municipios
- DEM (por incorporar)

---

# Software

- Google Colab
- Python
- QGIS
- GitHub

---

# Metodología

1. Importación y revisión de datos.
2. Análisis exploratorio.
3. Cartografía de puntos.
4. Integración con geología y fallas.
5. Variograma experimental.
6. Interpolación (IDW y Kriging).
7. Validación.
8. Elaboración de mapas finales e interpretación.

---

# Estructura del repositorio

```text
Proyecto_Cobre/
├── data/
├── scripts/
├── figures/
├── outputs/
├── qgis/
├── docs/
└── README.md
```

---

# Estado actual

- Base de datos revisada.
- Planteamiento del problema definido.
- Geología descargada.
- Fallas descargadas.
- Municipios descargados.
- Metodología definida.
- Organización inicial del repositorio establecida.

---

# Próximos pasos

- Crear el proyecto en QGIS.
- Importar la base de datos.
- Realizar el análisis exploratorio.
- Construir el primer mapa de distribución de muestras.
- Iniciar el análisis geoestadístico.

---

# Licencia

Proyecto académico desarrollado para el curso de **Análisis Geoespacial** de la Maestría en Ingeniería – Recursos Minerales.
