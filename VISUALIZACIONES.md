# 📊 Visualizaciones de Análisis de Siniestros Viales

## Descripción

Este módulo genera **10 visualizaciones analíticas profesionales** para el análisis exhaustivo de datos de siniestros viales. Las gráficas se crean automáticamente al ejecutar `main.py` y se guardan en el directorio `src/Visualization/Charts/`.

## 🎯 Visualizaciones Generadas

### 1. **Distribución por Gravedad** (`01_distribucion_gravedad.png`)
- **Tipo**: Gráfica de barras + Gráfica de pastel
- **Análisis**: Muestra la distribución de siniestros según su gravedad (Con Muertos, Con Heridos, Solo Daños)
- **Utilidad**: Identificar la proporción de incidentes graves vs. leves

### 2. **Evolución Temporal** (`02_evolucion_temporal.png`)
- **Tipo**: Gráfica de línea + Gráfica de barras
- **Análisis**: Evolución anual y distribución mensual de siniestros
- **Utilidad**: Detectar tendencias temporales y estacionalidad

### 3. **Tipos de Accidente** (`03_tipos_accidente.png`)
- **Tipo**: Gráfica de barras horizontales
- **Análisis**: Clasifica siniestros por tipo (Choque, Atropello, Volcamiento, etc.)
- **Utilidad**: Identificar los tipos de accidentes más frecuentes

### 4. **Distribución Horaria** (`04_distribucion_horaria.png`)
- **Tipo**: Gráfica de barras con código de colores
- **Análisis**: Distribución de siniestros por hora del día (0-23h)
- **Colores**:
  - 🌙 Madrugada (0-6h): Azul oscuro
  - 🌅 Mañana (6-12h): Rojo
  - ☀️ Tarde (12-18h): Naranja
  - 🌆 Noche (18-24h): Azul grisáceo
- **Utilidad**: Identificar las horas más peligrosas

### 5. **Top 10 Localidades** (`05_top_localidades.png`)
- **Tipo**: Gráfica de barras horizontales
- **Análisis**: Localidades con mayor número de siniestros
- **Utilidad**: Focalizar intervenciones en zonas críticas

### 6. **Perfil de Víctimas** (`06_perfil_victimas.png`)
- **Tipo**: Gráfica de pastel + Histograma
- **Análisis**: 
  - Distribución por sexo
  - Distribución por grupos de edad (0-17, 18-29, 30-44, 45-59, 60+)
- **Utilidad**: Diseñar campañas dirigidas a grupos de riesgo

### 7. **Vehículos Involucrados** (`07_vehiculos_involucrados.png`)
- **Tipo**: Gráfica de barras horizontales
- **Análisis**: Top 10 tipos de vehículos involucrados en siniestros
- **Utilidad**: Identificar vehículos de alto riesgo

### 8. **Heatmap Día-Hora** (`08_heatmap_dia_hora.png`)
- **Tipo**: Mapa de calor (heatmap)
- **Análisis**: Intensidad de siniestros por día de la semana y hora
- **Utilidad**: Visualizar patrones combinados temporales

### 9. **Causas Principales** (`09_causas_principales.png`)
- **Tipo**: Gráfica de barras horizontales
- **Análisis**: Top 10 causas de siniestros viales
- **Utilidad**: Priorizar medidas preventivas según causas más frecuentes

### 10. **Dashboard Resumen** (`10_dashboard_resumen.png`)
- **Tipo**: Panel de control con múltiples visualizaciones
- **Componentes**:
  - 📊 KPIs: Total siniestros, con muertos, con heridos
  - 📈 Evolución anual
  - 🥧 Top 5 tipos de accidente
  - ⏰ Distribución horaria
- **Utilidad**: Vista general ejecutiva del análisis

## 🚀 Cómo Ejecutar

```bash
# Ejecutar análisis completo (limpieza + visualizaciones)
python main.py
```

## 📦 Requisitos

Todas las dependencias están en `requirements.txt`:
- pandas >= 2.1.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- openpyxl >= 3.1.0

## 📁 Estructura de Archivos

```
ProyectoAnaliticaDatos/
├── main.py                          # Ejecuta limpieza + visualizaciones
├── src/
│   ├── Extract/
│   │   └── Files/
│   │       └── cleaned/             # CSV limpios (input visualizaciones)
│   └── Visualization/
│       ├── visualization_new.py     # Módulo de visualizaciones
│       └── Charts/                  # Gráficas generadas (output)
└── requirements.txt
```

## 🎨 Características de las Visualizaciones

✅ **Alta resolución**: 300 DPI para impresión profesional  
✅ **Etiquetas descriptivas**: Uso del diccionario de códigos  
✅ **Colores significativos**: Paletas adaptadas al contexto  
✅ **Formato estandarizado**: PNG con nombres ordenados  
✅ **Valores numéricos**: Anotaciones en las gráficas principales  

## 💡 Uso Profesional

Estas visualizaciones están diseñadas para:
- 📑 Reportes ejecutivos
- 🎓 Presentaciones académicas
- 🏛️ Informes gubernamentales
- 📊 Análisis de datos viales

## 📝 Notas

- Las gráficas se muestran automáticamente durante la ejecución (usar `plt.show()`)
- Si deseas solo guardar sin mostrar, modifica `visualization_new.py` comentando las líneas `plt.show()`
- El análisis se ejecuta secuencialmente, mostrando el progreso en consola
