# Análisis de Resultados - Eliminación de Nulos

## ⚠️ Advertencia Importante

Los datos del archivo **SINIESTROS.xlsx** demuestran un caso donde la eliminación directa de nulos puede no ser la mejor estrategia:

### Resultados del Dataset SINIESTROS

```
📊 Dataset Original:
   - Filas: 196,152
   - Columnas: 10
   - Valores nulos: 217,705

❌ Columnas Problemáticas:
   - CHOQUE: 28,242 nulos (14.40%)
   - OBJETO_FIJO: 189,463 nulos (96.59%)  ⚠️ CRÍTICO

✂️ Después de Eliminar Nulos:
   - Filas restantes: 6,689 (3.41% preservado)
   - Filas eliminadas: 189,463 (96.59% perdido)
   - Calidad: 100% (sin nulos)
```

## 🤔 ¿Es Este el Mejor Enfoque?

### ❌ Problemas con Eliminación Directa
- Se pierde el **96.59%** de los datos
- Solo quedan 6,689 de 196,152 registros originales
- Puede no ser representativo del dataset completo

### ✅ Estrategias Alternativas Recomendadas

#### Opción 1: Eliminar Columnas Problemáticas

```python
from src.Transform.transform import DataClean

# Eliminar columnas con >50% de nulos, luego eliminar filas
cleaner = DataClean(df)
cleaner.handle_missing_data(strategy='auto', threshold=0.5)
```

**Resultado esperado:**
- Eliminaría la columna OBJETO_FIJO (96.59% nulos)
- Mantendría más filas en el dataset
- Luego eliminaría solo las filas con nulos en CHOQUE

#### Opción 2: Análisis por Columna

```python
from src.Transform.transform import DataClean
import pandas as pd

# Analizar qué columnas son realmente importantes
cleaner = DataClean(df)

# Opción A: Eliminar columnas específicas manualmente
df_reduced = df.drop(columns=['OBJETO_FIJO'])  # 96% nulos
cleaner_reduced = DataClean(df_reduced)
cleaned = cleaner_reduced.clean_data()

# Opción B: Mantener columnas nulas y eliminar solo filas críticas
# (no eliminar si solo falta un dato no crítico)
```

#### Opción 3: Rellenar Estratégicamente

```python
from src.Transform.transform import DataClean

# Rellenar columnas no críticas
df['OBJETO_FIJO'] = df['OBJETO_FIJO'].fillna('NO_APLICA')
df['CHOQUE'] = df['CHOQUE'].fillna('DESCONOCIDO')

# Luego limpiar
cleaner = DataClean(df)
cleaned = cleaner.clean_data()
```

#### Opción 4: Imputación Inteligente

```python
from src.Transform.transform import DataClean

# Usar estrategia 'fill' para columnas categóricas
cleaner = DataClean(df)
cleaned = cleaner.handle_missing_data(strategy='fill')
```

## 📋 Script de Análisis Completo

Creamos un script para ayudarte a decidir la mejor estrategia:

```python
from src.Transform.transform import DataClean
from src.Extract.Extract import DataExtractor

def analyze_null_impact(file_path):
    """Analiza el impacto de diferentes estrategias de limpieza"""
    
    # Cargar datos
    extractor = DataExtractor(file_path)
    df = extractor.extract()
    
    print("="*80)
    print("ANÁLISIS DE IMPACTO - ESTRATEGIAS DE LIMPIEZA")
    print("="*80)
    
    # Estado original
    print(f"\n📊 DATASET ORIGINAL:")
    print(f"   Filas: {len(df):,}")
    print(f"   Columnas: {len(df.columns)}")
    
    # Analizar nulos por columna
    null_analysis = df.isnull().sum()
    null_pct = (null_analysis / len(df)) * 100
    
    print(f"\n🔍 ANÁLISIS POR COLUMNA:")
    for col, nulls in null_analysis[null_analysis > 0].items():
        pct = null_pct[col]
        status = "⚠️ CRÍTICO" if pct > 50 else "⚡ MODERADO" if pct > 10 else "✅ BAJO"
        print(f"   {status} {col}: {nulls:,} nulos ({pct:.2f}%)")
    
    # Estrategia 1: Eliminar todo
    print(f"\n📝 ESTRATEGIA 1: Eliminar Filas con Nulos")
    df1 = df.copy()
    cleaner1 = DataClean(df1)
    cleaned1 = cleaner1.clean_data()
    pct_kept1 = (len(cleaned1) / len(df)) * 100
    print(f"   Resultado: {len(cleaned1):,} filas ({pct_kept1:.2f}% preservado)")
    
    # Estrategia 2: Auto (eliminar columnas >50%, luego filas)
    print(f"\n📝 ESTRATEGIA 2: Auto (Eliminar columnas >50% nulos)")
    df2 = df.copy()
    cleaner2 = DataClean(df2)
    cleaned2 = cleaner2.handle_missing_data(strategy='auto', threshold=0.5)
    pct_kept2 = (len(cleaned2) / len(df)) * 100
    print(f"   Resultado: {len(cleaned2):,} filas ({pct_kept2:.2f}% preservado)")
    print(f"   Columnas: {len(cleaned2.columns)} de {len(df.columns)}")
    
    # Estrategia 3: Rellenar
    print(f"\n📝 ESTRATEGIA 3: Rellenar con Moda/Mediana")
    df3 = df.copy()
    cleaner3 = DataClean(df3)
    cleaned3 = cleaner3.handle_missing_data(strategy='fill')
    pct_kept3 = (len(cleaned3) / len(df)) * 100
    print(f"   Resultado: {len(cleaned3):,} filas ({pct_kept3:.2f}% preservado)")
    
    # Recomendación
    print(f"\n💡 RECOMENDACIÓN:")
    if pct_kept1 < 20:
        print(f"   ⚠️  Eliminar nulos reduce el dataset a {pct_kept1:.1f}%")
        print(f"   ✅ Considerar Estrategia 2 (auto) o Estrategia 3 (fill)")
        print(f"   ✅ O eliminar manualmente las columnas problemáticas")
    elif pct_kept1 < 50:
        print(f"   ⚡ Eliminar nulos reduce el dataset a {pct_kept1:.1f}%")
        print(f"   ⚠️  Evaluar si la pérdida es aceptable para tu análisis")
    else:
        print(f"   ✅ Eliminar nulos es viable ({pct_kept1:.1f}% preservado)")
    
    return {
        'strategy_1_rows': len(cleaned1),
        'strategy_2_rows': len(cleaned2),
        'strategy_3_rows': len(cleaned3),
    }

if __name__ == "__main__":
    analyze_null_impact('src/Extract/Files/SINIESTROS.xlsx')
```

## 🎯 Recomendación Final

Para el dataset **SINIESTROS**:

```python
from src.Transform.transform import DataClean
from src.Extract.Extract import DataExtractor

# Cargar datos
extractor = DataExtractor('src/Extract/Files/SINIESTROS.xlsx')
df = extractor.extract()

# OPCIÓN RECOMENDADA: Eliminar columna problemática primero
df_clean = df.drop(columns=['OBJETO_FIJO'])  # 96% nulos, no es útil

# Ahora limpiar el resto
cleaner = DataClean(df_clean)
cleaned_data = cleaner.clean_data()

print(f"Filas finales: {len(cleaned_data):,}")
print(f"Columnas finales: {len(cleaned_data.columns)}")
```

**Resultado esperado:**
- Conservará muchas más filas
- Solo eliminará filas con nulos en columnas realmente importantes
- Datos más representativos del conjunto original

## 📊 Cuándo Usar Cada Estrategia

| Estrategia | Usar Cuando | Ventajas | Desventajas |
|------------|-------------|----------|-------------|
| **Eliminar Filas** | Nulos < 20% | 100% confiable | Pérdida de datos |
| **Auto (eliminar cols+filas)** | Columnas problemáticas | Balancea pérdida | Pierde información |
| **Rellenar** | Cada fila es valiosa | Conserva datos | Introduce artificialidad |
| **Eliminar Columnas Manual** | Sabes qué columnas importan | Control total | Requiere análisis |

---

**Conclusión:** La estrategia correcta depende de tu objetivo de análisis y cuánta pérdida de datos puedes tolerar.
