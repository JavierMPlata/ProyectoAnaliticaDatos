"""
Script de prueba para verificar que la limpieza elimina filas con valores nulos
"""

import pandas as pd
import numpy as np
from src.Transform.transform import DataClean

def test_remove_nulls():
    """
    Prueba que verifica que se eliminan las filas con valores nulos
    """
    print("=" * 80)
    print("PRUEBA: Eliminación de Filas con Valores Nulos")
    print("=" * 80)
    
    # Crear dataset de prueba con valores nulos
    data = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Nombre': ['Juan', 'María', None, 'Pedro', 'Ana', 'Luis', None, 'Carmen', 'José', 'Laura'],
        'Edad': [25, 30, 35, None, 45, 50, 55, 60, None, 70],
        'Salario': [3000, 3500, 4000, 4500, None, 5500, 6000, None, 7000, 7500],
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', None, 'Málaga', 'Murcia', 'Alicante', None]
    }
    
    df = pd.DataFrame(data)
    
    print("\n📋 DATASET ORIGINAL:")
    print(df)
    print(f"\nFilas totales: {len(df)}")
    print(f"Columnas totales: {len(df.columns)}")
    
    # Análisis de nulos
    print("\n📊 ANÁLISIS DE VALORES NULOS:")
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            print(f"   - {col}: {count} nulos ({percentage:.1f}%)")
    
    total_nulls = df.isnull().sum().sum()
    print(f"\n   Total de valores nulos: {total_nulls}")
    
    # Aplicar limpieza
    print("\n" + "=" * 80)
    cleaner = DataClean(df)
    cleaned_df = cleaner.clean_data()
    
    # Mostrar resultados
    print("\n📋 DATASET LIMPIO:")
    print(cleaned_df)
    print(f"\nFilas totales: {len(cleaned_df)}")
    print(f"Columnas totales: {len(cleaned_df.columns)}")
    
    # Verificar que no quedan nulos
    remaining_nulls = cleaned_df.isnull().sum().sum()
    print(f"\n✅ Valores nulos restantes: {remaining_nulls}")
    
    # Resumen
    summary = cleaner.get_cleaning_summary()
    print("\n" + "=" * 80)
    print("📈 RESUMEN DEL PROCESO:")
    print(f"   Forma original: {summary['original_shape']}")
    print(f"   Forma final: {summary['current_shape']}")
    print(f"   Filas eliminadas: {summary['rows_removed']}")
    print(f"   Columnas eliminadas: {summary['columns_removed']}")
    print(f"   Valores nulos restantes: {summary['remaining_nulls']}")
    print(f"   Score de calidad de datos: {summary['data_quality_score']:.2f}%")
    print("=" * 80)
    
    # Verificación
    assert remaining_nulls == 0, "ERROR: Aún quedan valores nulos después de la limpieza"
    print("\n✅ PRUEBA EXITOSA: Todos los valores nulos fueron eliminados correctamente")
    
    return cleaned_df

if __name__ == "__main__":
    test_remove_nulls()
