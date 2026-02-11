import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta al archivo CSV original
CSV_PATH = os.path.join(BASE_DIR, 'Extract', 'files', 'all_seasons.csv')

# Ruta para guardar datos limpios
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'Extract', 'Files', 'all_seasons_cleaned.csv')

# Puedes agregar más configuraciones aquí

class Config:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    INPUT_PATH = 'app/Extract/Files/all_seasons.csv'
    SQLITE_TABLE = 'all_seasons_clean'