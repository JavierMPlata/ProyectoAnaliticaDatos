# 📊 Proyecto Analítica de Datos - Siniestros Viales

Sistema ETL (Extract, Transform, Load) para el análisis y limpieza de datos de siniestros viales en Colombia.

## 🎯 Descripción

Este proyecto implementa un pipeline completo de procesamiento de datos que:
- ✅ Extrae datos de múltiples archivos Excel (.xlsx)
- ✅ Limpia y transforma datos usando estrategias estadísticas robustas
- ✅ Carga los datos limpios en CSV y SQLite
- ✅ Genera reportes de calidad de datos detallados

## 📁 Estructura del Proyecto

```
ProyectoAnaliticaDatos/
├── main.py                      # Script principal de ejecución
├── test_cleaning.py             # Script de pruebas
├── requirements.txt             # Dependencias del proyecto
├── LIMPIEZA_DATOS.md           # Documentación detallada de limpieza
├── README.md                    # Este archivo
└── src/
    ├── Extract/
    │   ├── Extract.py          # Módulo de extracción de datos
    │   └── Files/               # Datasets originales y limpios
    │       ├── *.xlsx          # Archivos originales
    │       └── cleaned/        # Archivos limpios (CSV)
    ├── Transform/
    │   └── transform.py        # Módulo de transformación y limpieza
    ├── load/
    │   └── load.py             # Módulo de carga de datos
    ├── Visualization/
    │   └── visualization.py    # Módulo de visualización
    └── config/
        └── config.py           # Configuraciones
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JavierMPlata/ProyectoAnaliticaDatos.git
cd ProyectoAnaliticaDatos
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📝 Uso

### Limpiar Todos los Datasets

```bash
python main.py
```

Esto procesará todos los archivos `.xlsx` en `src/Extract/Files/` y guardará los resultados en `src/Extract/Files/cleaned/`.

### Uso Programático

```python
from src.Extract.Extract import DataExtractor
from src.Transform.transform import DataClean

# Extraer datos
extractor = DataExtractor('src/Extract/Files/SINIESTROS.xlsx')
df = extractor.extract()

# Limpiar datos
cleaner = DataClean(df)
cleaned_df = cleaner.clean_data()

# Ver resumen
summary = cleaner.get_cleaning_summary()
print(summary)
```

## 📊 Datasets Procesados

| Dataset | Registros | Columnas | Descripción |
|---------|-----------|----------|-------------|
| SINIESTROS | 196,152 | 10 | Información de siniestros viales |
| ACTOR_VIAL | 422,416 | 8 | Datos de actores involucrados |
| VEHICULOS | 371,605 | 7 | Información de vehículos |
| HIPOTESIS | 233,819 | 3 | Hipótesis de causas |
| DICCIONARIO | 211 | 4 | Diccionario de códigos |

**Total: 1,224,203 registros procesados**

## 🧹 Características de Limpieza

### Estrategias Disponibles

El sistema ahora ofrece **múltiples estrategias** para manejar valores nulos:

#### 1. **Eliminar Filas con Nulos** (Por defecto) 🆕
```python
cleaner.clean_data()  # O usar handle_missing_data(strategy='drop')
```
- ✅ Elimina directamente todas las filas con valores nulos
- ✅ Datos 100% completos y confiables
- ⚠️ Puede reducir significativamente el dataset

#### 2. **Auto (Inteligente)**
```python
cleaner.handle_missing_data(strategy='auto', threshold=0.5)
```
- Elimina columnas con >50% de nulos
- Luego elimina filas con nulos restantes
- Balancea preservación y calidad de datos

#### 3. **Rellenar con Mediana/Moda**
```python
cleaner.handle_missing_data(strategy='fill')
```
- Rellena columnas numéricas con la mediana
- Rellena columnas de texto con la moda
- Preserva 100% de las filas

#### 4. **Interpolación**
```python
cleaner.handle_missing_data(strategy='interpolate')
```
- Interpola valores en columnas numéricas
- Útil para series temporales

### Herramienta de Análisis 🔍

Usa el script de análisis para comparar estrategias:

```bash
python analyze_strategies.py
```

Esto te mostrará:
- Impacto de cada estrategia en tu dataset
- Porcentaje de datos preservados
- Recomendaciones personalizadas

### Otras Características

- **Eliminación de duplicados**: Identificación y remoción de registros duplicados
- **Detección de outliers**: Usando método IQR (Interquartile Range)
- **Estandarización**: Normalización de formatos y tipos de datos
- **Reportes de calidad**: Análisis completo de calidad de datos

## 📈 Resultados

## 📈 Resultados

El sistema puede alcanzar **100% de calidad** después de la limpieza (dependiendo de la estrategia):

**Con Estrategia "Eliminar Nulos":**
- ✅ **0 valores nulos**
- ✅ Datos 100% confiables
- ⚠️ Varía el % de filas preservadas según el dataset

**Ejemplo - Dataset SINIESTROS:**
- Estrategia 1 (Eliminar): 6,689 filas (3.41% preservado)
- Estrategia 2 (Auto): 167,910 filas (85.60% preservado) ✅ **Recomendada**
- Estrategia 3 (Rellenar): 196,152 filas (100% preservado)

📊 **Recomendación:** Usa `analyze_strategies.py` para elegir la mejor estrategia para tu dataset.

Ver [LIMPIEZA_DATOS.md](LIMPIEZA_DATOS.md) y [ACTUALIZACION_LIMPIEZA.md](ACTUALIZACION_LIMPIEZA.md) para más detalles.

## 🧪 Scripts de Prueba

| Script | Descripción |
|--------|-------------|
| `test_cleaning.py` | Prueba con archivos reales (SINIESTROS.xlsx) |
| `test_remove_nulls.py` | Demuestra eliminación de nulos con datos sintéticos |
| `analyze_strategies.py` | Compara las 3 estrategias de limpieza |

## 🛠️ Tecnologías

- **Python 3.x**
- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas
- **openpyxl**: Lectura de archivos Excel
- **matplotlib/seaborn**: Visualización
- **SQLite**: Almacenamiento de datos

## 📚 Documentación Adicional

- **[LIMPIEZA_DATOS.md](LIMPIEZA_DATOS.md)** - Documentación original del proceso de limpieza
- **[ACTUALIZACION_LIMPIEZA.md](ACTUALIZACION_LIMPIEZA.md)** - Nueva funcionalidad de eliminación de nulos 🆕
- **[RECOMENDACIONES_LIMPIEZA.md](RECOMENDACIONES_LIMPIEZA.md)** - Guía de estrategias y cuándo usarlas 🆕
- **[LICENSE](LICENSE)** - Licencia del proyecto

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👤 Autor

**Javier M. Plata**
- GitHub: [@JavierMPlata](https://github.com/JavierMPlata)

## 📄 Licencia

Este proyecto está bajo la licencia especificada en [LICENSE](LICENSE).

---

**Última actualización:** Febrero 2026 (Feature1 - Limpieza por eliminación de nulos)  
**Estado:** ✅ Funcional - Múltiples estrategias de limpieza disponibles  
**Versión:** 2.0