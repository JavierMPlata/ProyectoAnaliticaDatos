import pandas as pd
import numpy as np
import re
from datetime import datetime

class DataClean:
	def __init__(self, data: pd.DataFrame):
		"""
		Inicializa la clase DataClean con un DataFrame.
		Args:
			data (pd.DataFrame): Los datos a limpiar
		"""
		self.data = data.copy()
		self.original_shape = data.shape
		self.null_info = {}
		self.duplicates_info = {}
		self.outliers_info = {}
		self.quality_report = {}

	def remove_duplicates(self, subset=None, keep='first'):
		"""
		Elimina registros duplicados del dataset.
		Args:
			subset (list): Columnas a considerar para identificar duplicados
			keep (str): Qué duplicado mantener ('first', 'last', False)
		Returns:
			dict: Información sobre duplicados removidos
		"""
		initial_rows = len(self.data)
		
		# Identificar duplicados
		duplicates_mask = self.data.duplicated(subset=subset, keep=False)
		duplicates_count = duplicates_mask.sum()
		
		# Remover duplicados
		self.data = self.data.drop_duplicates(subset=subset, keep=keep)
		
		final_rows = len(self.data)
		removed_rows = initial_rows - final_rows
		
		self.duplicates_info = {
			'initial_rows': initial_rows,
			'final_rows': final_rows,
			'duplicates_found': duplicates_count,
			'duplicates_removed': removed_rows,
			'percentage_removed': (removed_rows / initial_rows) * 100 if initial_rows > 0 else 0
		}
		
		return self.duplicates_info

	def handle_missing_data(self, strategy='drop', threshold=0.5):
		"""
		Maneja datos ausentes con diferentes estrategias.
		Args:
			strategy (str): 'drop' (eliminar), 'auto', 'fill', 'interpolate'
			threshold (float): Umbral para eliminar columnas (% de datos faltantes)
		Returns:
			pd.DataFrame: Datos procesados
		"""
		initial_rows = len(self.data)
		
		if strategy == 'drop':
			# Eliminar todas las filas con valores nulos
			self.data = self.data.dropna()
			removed_rows = initial_rows - len(self.data)
			print(f"   ✅ Filas eliminadas por valores nulos: {removed_rows}")
		
		elif strategy == 'auto':
			# Estrategia automática basada en el porcentaje de datos faltantes
			null_percentages = (self.data.isnull().sum() / len(self.data))
			
			# Eliminar columnas con más del umbral de datos faltantes
			cols_to_drop = null_percentages[null_percentages > threshold].index
			if len(cols_to_drop) > 0:
				self.data = self.data.drop(columns=cols_to_drop)
				print(f"   Columnas eliminadas por exceso de valores nulos: {list(cols_to_drop)}")
			
			# Eliminar filas con valores nulos restantes
			self.data = self.data.dropna()
			removed_rows = initial_rows - len(self.data)
			print(f"   ✅ Filas eliminadas por valores nulos: {removed_rows}")
		
		elif strategy == 'fill':
			# Rellenar con mediana/moda (método antiguo)
			numeric_columns = self.data.select_dtypes(include=[np.number]).columns
			for col in numeric_columns:
				if self.data[col].isna().any():
					self.data[col] = self.data[col].fillna(self.data[col].median())
			
			non_numeric_columns = self.data.select_dtypes(exclude=[np.number]).columns
			for col in non_numeric_columns:
				if self.data[col].isna().any():
					mode_val = self.data[col].mode()
					if len(mode_val) > 0:
						self.data[col] = self.data[col].fillna(mode_val[0])
		
		elif strategy == 'interpolate':
			numeric_columns = self.data.select_dtypes(include=[np.number]).columns
			for col in numeric_columns:
				self.data[col] = self.data[col].interpolate()
		
		return self.data

	def remove_unwanted_values(self, remove_outliers=True, clean_text=True, standardize_formats=True):
		"""
		Elimina valores no deseados del dataset.
		Args:
			remove_outliers (bool): Si eliminar outliers
			clean_text (bool): Si limpiar texto
			standardize_formats (bool): Si estandarizar formatos
		Returns:
			dict: Resumen de limpieza
		"""
		initial_rows = len(self.data)
		outliers_removed = 0
		
		# 1. Eliminar outliers usando IQR
		if remove_outliers:
			numeric_columns = self.data.select_dtypes(include=[np.number]).columns
			for col in numeric_columns:
				Q1 = self.data[col].quantile(0.25)
				Q3 = self.data[col].quantile(0.75)
				IQR = Q3 - Q1
				lower_bound = Q1 - 1.5 * IQR
				upper_bound = Q3 + 1.5 * IQR
				
				outliers_mask = (self.data[col] < lower_bound) | (self.data[col] > upper_bound)
				outliers_count = outliers_mask.sum()
				outliers_removed += outliers_count
				
				# Remover outliers
				self.data = self.data[~outliers_mask]
		
		# 2. Limpiar texto
		if clean_text:
			text_columns = self.data.select_dtypes(include=['object']).columns
			for col in text_columns:
				if self.data[col].dtype == 'object':
					# Eliminar espacios extra
					self.data[col] = self.data[col].astype(str).str.strip()
					# Reemplazar múltiples espacios con uno solo
					self.data[col] = self.data[col].str.replace(r'\s+', ' ', regex=True)
					# Eliminar caracteres especiales no deseados (opcional)
					self.data[col] = self.data[col].str.replace(r'[^\w\s\-\.\,]', '', regex=True)
		
		# 3. Estandarizar formatos
		if standardize_formats:
			text_columns = self.data.select_dtypes(include=['object']).columns
			for col in text_columns:
				if self.data[col].dtype == 'object':
					# Convertir a título (primera letra mayúscula)
					self.data[col] = self.data[col].str.title()
		
		final_rows = len(self.data)
		
		self.outliers_info = {
			'initial_rows': initial_rows,
			'final_rows': final_rows,
			'outliers_removed': outliers_removed,
			'total_removed': initial_rows - final_rows,
			'percentage_removed': ((initial_rows - final_rows) / initial_rows) * 100 if initial_rows > 0 else 0
		}
		
		return self.outliers_info

	def quality_assessment(self):
		"""
		Realiza un control de calidad (QA) completo para Big Data.
		Returns:
			dict: Reporte completo de calidad de datos
		"""
		current_shape = self.data.shape
		
		# 1. Métricas básicas
		basic_metrics = {
			'total_rows': current_shape[0],
			'total_columns': current_shape[1],
			'total_cells': current_shape[0] * current_shape[1],
			'memory_usage_mb': self.data.memory_usage(deep=True).sum() / 1024 / 1024
		}
		
		# 2. Análisis de completitud
		null_counts = self.data.isnull().sum()
		completeness = {
			'total_nulls': null_counts.sum(),
			'null_percentage': (null_counts.sum() / basic_metrics['total_cells']) * 100,
			'complete_rows': len(self.data.dropna()),
			'completeness_score': (basic_metrics['total_cells'] - null_counts.sum()) / basic_metrics['total_cells'] * 100
		}
		
		# 3. Análisis de unicidad
		uniqueness = {}
		for col in self.data.columns:
			unique_count = self.data[col].nunique()
			total_count = len(self.data[col].dropna())
			uniqueness[col] = {
				'unique_values': unique_count,
				'uniqueness_ratio': unique_count / total_count if total_count > 0 else 0
			}
		
		# 4. Análisis de tipos de datos
		data_types = {
			'numeric_columns': len(self.data.select_dtypes(include=[np.number]).columns),
			'text_columns': len(self.data.select_dtypes(include=['object']).columns),
			'datetime_columns': len(self.data.select_dtypes(include=['datetime']).columns),
			'boolean_columns': len(self.data.select_dtypes(include=['bool']).columns)
		}
		
		# 5. Análisis de valores atípicos
		outliers_analysis = {}
		numeric_columns = self.data.select_dtypes(include=[np.number]).columns
		for col in numeric_columns:
			Q1 = self.data[col].quantile(0.25)
			Q3 = self.data[col].quantile(0.75)
			IQR = Q3 - Q1
			lower_bound = Q1 - 1.5 * IQR
			upper_bound = Q3 + 1.5 * IQR
			outliers_count = ((self.data[col] < lower_bound) | (self.data[col] > upper_bound)).sum()
			outliers_analysis[col] = {
				'outliers_count': outliers_count,
				'outliers_percentage': (outliers_count / len(self.data)) * 100
			}
		
		# 6. Score general de calidad
		quality_score = (
			completeness['completeness_score'] * 0.4 +  # 40% completitud
			min(100, (1 - completeness['null_percentage']/100) * 100) * 0.3 +  # 30% ausencia de nulos
			min(100, (current_shape[0] / max(1, self.original_shape[0])) * 100) * 0.3  # 30% preservación de datos
		)
		
		self.quality_report = {
			'timestamp': datetime.now().isoformat(),
			'basic_metrics': basic_metrics,
			'completeness': completeness,
			'uniqueness': uniqueness,
			'data_types': data_types,
			'outliers_analysis': outliers_analysis,
			'overall_quality_score': quality_score,
			'recommendations': self._generate_recommendations(completeness, outliers_analysis)
		}
		
		return self.quality_report

	def _generate_recommendations(self, completeness, outliers_analysis):
		"""
		Genera recomendaciones basadas en el análisis de calidad.
		"""
		recommendations = []
		
		if completeness['null_percentage'] > 10:
			recommendations.append("Considerar estrategias adicionales para manejar valores nulos")
		
		if completeness['completeness_score'] < 80:
			recommendations.append("La completitud de los datos es baja, revisar fuentes de datos")
		
		high_outlier_cols = [col for col, info in outliers_analysis.items() 
						   if info['outliers_percentage'] > 5]
		if high_outlier_cols:
			recommendations.append(f"Revisar outliers en columnas: {', '.join(high_outlier_cols)}")
		
		if len(recommendations) == 0:
			recommendations.append("Los datos tienen buena calidad general")
		
		return recommendations

	def comprehensive_clean(self, remove_duplicates=True, handle_missing=True, 
						  remove_unwanted=True, run_qa=True):
		"""
		Ejecuta un proceso completo de limpieza de datos.
		Args:
			remove_duplicates (bool): Eliminar duplicados
			handle_missing (bool): Manejar datos faltantes
			remove_unwanted (bool): Eliminar valores no deseados
			run_qa (bool): Ejecutar control de calidad
		Returns:
			dict: Resumen completo del proceso
		"""
		print("=== INICIANDO LIMPIEZA COMPLETA DE DATOS ===")
		
		results = {
			'initial_shape': self.original_shape,
			'steps_performed': []
		}
		
		# Paso 1: Eliminar duplicados
		if remove_duplicates:
			print("1. Eliminando duplicados...")
			dup_info = self.remove_duplicates()
			results['duplicates'] = dup_info
			results['steps_performed'].append('remove_duplicates')
			print(f"   Duplicados eliminados: {dup_info['duplicates_removed']}")
		
		# Paso 2: Manejar datos faltantes
		if handle_missing:
			print("2. Manejando datos faltantes...")
			self.handle_missing_data(strategy='drop')
			results['steps_performed'].append('handle_missing_data')
		
		# Paso 3: Eliminar valores no deseados
		if remove_unwanted:
			print("3. Eliminando valores no deseados...")
			unwanted_info = self.remove_unwanted_values()
			results['unwanted_values'] = unwanted_info
			results['steps_performed'].append('remove_unwanted_values')
			print(f"   Outliers eliminados: {unwanted_info['outliers_removed']}")
		
		# Paso 4: Control de calidad
		if run_qa:
			print("4. Ejecutando control de calidad...")
			qa_report = self.quality_assessment()
			results['quality_assessment'] = qa_report
			results['steps_performed'].append('quality_assessment')
			print(f"   Score de calidad: {qa_report['overall_quality_score']:.2f}%")
		
		results['final_shape'] = self.data.shape
		results['total_rows_removed'] = self.original_shape[0] - self.data.shape[0]
		results['total_columns_removed'] = self.original_shape[1] - self.data.shape[1]
		
		print("=== LIMPIEZA COMPLETADA ===")
		print(f"Forma original: {results['initial_shape']}")
		print(f"Forma final: {results['final_shape']}")
		print(f"Filas eliminadas: {results['total_rows_removed']}")
		print(f"Columnas eliminadas: {results['total_columns_removed']}")
		
		return results

	def print_quality_report(self):
		"""
		Imprime un reporte detallado de calidad de datos.
		"""
		if not self.quality_report:
			self.quality_assessment()
		
		report = self.quality_report
		print("=== REPORTE DE CALIDAD DE DATOS ===")
		print(f"Timestamp: {report['timestamp']}")
		print(f"Score General de Calidad: {report['overall_quality_score']:.2f}%")
		
		print("\n--- MÉTRICAS BÁSICAS ---")
		basic = report['basic_metrics']
		print(f"Filas: {basic['total_rows']:,}")
		print(f"Columnas: {basic['total_columns']}")
		print(f"Uso de memoria: {basic['memory_usage_mb']:.2f} MB")
		
		print("\n--- COMPLETITUD ---")
		comp = report['completeness']
		print(f"Valores nulos: {comp['total_nulls']:,} ({comp['null_percentage']:.2f}%)")
		print(f"Filas completas: {comp['complete_rows']:,}")
		print(f"Score de completitud: {comp['completeness_score']:.2f}%")
		
		print("\n--- RECOMENDACIONES ---")
		for i, rec in enumerate(report['recommendations'], 1):
			print(f"{i}. {rec}")

	def analyze_null_values(self):
		"""
		Analiza los valores nulos en el dataset.
		Returns:
			dict: Información detallada sobre valores nulos
		"""
		null_counts = self.data.isnull().sum()
		null_percentages = (null_counts / len(self.data)) * 100
		self.null_info = {
			'total_rows': len(self.data),
			'total_columns': len(self.data.columns),
			'columns_with_nulls': null_counts[null_counts > 0].to_dict(),
			'null_percentages': null_percentages[null_percentages > 0].to_dict(),
			'total_null_values': null_counts.sum(),
			'columns_names': list(self.data.columns)
		}
		return self.null_info

	def clean_specific_numeric_columns(self):
		"""
		Limpia todas las columnas que deberían ser numéricas en el dataset actual, reemplazando valores no numéricos con la mediana.
		Returns:
			dict: Resumen del proceso de limpieza
		"""
		print("Limpiando columnas numéricas del dataset...")
		numeric_candidates = [
			'age', 'player_height', 'player_weight', 'draft_year', 'draft_round', 
			'draft_number', 'gp', 'pts', 'reb', 'ast', 'net_rating', 'oreb_pct', 
			'dreb_pct', 'usg_pct', 'ts_pct', 'ast_pct'
		]
		cleaning_summary = {
			'columns_processed': [],
			'columns_not_found': [],
			'total_conversions': 0,
			'total_filled': 0,
			'column_details': {}
		}
		for col in numeric_candidates:
			if col not in self.data.columns:
				cleaning_summary['columns_not_found'].append(col)
				continue
			initial_nulls = self.data[col].isna().sum()
			initial_dtype = str(self.data[col].dtype)
			if not pd.api.types.is_numeric_dtype(self.data[col]):
				self.data[col] = self.data[col].astype(str)
				self.data[col] = self.data[col].str.replace(',', '', regex=False)
				self.data[col] = self.data[col].str.replace(' ', '', regex=False)
				self.data[col] = self.data[col].replace(['nan', 'None', 'null', 'NULL', '', 'N/A', 'n/a', 'NaN'], np.nan)
				self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
			after_conversion_nulls = self.data[col].isna().sum()
			conversions = after_conversion_nulls - initial_nulls
			if conversions > 0:
				cleaning_summary['total_conversions'] += conversions
			valid_values = self.data[col].dropna()
			if len(valid_values) > 0:
				median_value = valid_values.median()
				filled_count = after_conversion_nulls
				self.data[col] = self.data[col].fillna(median_value)
				cleaning_summary['total_filled'] += filled_count
				final_nulls = self.data[col].isna().sum()
				final_dtype = str(self.data[col].dtype)
				final_min = self.data[col].min()
				final_max = self.data[col].max()
				column_detail = {
					'initial_nulls': initial_nulls,
					'conversions': conversions,
					'filled_count': filled_count,
					'final_nulls': final_nulls,
					'median_used': median_value,
					'final_range': f"{final_min:.2f} - {final_max:.2f}",
					'final_dtype': final_dtype
				}
				cleaning_summary['column_details'][col] = column_detail
				cleaning_summary['columns_processed'].append(col)
			else:
				cleaning_summary['columns_not_found'].append(col)
		return cleaning_summary
	
	def clean_data(self):
		"""
		Limpia los datos eliminando filas con valores nulos.
		Nuevo comportamiento: elimina directamente las filas con datos nulos.
		Returns:
			pd.DataFrame: Datos limpios
		"""
		print("🧹 Iniciando limpieza completa de datos...")
		
		initial_rows = len(self.data)
		initial_nulls = self.data.isnull().sum().sum()
		
		print(f"\n📊 Estado inicial:")
		print(f"   Total de filas: {initial_rows:,}")
		print(f"   Total de valores nulos: {initial_nulls:,}")
		
		# Mostrar columnas con valores nulos
		null_counts = self.data.isnull().sum()
		cols_with_nulls = null_counts[null_counts > 0]
		
		if len(cols_with_nulls) > 0:
			print(f"\n🔍 Columnas con valores nulos:")
			for col, count in cols_with_nulls.items():
				percentage = (count / initial_rows) * 100
				print(f"   - {col}: {count:,} nulos ({percentage:.2f}%)")
		
		# Eliminar filas con valores nulos
		print(f"\n🗑️  Eliminando filas con valores nulos...")
		self.data = self.data.dropna()
		
		final_rows = len(self.data)
		removed_rows = initial_rows - final_rows
		final_nulls = self.data.isnull().sum().sum()
		
		print(f"\n✅ Limpieza completada:")
		print(f"   Filas eliminadas: {removed_rows:,}")
		print(f"   Filas restantes: {final_rows:,}")
		print(f"   Valores nulos eliminados: {initial_nulls:,}")
		print(f"   Valores nulos restantes: {final_nulls:,}")
		if initial_rows > 0:
			print(f"   Porcentaje de datos preservados: {(final_rows/initial_rows)*100:.2f}%")
		
		print("\n🎯 Limpieza de datos completada exitosamente")
		return self.data
	
	def validate_specific_numeric_columns(self):
		"""
		Valida que las columnas numéricas principales estén correctamente convertidas a numéricas.
		Returns:
			dict: Resultado de la validación con detalles por columna
		"""
		print("Validando columnas numéricas principales...")
		target_columns = [
			'age', 'player_height', 'player_weight', 'draft_year', 'draft_round', 
			'draft_number', 'gp', 'pts', 'reb', 'ast', 'net_rating', 'oreb_pct', 
			'dreb_pct', 'usg_pct', 'ts_pct', 'ast_pct'
		]
		validation_results = {
			'valid_columns': [],
			'invalid_columns': [],
			'missing_columns': [],
			'column_details': {},
			'overall_status': True
		}
		for col in target_columns:
			if col not in self.data.columns:
				validation_results['missing_columns'].append(col)
				validation_results['overall_status'] = False
				continue
			is_numeric = pd.api.types.is_numeric_dtype(self.data[col])
			has_nulls = self.data[col].isna().any()
			null_count = self.data[col].isna().sum()
			has_infinite = False
			infinite_count = 0
			if is_numeric:
				has_infinite = np.isinf(self.data[col]).any()
				infinite_count = np.isinf(self.data[col]).sum()
			column_validation = {
				'is_numeric': is_numeric,
				'has_nulls': has_nulls,
				'null_count': null_count,
				'has_infinite': has_infinite,
				'infinite_count': infinite_count,
				'dtype': str(self.data[col].dtype),
				'is_valid': is_numeric and not has_nulls and not has_infinite
			}
			if is_numeric:
				column_validation.update({
					'min_value': float(self.data[col].min()),
					'max_value': float(self.data[col].max()),
					'median_value': float(self.data[col].median())
				})
			validation_results['column_details'][col] = column_validation
			if column_validation['is_valid']:
				validation_results['valid_columns'].append(col)
			else:
				validation_results['invalid_columns'].append(col)
				validation_results['overall_status'] = False
		return validation_results
	
	def get_numeric_columns_summary(self):
		"""
		Obtiene un resumen estadístico de las columnas numéricas principales del dataset actual.
		Returns:
			dict: Estadísticas detalladas por columna
		"""
		target_columns = [
			'age', 'player_height', 'player_weight', 'draft_year', 'draft_round', 
			'draft_number', 'gp', 'pts', 'reb', 'ast', 'net_rating', 'oreb_pct', 
			'dreb_pct', 'usg_pct', 'ts_pct', 'ast_pct'
		]
		summary = {
			'column_statistics': {},
			'overall_stats': {
				'total_target_columns': len(target_columns),
				'found_columns': 0,
				'numeric_columns': 0,
				'complete_columns': 0
			}
		}
		for col in target_columns:
			if col in self.data.columns:
				summary['overall_stats']['found_columns'] += 1
				if pd.api.types.is_numeric_dtype(self.data[col]):
					summary['overall_stats']['numeric_columns'] += 1
					col_stats = {
						'count': len(self.data[col]),
						'non_null_count': self.data[col].notna().sum(),
						'null_count': self.data[col].isna().sum(),
						'null_percentage': (self.data[col].isna().sum() / len(self.data[col])) * 100,
						'dtype': str(self.data[col].dtype),
						'min': float(self.data[col].min()),
						'max': float(self.data[col].max()),
						'median': float(self.data[col].median()),
						'mean': float(self.data[col].mean()),
						'std': float(self.data[col].std()),
						'unique_values': self.data[col].nunique()
					}
					if col_stats['null_count'] == 0:
						summary['overall_stats']['complete_columns'] += 1
					summary['column_statistics'][col] = col_stats
				else:
					summary['column_statistics'][col] = {
						'error': 'Columna no numérica',
						'dtype': str(self.data[col].dtype)
					}
			else:
				summary['column_statistics'][col] = {'error': 'Columna no encontrada'}
		return summary

	def get_cleaning_summary(self):
		"""
		Obtiene un resumen del proceso de limpieza.
		Returns:
			dict: Resumen del proceso de limpieza
		"""
		current_shape = self.data.shape
		summary = {
			'original_shape': self.original_shape,
			'current_shape': current_shape,
			'rows_removed': self.original_shape[0] - current_shape[0],
			'columns_removed': self.original_shape[1] - current_shape[1],
			'remaining_nulls': self.data.isnull().sum().sum(),
			'data_quality_score': ((self.data.notna().sum().sum()) / (current_shape[0] * current_shape[1])) * 100
		}
		return summary

	def get_cleaned_data(self):
		"""
		Retorna los datos limpios.
		Returns:
			pd.DataFrame: Datos después de la limpieza
		"""
		return self.data

	def print_null_analysis(self):
		"""
		Imprime un análisis detallado de los valores nulos.
		"""
		info = self.analyze_null_values()
		print("=== ANÁLISIS DE VALORES NULOS ===")
		print(f"Total de filas: {info['total_rows']}")
		print(f"Total de columnas: {info['total_columns']}")
		print(f"Total de valores nulos: {info['total_null_values']}")
		print("\nColumnas con valores nulos:")
		if info['columns_with_nulls']:
			for col, count in info['columns_with_nulls'].items():
				percentage = info['null_percentages'][col]
				print(f"  - {col}: {count} nulos ({percentage:.2f}%)")
		else:
			print("  ¡No se encontraron valores nulos!")
		print(f"\nColumnas disponibles: {', '.join(info['columns_names'])}")