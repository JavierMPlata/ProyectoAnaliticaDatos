from src.load.load import Loader
from src.Extract.Extract import DataExtractor
from src.Transform.transform import DataClean
import pandas as pd
import os

def clean_single_file(file_path: str, output_dir: str = None):
	"""
	Limpia un archivo individual.
	Args:
		file_path (str): Ruta al archivo
		output_dir (str): Directorio de salida (opcional)
	"""
	print(f"\n{'='*60}")
	print(f"PROCESANDO: {os.path.basename(file_path)}")
	print(f"{'='*60}")
	
	# Extraer datos
	extractor = DataExtractor(file_path)
	df = extractor.extract()
	
	# Análisis de nulos antes de limpiar
	print("\n📊 ANÁLISIS PREVIO A LIMPIEZA:")
	data_cleaner = DataClean(df)
	data_cleaner.print_null_analysis()
	
	# Limpiar datos
	print("\n🧹 INICIANDO LIMPIEZA...")
	cleaned_data = data_cleaner.clean_data()
	
	# Resumen post-limpieza
	summary = data_cleaner.get_cleaning_summary()
	print("\n📈 RESUMEN DE LIMPIEZA:")
	for key, value in summary.items():
		print(f"   {key}: {value}")
	
	# Mostrar vista previa
	print("\n👁️  VISTA PREVIA (5 primeros registros):")
	print(cleaned_data.head(5))
	
	# Guardar datos limpios
	if output_dir:
		loader = Loader(cleaned_data)
		file_name = os.path.splitext(os.path.basename(file_path))[0]
		output_path = os.path.join(output_dir, f"{file_name}_cleaned.csv")
		loader.to_csv(output_path)
		print(f"\n💾 Datos guardados en: {output_path}")
	
	return cleaned_data

def clean_all_files(files_directory: str, output_dir: str = None, file_pattern: str = "*.xlsx"):
	"""
	Limpia todos los archivos de un directorio.
	Args:
		files_directory (str): Directorio con los archivos
		output_dir (str): Directorio de salida
		file_pattern (str): Patrón de archivos a procesar
	"""
	print("\n" + "="*80)
	print("       SISTEMA DE LIMPIEZA DE DATOS - ETL ANALYTICS")
	print("="*80)
	
	# Extraer múltiples archivos
	extractor = DataExtractor()
	datasets = extractor.extract_multiple(files_directory, file_pattern)
	
	if not datasets:
		print("❌ No se encontraron archivos para procesar")
		return
	
	cleaned_datasets = {}
	
	for file_name, df in datasets.items():
		print(f"\n{'='*60}")
		print(f"PROCESANDO: {file_name}")
		print(f"{'='*60}")
		
		# Análisis previo
		print("\n📊 ANÁLISIS PREVIO:")
		data_cleaner = DataClean(df)
		data_cleaner.print_null_analysis()
		
		# Limpiar
		print("\n🧹 LIMPIANDO DATOS...")
		cleaned_data = data_cleaner.clean_data()
		
		# Resumen
		summary = data_cleaner.get_cleaning_summary()
		print("\n📈 RESUMEN:")
		for key, value in summary.items():
			print(f"   {key}: {value}")
		
		cleaned_datasets[file_name] = cleaned_data
		
		# Guardar
		if output_dir:
			os.makedirs(output_dir, exist_ok=True)
			loader = Loader(cleaned_data)
			output_path = os.path.join(output_dir, f"{file_name}_cleaned.csv")
			loader.to_csv(output_path)
			print(f"💾 Guardado: {output_path}")
	
	print("\n" + "="*80)
	print(f"✅ PROCESO COMPLETADO: {len(cleaned_datasets)} archivos procesados")
	print("="*80)
	
	return cleaned_datasets

def main():
	"""
	Función principal para ejecutar la limpieza de datos y generar visualizaciones.
	"""
	# Configuración
	files_directory = 'src/Extract/Files'
	output_directory = 'src/Extract/Files/cleaned'
	
	# Limpiar todos los archivos Excel del directorio
	cleaned_datasets = clean_all_files(
		files_directory=files_directory,
		output_dir=output_directory,
		file_pattern="*.xlsx"
	)
	
	# Si quieres procesar un archivo específico, descomenta:
	# cleaned_data = clean_single_file(
	#     file_path='src/Extract/Files/SINIESTROS.xlsx',
	#     output_dir='src/Extract/Files/cleaned'
	# )
	
	# Generar visualizaciones analíticas
	print("\n" + "="*80)
	print("🎨 INICIANDO GENERACIÓN DE VISUALIZACIONES ANALÍTICAS")
	print("="*80)
	
	# Importar aquí para evitar problemas de caché
	import importlib
	import sys
	# Limpiar caché si existe
	if 'src.Visualization.visualization_new' in sys.modules:
		importlib.reload(sys.modules['src.Visualization.visualization_new'])
	
	from src.Visualization.visualization_new import SiniestrosVialesAnalyzer
	analyzer = SiniestrosVialesAnalyzer(
		data_dir=output_directory,
		charts_dir='src/Visualization/Charts'
	)
	analyzer.generar_todas_graficas()

if __name__ == "__main__":
	main()