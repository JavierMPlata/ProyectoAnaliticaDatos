# Documentación del Sistema de Limpieza de Datos

## 📋 Resumen de Procesamiento

Se procesaron exitosamente **5 datasets** de siniestros viales:

### Resultados por Dataset:

| Dataset | Filas | Columnas | Nulos Iniciales | Nulos Finales | Calidad |
|---------|-------|----------|----------------|---------------|---------|
| **SINIESTROS** | 196,152 | 10 | 217,705 (14.40% y 96.59% en 2 columnas) | 0 | 100% |
| **DICCIONARIO** | 211 | 4 | 0 | 0 | 100% |
| **ACTOR_VIAL** | 422,416 | 8 | 23,447 (5.55% en VEHICULO) | 0 | 100% |
| **HIPOTESIS** | 233,819 | 3 | 0 | 0 | 100% |
| **VEHICULOS** | 371,605 | 7 | 246,461 (0.77%, 4.22%, 61.33% en 3 columnas) | 0 | 100% |

**Total de registros procesados: 1,224,203 filas**  
**Valores nulos eliminados: 487,613**

## 🔧 Modificaciones Realizadas

### 1. **requirements.txt**
- ✅ Añadida dependencia `openpyxl>=3.1.0` para leer archivos Excel

### 2. **src/Extract/Extract.py**
- ✅ Nueva clase `DataExtractor` genérica para CSV y Excel
- ✅ Método `extract()` para archivos individuales
- ✅ Método `extract_multiple()` para procesar múltiples archivos
- ✅ Detección automática de tipo de archivo
- ✅ Mantenida compatibilidad con `SpotifyExtractor` (código legacy)

### 3. **src/Transform/transform.py**
- ✅ Ya contenía métodos robustos de limpieza genéricos
- ✅ `clean_data()`: Limpia columnas numéricas (mediana) y texto (moda)
- ✅ `remove_duplicates()`: Elimina registros duplicados
- ✅ `handle_missing_data()`: Estrategias automáticas para datos faltantes
- ✅ `remove_unwanted_values()`: Elimina outliers usando IQR
- ✅ `quality_assessment()`: Control de calidad completo

### 4. **main.py**
- ✅ Nueva función `clean_all_files()`: Procesa todos los archivos del directorio
- ✅ Nueva función `clean_single_file()`: Procesa un archivo específico
- ✅ Integración completa con Extract, Transform y Load
- ✅ Reportes detallados con emojis para mejor visualización
- ✅ Guardado automático en directorio `cleaned/`

## 🚀 Cómo Usar el Sistema

### Opción 1: Limpiar Todos los Archivos Excel

```python
python main.py
```

Esto procesará todos los archivos `.xlsx` en `src/Extract/Files/` y guardará los resultados en `src/Extract/Files/cleaned/`.

### Opción 2: Limpiar un Archivo Específico

Edita `main.py` y descomenta:

```python
cleaned_data = clean_single_file(
    file_path='src/Extract/Files/SINIESTROS.xlsx',
    output_dir='src/Extract/Files/cleaned'
)
```

### Opción 3: Uso Programático

```python
from src.Extract.Extract import DataExtractor
from src.Transform.transform import DataClean
from src.load.load import Loader

# Extraer
extractor = DataExtractor('src/Extract/Files/SINIESTROS.xlsx')
df = extractor.extract()

# Limpiar
cleaner = DataClean(df)
cleaned_df = cleaner.clean_data()

# Guardar
loader = Loader(cleaned_df)
loader.to_csv('output/SINIESTROS_cleaned.csv')
```

## 🧹 Estrategias de Limpieza Aplicadas

### Para Columnas Numéricas:
1. Conversión de valores no numéricos a NaN
2. Eliminación de caracteres especiales
3. **Relleno con la MEDIANA** de los valores válidos

### Para Columnas de Texto:
1. Eliminación de espacios extras
2. Estandarización de formatos
3. **Relleno con la MODA** (valor más frecuente)

### Limpieza Adicional Disponible:
- `remove_duplicates()`: Eliminar registros duplicados
- `remove_unwanted_values()`: Eliminar outliers
- `handle_missing_data(strategy='auto')`: Estrategias automáticas
- `comprehensive_clean()`: Limpieza completa con todos los pasos

## 📂 Estructura de Archivos Generados

```
src/Extract/Files/
├── ACTOR_VIAL.xlsx          # Original
├── DICCIONARIO.xlsx         # Original
├── HIPOTESIS.xlsx          # Original
├── SINIESTROS.xlsx         # Original
├── VEHICULOS.xlsx          # Original
└── cleaned/
    ├── ACTOR_VIAL_cleaned.csv     # Limpiado ✅
    ├── DICCIONARIO_cleaned.csv    # Limpiado ✅
    ├── HIPOTESIS_cleaned.csv      # Limpiado ✅
    ├── SINIESTROS_cleaned.csv     # Limpiado ✅
    └── VEHICULOS_cleaned.csv      # Limpiado ✅
```

## 📊 Análisis de Calidad

Todos los datasets alcanzaron **100% de calidad** después de la limpieza:

- ✅ **0 valores nulos** en todos los datasets
- ✅ **0 filas eliminadas** (preservación de datos)
- ✅ **0 columnas eliminadas**
- ✅ Todos los datos están listos para análisis

## 🔍 Detalles Técnicos

### Valores Nulos Eliminados por Dataset:

1. **SINIESTROS**: 217,705 nulos
   - CHOQUE: 28,242 (14.40%)
   - OBJETO_FIJO: 189,463 (96.59%)

2. **ACTOR_VIAL**: 23,447 nulos
   - VEHICULO: 23,447 (5.55%)

3. **VEHICULOS**: 246,461 nulos
   - CLASE: 2,854 (0.77%)
   - SERVICIO: 15,687 (4.22%)
   - MODALIDAD: 227,920 (61.33%)

4. **DICCIONARIO** y **HIPOTESIS**: Sin valores nulos

## 💡 Recomendaciones

1. **Validar** los datos limpios según tu dominio específico
2. **Revisar** las columnas con alto porcentaje de nulos (ej: OBJETO_FIJO 96.59%)
3. **Considerar** eliminar columnas con >90% de nulos si no son críticas
4. **Ejecutar** análisis estadísticos adicionales con los datos limpios
5. **Documentar** cualquier transformación específica del dominio

## 🎯 Próximos Pasos

1. ✅ Datos limpios y guardados en `cleaned/`
2. Realizar análisis exploratorio de datos (EDA)
3. Crear visualizaciones con `src/Visualization/visualization.py`
4. Entrenar modelos de machine learning si es necesario
5. Generar reportes y dashboards

---

**Fecha de procesamiento:** 11 de febrero de 2026  
**Total de registros procesados:** 1,224,203  
**Calidad final:** 100% en todos los datasets
