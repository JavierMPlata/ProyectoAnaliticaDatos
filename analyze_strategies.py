"""
Script de análisis para comparar diferentes estrategias de limpieza de datos
"""

from src.Transform.transform import DataClean
from src.Extract.Extract import DataExtractor

def analyze_null_impact(file_path):
    """Analiza el impacto de diferentes estrategias de limpieza"""
    
    # Cargar datos
    print(f"\n📂 Cargando archivo: {file_path}")
    extractor = DataExtractor(file_path)
    df = extractor.extract()
    
    print("="*80)
    print("ANÁLISIS DE IMPACTO - ESTRATEGIAS DE LIMPIEZA")
    print("="*80)
    
    # Estado original
    print(f"\n📊 DATASET ORIGINAL:")
    print(f"   Filas: {len(df):,}")
    print(f"   Columnas: {len(df.columns)}")
    print(f"   Total de celdas: {len(df) * len(df.columns):,}")
    
    # Analizar nulos por columna
    null_analysis = df.isnull().sum()
    null_pct = (null_analysis / len(df)) * 100
    total_nulls = null_analysis.sum()
    
    print(f"\n🔍 ANÁLISIS POR COLUMNA:")
    print(f"   Total de valores nulos: {total_nulls:,}")
    print(f"   Porcentaje del dataset: {(total_nulls / (len(df) * len(df.columns))) * 100:.2f}%")
    print(f"\n   Desglose por columna:")
    
    for col in df.columns:
        nulls = null_analysis[col]
        pct = null_pct[col]
        if nulls > 0:
            status = "⚠️ CRÍTICO" if pct > 50 else "⚡ MODERADO" if pct > 10 else "✅ BAJO"
            print(f"   {status} {col}: {nulls:,} nulos ({pct:.2f}%)")
        else:
            print(f"   ✅ COMPLETO {col}: 0 nulos")
    
    # Estrategia 1: Eliminar todo
    print(f"\n{'='*80}")
    print(f"📝 ESTRATEGIA 1: Eliminar Filas con Nulos")
    print(f"{'='*80}")
    df1 = df.copy()
    cleaner1 = DataClean(df1)
    cleaned1 = cleaner1.clean_data()
    pct_kept1 = (len(cleaned1) / len(df)) * 100
    print(f"\n✅ RESULTADO:")
    print(f"   Filas: {len(cleaned1):,} de {len(df):,} ({pct_kept1:.2f}% preservado)")
    print(f"   Filas eliminadas: {len(df) - len(cleaned1):,}")
    print(f"   Columnas: {len(cleaned1.columns)} (sin cambio)")
    print(f"   Valores nulos: {cleaned1.isnull().sum().sum()}")
    
    # Estrategia 2: Auto (eliminar columnas >50%, luego filas)
    print(f"\n{'='*80}")
    print(f"📝 ESTRATEGIA 2: Auto (Eliminar columnas >50% nulos, luego filas)")
    print(f"{'='*80}")
    df2 = df.copy()
    cleaner2 = DataClean(df2)
    
    # Identificar columnas a eliminar
    cols_to_drop = null_pct[null_pct > 50].index.tolist()
    if cols_to_drop:
        print(f"\n🗑️  Columnas a eliminar (>50% nulos): {cols_to_drop}")
    else:
        print(f"\n✅ No hay columnas con >50% de nulos")
    
    cleaned2 = cleaner2.handle_missing_data(strategy='auto', threshold=0.5)
    pct_kept2 = (len(cleaned2) / len(df)) * 100
    print(f"\n✅ RESULTADO:")
    print(f"   Filas: {len(cleaned2):,} de {len(df):,} ({pct_kept2:.2f}% preservado)")
    print(f"   Filas eliminadas: {len(df) - len(cleaned2):,}")
    print(f"   Columnas: {len(cleaned2.columns)} de {len(df.columns)} ({len(df.columns) - len(cleaned2.columns)} eliminadas)")
    print(f"   Valores nulos: {cleaned2.isnull().sum().sum()}")
    
    # Estrategia 3: Rellenar
    print(f"\n{'='*80}")
    print(f"📝 ESTRATEGIA 3: Rellenar con Moda/Mediana")
    print(f"{'='*80}")
    df3 = df.copy()
    cleaner3 = DataClean(df3)
    cleaned3 = cleaner3.handle_missing_data(strategy='fill')
    pct_kept3 = (len(cleaned3) / len(df)) * 100
    print(f"\n✅ RESULTADO:")
    print(f"   Filas: {len(cleaned3):,} de {len(df):,} ({pct_kept3:.2f}% preservado)")
    print(f"   Filas eliminadas: {len(df) - len(cleaned3):,}")
    print(f"   Columnas: {len(cleaned3.columns)} (sin cambio)")
    print(f"   Valores nulos: {cleaned3.isnull().sum().sum()}")
    
    # Comparación y Recomendación
    print(f"\n{'='*80}")
    print(f"📊 COMPARACIÓN DE ESTRATEGIAS")
    print(f"{'='*80}")
    print(f"\n| Estrategia | Filas | % Preservado | Columnas | Nulos |")
    print(f"|------------|-------|--------------|----------|-------|")
    print(f"| Original   | {len(df):>5,} | 100.00%      | {len(df.columns):>8} | {total_nulls:>5,} |")
    print(f"| Eliminar   | {len(cleaned1):>5,} | {pct_kept1:>6.2f}%      | {len(cleaned1.columns):>8} | {cleaned1.isnull().sum().sum():>5} |")
    print(f"| Auto       | {len(cleaned2):>5,} | {pct_kept2:>6.2f}%      | {len(cleaned2.columns):>8} | {cleaned2.isnull().sum().sum():>5} |")
    print(f"| Rellenar   | {len(cleaned3):>5,} | {pct_kept3:>6.2f}%      | {len(cleaned3.columns):>8} | {cleaned3.isnull().sum().sum():>5} |")
    
    # Recomendación basada en resultados
    print(f"\n{'='*80}")
    print(f"💡 RECOMENDACIÓN")
    print(f"{'='*80}")
    
    if pct_kept1 < 20:
        print(f"\n⚠️  ALERTA: Eliminar nulos reduce el dataset a {pct_kept1:.1f}%")
        print(f"\n✅ RECOMENDACIONES:")
        print(f"   1. Usar Estrategia 2 (Auto) - Conserva {pct_kept2:.1f}% de datos")
        print(f"   2. Usar Estrategia 3 (Rellenar) - Conserva {pct_kept3:.1f}% de datos")
        print(f"   3. Eliminar manualmente las columnas con >50% de nulos")
        print(f"\n💭 CONSIDERACIÓN:")
        print(f"   La pérdida de {100-pct_kept1:.1f}% de los datos puede afectar")
        print(f"   significativamente la representatividad de tu análisis.")
    elif pct_kept1 < 50:
        print(f"\n⚡ PRECAUCIÓN: Eliminar nulos reduce el dataset a {pct_kept1:.1f}%")
        print(f"\n✅ RECOMENDACIONES:")
        print(f"   1. Evaluar si la pérdida de {100-pct_kept1:.1f}% es aceptable")
        print(f"   2. Considerar Estrategia 2 si necesitas más datos")
        print(f"   3. Analizar qué información se pierde con cada estrategia")
    else:
        print(f"\n✅ ÓPTIMO: Eliminar nulos es viable ({pct_kept1:.1f}% preservado)")
        print(f"\n✅ RECOMENDACIONES:")
        print(f"   Puedes usar la Estrategia 1 sin problemas significativos")
        print(f"   La pérdida de {100-pct_kept1:.1f}% es aceptable en la mayoría de casos")
    
    print(f"\n{'='*80}")
    
    return {
        'original_rows': len(df),
        'strategy_1_rows': len(cleaned1),
        'strategy_2_rows': len(cleaned2),
        'strategy_3_rows': len(cleaned3),
        'strategy_1_pct': pct_kept1,
        'strategy_2_pct': pct_kept2,
        'strategy_3_pct': pct_kept3,
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'src/Extract/Files/SINIESTROS.xlsx'
    
    print("\n🔍 ANÁLISIS DE ESTRATEGIAS DE LIMPIEZA DE DATOS")
    print(f"{'='*80}\n")
    
    try:
        results = analyze_null_impact(file_path)
        print("\n✅ Análisis completado exitosamente")
    except FileNotFoundError:
        print(f"\n❌ Error: Archivo no encontrado: {file_path}")
        print("\nUso:")
        print(f"   python {sys.argv[0]} <ruta_al_archivo>")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")
