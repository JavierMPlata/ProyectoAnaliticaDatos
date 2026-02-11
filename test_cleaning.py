"""
Script de prueba para verificar la limpieza de datos
"""
from src.Extract.Extract import DataExtractor
from src.Transform.transform import DataClean
import os

def test_single_file():
    """Prueba la limpieza de un archivo individual"""
    file_path = 'src/Extract/Files/SINIESTROS.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return
    
    print("\n" + "="*60)
    print("PRUEBA DE LIMPIEZA - SINIESTROS.xlsx")
    print("="*60)
    
    # Extraer
    print("\n📂 Extrayendo datos...")
    extractor = DataExtractor(file_path)
    df = extractor.extract()
    
    # Análisis previo
    print("\n📊 ANÁLISIS PREVIO:")
    data_cleaner = DataClean(df)
    data_cleaner.print_null_analysis()
    
    # Limpiar
    print("\n🧹 LIMPIANDO DATOS...")
    cleaned_data = data_cleaner.clean_data()
    
    # Resumen
    print("\n📈 RESUMEN POST-LIMPIEZA:")
    summary = data_cleaner.get_cleaning_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n✅ PRUEBA COMPLETADA")
    print(f"   Dimensiones finales: {cleaned_data.shape}")
    print(f"   Valores nulos restantes: {cleaned_data.isnull().sum().sum()}")

if __name__ == "__main__":
    test_single_file()
