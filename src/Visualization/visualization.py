import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SiniestrosViales:
    """
    Clase para crear visualizaciones analíticas de datos de siniestros viales.
    """
    
    def __init__(self, data_dir='src/Extract/Files/cleaned', charts_dir='src/Visualization/Charts'):
        """
        Inicializa el visualizador.
        
        Args:
            data_dir (str): Directorio con los archivos CSV limpios
            charts_dir (str): Directorio donde guardar las gráficas
        """
        self.data_dir = data_dir
        self.charts_dir = charts_dir
        self.siniestros = None
        self.vehiculos = None
        self.actores = None
        self.hipotesis = None
        self.diccionario = None
        
        # Crear directorio de gráficas si no existe
        Path(self.charts_dir).mkdir(parents=True, exist_ok=True)
        
        # Configurar estilo
        plt.style.use('default')
        sns.set_palette("husl")
        sns.set_context("notebook", font_scale=1.1)
        
    def load_data(self):
        """Carga todos los archivos CSV necesarios."""
        try:
            print("📊 Cargando datos...")
            self.siniestros = pd.read_csv(f'{self.data_dir}/SINIESTROS_cleaned.csv')
            self.vehiculos = pd.read_csv(f'{self.data_dir}/VEHICULOS_cleaned.csv')
            self.actores = pd.read_csv(f'{self.data_dir}/ACTOR_VIAL_cleaned.csv')
            self.hipotesis = pd.read_csv(f'{self.data_dir}/HIPOTESIS_cleaned.csv')
            self.diccionario = pd.read_csv(f'{self.data_dir}/DICCIONARIO_cleaned.csv')
            
            # Convertir fecha a datetime
            self.siniestros['FECHA'] = pd.to_datetime(self.siniestros['FECHA'], format='%d/%m/%Y', errors='coerce')
            self.actores['FECHA'] = pd.to_datetime(self.actores['FECHA'], format='%d/%m/%Y', errors='coerce')
            
            # Extraer componentes de fecha
            self.siniestros['AÑO'] = self.siniestros['FECHA'].dt.year
            self.siniestros['MES'] = self.siniestros['FECHA'].dt.month
            self.siniestros['DIA_SEMANA'] = self.siniestros['FECHA'].dt.dayofweek
            
            # Extraer hora del día
            if 'HORA' in self.siniestros.columns:
                self.siniestros['HORA_NUM'] = pd.to_datetime(self.siniestros['HORA'], format='%H:%M:%S', errors='coerce').dt.hour
            
            print(f"✅ Datos cargados: {len(self.siniestros)} siniestros, {len(self.actores)} actores viales")
            return True
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return False
    
    def get_descripcion(self, hoja, campo, codigo):
        """Obtiene la descripción de un código del diccionario."""
        try:
            desc = self.diccionario[
                (self.diccionario['HOJA'] == hoja) & 
                (self.diccionario['CAMPO'] == campo) & 
                (self.diccionario['CODIGO'] == int(codigo))
            ]['DESCRIPCION'].values
            return desc[0] if len(desc) > 0 else f'Código {codigo}'
        except:
            return f'Código {codigo}'
    
    def prepare_season_data(self):
        """Prepara los datos agregados por temporada."""
        if self.data is None:
            print("Primero debes cargar los datos")
            return None
            
        # Agregar datos por temporada
        season_stats = self.data.groupby('season').agg({
            'pts': ['mean', 'sum', 'count'],
            'reb': 'mean',
            'ast': 'mean',
            'gp': 'mean',
            'net_rating': 'mean'
        }).round(2)
        
        # Aplanar nombres de columnas
        season_stats.columns = ['_'.join(col).strip() for col in season_stats.columns]
        season_stats = season_stats.reset_index()
        
        # Extraer año para facilitar análisis temporal
        season_stats['year'] = season_stats['season'].str[:4].astype(int)
        
        # Crear décadas
        season_stats['decade'] = (season_stats['year'] // 10) * 10
        season_stats['decade_label'] = season_stats['decade'].astype(str) + 's'
        
        return season_stats
    
    def create_temporal_points_evolution(self):
        """
        Crea gráfica de evolución temporal de puntos por temporada.
        """
        if self.data is None:
            if not self.load_data():
                return
        
        season_stats = self.prepare_season_data()
        
        plt.figure(figsize=(15, 8))
        
        # Gráfica de línea para evolución temporal
        sns.lineplot(data=season_stats, x='year', y='pts_mean', 
                    marker='o', linewidth=2.5, markersize=8)
        
        plt.title('Evolución Temporal de Puntos Promedio por Temporada NBA', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Año', fontsize=12, fontweight='bold')
        plt.ylabel('Puntos Promedio por Jugador', fontsize=12, fontweight='bold')
        
        # Añadir línea de tendencia
        z = np.polyfit(season_stats['year'], season_stats['pts_mean'], 1)
        p = np.poly1d(z)
        plt.plot(season_stats['year'], p(season_stats['year']), 
                "r--", alpha=0.8, linewidth=2, label='Tendencia')
        
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Guardar gráfica
        output_path = os.path.join(self.charts_dir, 'evolucion_temporal_puntos.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Gráfica guardada en: {output_path}")
    
    def create_stacked_wins_losses_chart(self):
        """
        Crea gráfica de barras apiladas: Victorias, Empates y Derrotas por Temporada.
        Nota: Como los datos son de jugadores individuales, simularemos estadísticas de equipo
        basadas en net_rating y rendimiento del jugador.
        """
        if self.data is None:
            if not self.load_data():
                return
        
        # Simular categorías de rendimiento basadas en net_rating y estadísticas
        def categorize_performance(row):
            if row['net_rating'] > 5 and row['pts'] > 10:
                return 'Alto Rendimiento'
            elif row['net_rating'] > 0 or row['pts'] > 8:
                return 'Rendimiento Medio'
            else:
                return 'Bajo Rendimiento'
        
        self.data['performance_category'] = self.data.apply(categorize_performance, axis=1)
        
        # Crear tabla cruzada para barras apiladas
        performance_by_season = pd.crosstab(self.data['season'], 
                                          self.data['performance_category'])
        
        # Convertir a porcentajes para mejor visualización
        performance_pct = performance_by_season.div(performance_by_season.sum(axis=1), axis=0) * 100
        
        plt.figure(figsize=(16, 8))
        
        # Crear gráfica de barras apiladas
        performance_pct.plot(kind='bar', stacked=True, 
                           color=['#d62728', '#ff7f0e', '#2ca02c'],
                           figsize=(16, 8))
        
        plt.title('Distribución de Rendimiento de Jugadores por Temporada NBA', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Temporada', fontsize=12, fontweight='bold')
        plt.ylabel('Porcentaje de Jugadores (%)', fontsize=12, fontweight='bold')
        plt.legend(title='Categoría de Rendimiento', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Guardar gráfica
        output_path = os.path.join(self.charts_dir, 'barras_apiladas_rendimiento.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Gráfica guardada en: {output_path}")
    
    def create_points_distribution_boxplot(self):
        """
        Crea box plot: Distribución de Puntos por Décadas/Períodos.
        """
        if self.data is None:
            if not self.load_data():
                return
        
        # Añadir década a los datos originales
        self.data['year'] = self.data['season'].str[:4].astype(int)
        self.data['decade'] = (self.data['year'] // 10) * 10
        self.data['decade_label'] = self.data['decade'].astype(str) + 's'
        
        plt.figure(figsize=(14, 8))
        
        # Crear box plot
        sns.boxplot(data=self.data, x='decade_label', y='pts', 
                   hue='decade_label', palette='Set2', width=0.6, legend=False)
        
        plt.title('Distribución de Puntos por Jugador según Décadas NBA', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Década', fontsize=12, fontweight='bold')
        plt.ylabel('Puntos por Jugador', fontsize=12, fontweight='bold')
        
        # Añadir estadísticas descriptivas
        for i, decade in enumerate(sorted(self.data['decade_label'].unique())):
            decade_data = self.data[self.data['decade_label'] == decade]['pts']
            median_val = decade_data.median()
            plt.text(i, median_val + 1, f'Med: {median_val:.1f}', 
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        # Guardar gráfica
        output_path = os.path.join(self.charts_dir, 'boxplot_puntos_decadas.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Gráfica guardada en: {output_path}")
    
    def create_all_visualizations(self):
        """
        Crea todas las visualizaciones solicitadas.
        """
        print("Iniciando creación de todas las visualizaciones...")
        print("=" * 50)
        
        # Cargar datos
        if not self.load_data():
            return
        
        print("\n1. Creando gráfica de evolución temporal de puntos...")
        self.create_temporal_points_evolution()
        
        print("\n2. Creando gráfica de barras apiladas de rendimiento...")
        self.create_stacked_wins_losses_chart()
        
        print("\n3. Creando box plot de distribución de puntos por décadas...")
        self.create_points_distribution_boxplot()
        
        print("\n" + "=" * 50)
        print("¡Todas las visualizaciones han sido creadas exitosamente!")
        print(f"Las gráficas se han guardado en: {self.charts_dir}")

def main():
    """Función principal para ejecutar las visualizaciones."""
    visualizer = NBADataVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main()