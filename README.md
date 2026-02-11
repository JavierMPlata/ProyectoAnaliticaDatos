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

- **Manejo de valores nulos**: Relleno con mediana (numéricos) y moda (texto)
- **Eliminación de duplicados**: Identificación y remoción de registros duplicados
- **Detección de outliers**: Usando método IQR (Interquartile Range)
- **Estandarización**: Normalización de formatos y tipos de datos
- **Reportes de calidad**: Análisis completo de calidad de datos

## 📈 Resultados

Todos los datasets alcanzaron **100% de calidad** después de la limpieza:
- ✅ **0 valores nulos**
- ✅ **487,613 valores nulos corregidos**
- ✅ Preservación del 100% de registros
- ✅ Datos listos para análisis

Ver [LIMPIEZA_DATOS.md](LIMPIEZA_DATOS.md) para más detalles.

## 🛠️ Tecnologías

- **Python 3.x**
- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas
- **openpyxl**: Lectura de archivos Excel
- **matplotlib/seaborn**: Visualización
- **SQLite**: Almacenamiento de datos

## 📚 Documentación Adicional

- [LIMPIEZA_DATOS.md](LIMPIEZA_DATOS.md) - Documentación completa del proceso de limpieza
- [LICENSE](LICENSE) - Licencia del proyecto

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

**Última actualización:** Febrero 2026  
**Estado:** ✅ Funcional - Limpieza de datos completada