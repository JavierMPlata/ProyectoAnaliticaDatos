
import pandas as pd
import numpy as np
import os
from pathlib import Path
from src.Transform.transform import DataClean

class DataExtractor:
    def __init__(self, file_path: str = None):
        """
        Inicializa el extractor de datos.
        Args:
            file_path (str): Ruta al archivo a extraer (CSV o Excel)
        """
        self.file_path = file_path
        self.data = None
        self.file_type = None
        
        if file_path:
            self._detect_file_type()

    def _detect_file_type(self):
        """Detecta el tipo de archivo basándose en la extensión."""
        if self.file_path.endswith('.csv'):
            self.file_type = 'csv'
        elif self.file_path.endswith(('.xlsx', '.xls')):
            self.file_type = 'excel'
        else:
            raise ValueError(f"Tipo de archivo no soportado: {self.file_path}")

    def extract(self):
        """
        Extrae datos del archivo (CSV o Excel).
        Returns:
            pd.DataFrame: Datos extraídos
        """
        if self.file_type == 'csv':
            self.data = pd.read_csv(self.file_path)
        elif self.file_type == 'excel':
            self.data = pd.read_excel(self.file_path)
        else:
            raise ValueError("Debe especificar un archivo válido")
        
        print(f"✅ Archivo cargado: {os.path.basename(self.file_path)}")
        print(f"   Dimensiones: {self.data.shape[0]} filas x {self.data.shape[1]} columnas")
        return self.data

    def extract_multiple(self, files_directory: str, file_pattern: str = "*.xlsx"):
        """
        Extrae múltiples archivos de un directorio.
        Args:
            files_directory (str): Directorio con los archivos
            file_pattern (str): Patrón de archivos a buscar
        Returns:
            dict: Diccionario con {nombre_archivo: DataFrame}
        """
        files_path = Path(files_directory)
        files = list(files_path.glob(file_pattern))
        
        datasets = {}
        print(f"\n📂 Encontrados {len(files)} archivos en {files_directory}")
        
        for file in files:
            file_name = file.stem  # Nombre sin extensión
            try:
                if file.suffix == '.csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                datasets[file_name] = df
                print(f"   ✅ {file.name}: {df.shape[0]} filas x {df.shape[1]} columnas")
            except Exception as e:
                print(f"   ❌ Error al cargar {file.name}: {str(e)}")
        
        return datasets

    def response(self):
        """Retorna una vista previa de los datos."""
        if self.data is None:
            raise ValueError("Los datos no han sido cargados. Llama al método extract() primero.")
        return self.data.head(5)

    def extract_and_clean(self):
        """
        Extrae los datos del archivo y los limpia utilizando la clase DataClean.
        Returns:
            pd.DataFrame: Datos limpios
        """
        # Extraer los datos
        self.extract()

        # Limpiar los datos
        cleaner = DataClean(self.data)
        cleaner.clean_data()

        # Actualizar los datos con los datos limpios
        self.data = cleaner.get_cleaned_data()
        return self.data


# Mantener compatibilidad con código antiguo
class SpotifyExtractor(DataExtractor):
    def __init__(self, csv_path: str):
        super().__init__(csv_path)
    
    def queries(self):
        return self.extract()