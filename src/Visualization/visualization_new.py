import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SiniestrosVialesAnalyzer:
    """
    Clase para crear visualizaciones analíticas profesionales de datos de siniestros viales.
    """
    
    def __init__(self, data_dir='src/Extract/Files/cleaned', charts_dir='src/Visualization/Charts'):
        """
        Inicializa el analizador de siniestros viales.
        
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
        
        # Configurar estilo matplotlib/seaborn
        plt.style.use('default')
        sns.set_palette("husl")
        sns.set_context("notebook", font_scale=1.0)
        
    def load_data(self):
        """Carga todos los archivos CSV necesarios y prepara los datos."""
        try:
            print("\n📊 Cargando datos de siniestros viales...")
            
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
            
            # Mapeo manual de meses (sin dependencia de locale)
            meses_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                         7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
            self.siniestros['MES_NOMBRE'] = self.siniestros['MES'].map(meses_dict).fillna('Desconocido')
            
            self.siniestros['DIA_SEMANA'] = self.siniestros['FECHA'].dt.dayofweek
            
            # Mapeo manual de días (sin dependencia de locale)
            dias_dict = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
            self.siniestros['DIA_NOMBRE'] = self.siniestros['DIA_SEMANA'].map(dias_dict).fillna('Desconocido')
            
            # Extraer hora del día
            if 'HORA' in self.siniestros.columns:
                self.siniestros['HORA_NUM'] = pd.to_datetime(self.siniestros['HORA'], format='%H:%M:%S', errors='coerce').dt.hour
            
            print(f"✅ Datos cargados exitosamente:")
            print(f"   - Siniestros: {len(self.siniestros):,}")
            print(f"   - Vehículos: {len(self.vehiculos):,}")
            print(f"   - Actores viales: {len(self.actores):,}")
            print(f"   - Hipótesis: {len(self.hipotesis):,}")
            
            return True
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_descripcion(self, hoja, campo, codigo):
        """Obtiene la descripción de un código del diccionario."""
        try:
            if pd.isna(codigo):
                return 'Desconocido'
            desc = self.diccionario[
                (self.diccionario['HOJA'] == hoja) & 
                (self.diccionario['CAMPO'] == campo) & 
                (self.diccionario['CODIGO'] == int(float(codigo)))
            ]['DESCRIPCION'].values
            return desc[0] if len(desc) > 0 else f'Código {codigo}'
        except:
            return f'Código {codigo}'
    
    def plot_gravedad_distribucion(self):
        """Gráfica 1: Distribución de siniestros por gravedad."""
        print("\n📈 Creando gráfica: Distribución por gravedad...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Obtener conteo y descripciones
        gravedad_counts = self.siniestros['GRAVEDAD'].value_counts().sort_index()
        labels = [self.get_descripcion('SINIESTROS', 'GRAVEDAD', cod) for cod in gravedad_counts.index]
        
        # Gráfica de barras
        colors = ['#d62728', '#ff7f0e', '#2ca02c']
        axes[0].bar(range(len(gravedad_counts)), gravedad_counts.values, color=colors, alpha=0.8, edgecolor='black')
        axes[0].set_xticks(range(len(gravedad_counts)))
        axes[0].set_xticklabels(labels, rotation=15, ha='right')
        axes[0].set_ylabel('Número de Siniestros', fontweight='bold')
        axes[0].set_title('Distribución de Siniestros por Gravedad', fontweight='bold', fontsize=13)
        axes[0].grid(axis='y', alpha=0.3)
        
        # Añadir valores sobre las barras
        for i, v in enumerate(gravedad_counts.values):
            axes[0].text(i, v + 100, f'{v:,}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfica de pastel
        axes[1].pie(gravedad_counts.values, labels=labels, autopct='%1.1f%%', 
                   colors=colors, startangle=90, textprops={'fontweight': 'bold'})
        axes[1].set_title('Proporción de Gravedad', fontweight='bold', fontsize=13)
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '01_distribucion_gravedad.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_evolucion_temporal(self):
        """Gráfica 2: Evolución temporal de siniestros."""
        print("\n📈 Creando gráfica: Evolución temporal...")
        
        fig, axes = plt.subplots(2, 1, figsize=(16, 10))
        
        # Por año
        siniestros_año = self.siniestros.groupby('AÑO').size()
        axes[0].plot(siniestros_año.index, siniestros_año.values, marker='o', linewidth=2.5, 
                    markersize=8, color='#1f77b4')
        axes[0].fill_between(siniestros_año.index, siniestros_año.values, alpha=0.3)
        axes[0].set_xlabel('Año', fontweight='bold')
        axes[0].set_ylabel('Número de Siniestros', fontweight='bold')
        axes[0].set_title('Evolución Anual de Siniestros Viales', fontweight='bold', fontsize=14)
        axes[0].grid(True, alpha=0.3)
        
        # Añadir valores
        for x, y in zip(siniestros_año.index, siniestros_año.values):
            axes[0].text(x, y + 50, f'{y:,}', ha='center', va='bottom', fontsize=9)
        
        # Por mes agregado
        siniestros_mes = self.siniestros.groupby('MES').size()
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        axes[1].bar(range(1, 13), [siniestros_mes.get(i, 0) for i in range(1, 13)], 
                   color='#ff7f0e', alpha=0.8, edgecolor='black')
        axes[1].set_xticks(range(1, 13))
        axes[1].set_xticklabels(meses)
        axes[1].set_xlabel('Mes', fontweight='bold')
        axes[1].set_ylabel('Número de Siniestros', fontweight='bold')
        axes[1].set_title('Distribución Mensual de Siniestros', fontweight='bold', fontsize=14)
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '02_evolucion_temporal.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_tipo_accidente(self):
        """Gráfica 3: Distribución por tipo de accidente (clase)."""
        print("\n📈 Creando gráfica: Tipos de accidente...")
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        clase_counts = self.siniestros['CLASE'].value_counts().sort_values(ascending=True)
        labels = [self.get_descripcion('SINIESTROS', 'CLASE', cod) for cod in clase_counts.index]
        
        colors = sns.color_palette("Set2", len(clase_counts))
        bars = ax.barh(range(len(clase_counts)), clase_counts.values, color=colors, 
                      alpha=0.8, edgecolor='black')
        
        ax.set_yticks(range(len(clase_counts)))
        ax.set_yticklabels(labels)
        ax.set_xlabel('Número de Siniestros', fontweight='bold')
        ax.set_title('Distribución de Siniestros por Tipo de Accidente', fontweight='bold', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Añadir valores
        for i, v in enumerate(clase_counts.values):
            ax.text(v + 50, i, f'{v:,}', va='center', fontweight='bold')
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '03_tipos_accidente.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_distribucion_horaria(self):
        """Gráfica 4: Distribución de siniestros por hora del día."""
        print("\n📈 Creando gráfica: Distribución horaria...")
        
        if 'HORA_NUM' not in self.siniestros.columns or self.siniestros['HORA_NUM'].isna().all():
            print("   ⚠️ No hay datos de hora disponible")
            return
        
        fig, ax = plt.subplots(figsize=(16, 7))
        
        hora_counts = self.siniestros['HORA_NUM'].value_counts().sort_index()
        
        colors_hora = ['#2c3e50' if 0 <= h < 6 else 
                       '#e74c3c' if 6 <= h < 12 else 
                       '#f39c12' if 12 <= h < 18 else 
                       '#34495e' for h in hora_counts.index]
        
        bars = ax.bar(hora_counts.index, hora_counts.values, color=colors_hora, 
                     alpha=0.8, edgecolor='black', width=0.8)
        
        ax.set_xlabel('Hora del Día', fontweight='bold')
        ax.set_ylabel('Número de Siniestros', fontweight='bold')
        ax.set_title('Distribución de Siniestros por Hora del Día', fontweight='bold', fontsize=14)
        ax.set_xticks(range(0, 24))
        ax.grid(axis='y', alpha=0.3)
        
        # Añadir leyenda de franjas horarias
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2c3e50', label='Madrugada (0-6h)'),
            Patch(facecolor='#e74c3c', label='Mañana (6-12h)'),
            Patch(facecolor='#f39c12', label='Tarde (12-18h)'),
            Patch(facecolor='#34495e', label='Noche (18-24h)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '04_distribucion_horaria.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_top_localidades(self):
        """Gráfica 5: Top 10 localidades con más siniestros."""
        print("\n📈 Creando gráfica: Top localidades...")
        
        if 'CODIGO_LOCALIDAD' not in self.siniestros.columns:
            print("   ⚠️ No hay datos de localidad disponible")
            return
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        localidad_counts = self.siniestros['CODIGO_LOCALIDAD'].value_counts().head(10)
        
        colors = sns.color_palette("coolwarm", len(localidad_counts))
        bars = ax.barh(range(len(localidad_counts)), localidad_counts.values, 
                      color=colors, alpha=0.8, edgecolor='black')
        
        ax.set_yticks(range(len(localidad_counts)))
        ax.set_yticklabels([f'Localidad {int(cod)}' for cod in localidad_counts.index])
        ax.set_xlabel('Número de Siniestros', fontweight='bold')
        ax.set_title('Top 10 Localidades con Más Siniestros', fontweight='bold', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Añadir valores
        for i, v in enumerate(localidad_counts.values):
            ax.text(v + 20, i, f'{v:,}', va='center', fontweight='bold')
        
        plt.gca().invert_yaxis()
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '05_top_localidades.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_perfil_victimas(self):
        """Gráfica 6: Perfil de víctimas (edad y sexo)."""
        print("\n📈 Creando gráfica: Perfil de víctimas...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Distribución por sexo
        if 'SEXO' in self.actores.columns:
            sexo_counts = self.actores['SEXO'].value_counts()
            sexo_labels = [self.get_descripcion('ACTOR_VIAL', 'SEXO', cod) for cod in sexo_counts.index]
            
            colors_sexo = ['#3498db', '#e74c3c', '#95a5a6']
            axes[0].pie(sexo_counts.values, labels=sexo_labels, autopct='%1.1f%%',
                       colors=colors_sexo[:len(sexo_counts)], startangle=90,
                       textprops={'fontweight': 'bold', 'fontsize': 11})
            axes[0].set_title('Distribución por Sexo', fontweight='bold', fontsize=13)
        
        # Distribución por edad
        if 'EDAD' in self.actores.columns:
            # Convertir edad a numérico
            self.actores['EDAD_NUM'] = pd.to_numeric(self.actores['EDAD'], errors='coerce')
            edades_validas = self.actores[self.actores['EDAD_NUM'].notna() & (self.actores['EDAD_NUM'] > 0) & (self.actores['EDAD_NUM'] < 120)]
            
            if len(edades_validas) > 0:
                bins = [0, 18, 30, 45, 60, 120]
                labels_edad = ['0-17', '18-29', '30-44', '45-59', '60+']
                edades_validas['GRUPO_EDAD'] = pd.cut(edades_validas['EDAD_NUM'], bins=bins, labels=labels_edad)
                
                edad_counts = edades_validas['GRUPO_EDAD'].value_counts().sort_index()
                colors_edad = sns.color_palette("viridis", len(edad_counts))
                
                axes[1].bar(range(len(edad_counts)), edad_counts.values, 
                           color=colors_edad, alpha=0.8, edgecolor='black')
                axes[1].set_xticks(range(len(edad_counts)))
                axes[1].set_xticklabels(edad_counts.index, rotation=0)
                axes[1].set_xlabel('Grupo de Edad', fontweight='bold')
                axes[1].set_ylabel('Número de Personas', fontweight='bold')
                axes[1].set_title('Distribución por Grupo de Edad', fontweight='bold', fontsize=13)
                axes[1].grid(axis='y', alpha=0.3)
                
                # Añadir valores
                for i, v in enumerate(edad_counts.values):
                    axes[1].text(i, v + 50, f'{v:,}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '06_perfil_victimas.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_vehiculos_involucrados(self):
        """Gráfica 7: Tipos de vehículos involucrados."""
        print("\n📈 Creando gráfica: Vehículos involucrados...")
        
        if 'VEHICULO' not in self.vehiculos.columns:
            print("   ⚠️ No hay datos de vehículos disponible")
            return
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        vehiculo_counts = self.vehiculos['VEHICULO'].value_counts().head(10)
        labels_vehiculo = [self.get_descripcion('VEHICULOS', 'VEHICULO', cod) for cod in vehiculo_counts.index]
        
        colors = sns.color_palette("tab10", len(vehiculo_counts))
        bars = ax.barh(range(len(vehiculo_counts)), vehiculo_counts.values,
                      color=colors, alpha=0.8, edgecolor='black')
        
        ax.set_yticks(range(len(vehiculo_counts)))
        ax.set_yticklabels(labels_vehiculo)
        ax.set_xlabel('Número de Vehículos Involucrados', fontweight='bold')
        ax.set_title('Top 10 Tipos de Vehículos Involucrados en Siniestros', fontweight='bold', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Añadir valores
        for i, v in enumerate(vehiculo_counts.values):
            ax.text(v + 50, i, f'{v:,}', va='center', fontweight='bold')
        
        plt.gca().invert_yaxis()
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '07_vehiculos_involucrados.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_heatmap_dia_hora(self):
        """Gráfica 8: Heatmap de siniestros por día de semana y hora."""
        print("\n📈 Creando gráfica: Heatmap día-hora...")
        
        if 'HORA_NUM' not in self.siniestros.columns or 'DIA_SEMANA' not in self.siniestros.columns:
            print("   ⚠️ No hay datos suficientes para el heatmap")
            return
        
        # Crear tabla cruzada
        heatmap_data = pd.crosstab(self.siniestros['DIA_SEMANA'], self.siniestros['HORA_NUM'])
        
        # Nombres de días
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        fig, ax = plt.subplots(figsize=(18, 7))
        
        sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, fmt='d', 
                   cbar_kws={'label': 'Número de Siniestros'},
                   linewidths=0.5, ax=ax)
        
        ax.set_yticklabels([dias[i] for i in heatmap_data.index], rotation=0)
        ax.set_xlabel('Hora del Día', fontweight='bold')
        ax.set_ylabel('Día de la Semana', fontweight='bold')
        ax.set_title('Intensidad de Siniestros por Día y Hora', fontweight='bold', fontsize=14)
        
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '08_heatmap_dia_hora.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_causas_principales(self):
        """Gráfica 9: Principales causas de siniestros."""
        print("\n📈 Creando gráfica: Causas principales...")
        
        if 'CODIGO_CAUSA' not in self.hipotesis.columns:
            print("   ⚠️ No hay datos de causas disponible")
            return
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        causa_counts = self.hipotesis['CODIGO_CAUSA'].value_counts().head(10)
        labels_causa = [self.get_descripcion('HIPOTESIS', 'CODIGO_CAUSA', cod) for cod in causa_counts.index]
        
        colors = sns.color_palette("Spectral", len(causa_counts))
        bars = ax.barh(range(len(causa_counts)), causa_counts.values,
                      color=colors, alpha=0.8, edgecolor='black')
        
        ax.set_yticks(range(len(causa_counts)))
        ax.set_yticklabels(labels_causa, fontsize=10)
        ax.set_xlabel('Número de Casos', fontweight='bold')
        ax.set_title('Top 10 Causas de Siniestros Viales', fontweight='bold', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Añadir valores
        for i, v in enumerate(causa_counts.values):
            ax.text(v + 20, i, f'{v:,}', va='center', fontweight='bold')
        
        plt.gca().invert_yaxis()
        plt.tight_layout()
        output_path = os.path.join(self.charts_dir, '09_causas_principales.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def plot_resumen_dashboard(self):
        """Gráfica 10: Dashboard resumen con múltiples métricas."""
        print("\n📈 Creando gráfica: Dashboard resumen...")
        
        fig = plt.figure(figsize=(18, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Total de siniestros
        ax1 = fig.add_subplot(gs[0, 0])
        total_siniestros = len(self.siniestros)
        ax1.text(0.5, 0.5, f'{total_siniestros:,}', ha='center', va='center', 
                fontsize=40, fontweight='bold', color='#2c3e50')
        ax1.text(0.5, 0.2, 'Total Siniestros', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        ax1.axis('off')
        ax1.set_facecolor('#ecf0f1')
        
        # 2. Siniestros con muertos
        ax2 = fig.add_subplot(gs[0, 1])
        con_muertos = len(self.siniestros[self.siniestros['GRAVEDAD'] == 1])
        ax2.text(0.5, 0.5, f'{con_muertos:,}', ha='center', va='center', 
                fontsize=40, fontweight='bold', color='#e74c3c')
        ax2.text(0.5, 0.2, 'Con Muertos', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        ax2.axis('off')
        ax2.set_facecolor('#fadbd8')
        
        # 3. Siniestros con heridos
        ax3 = fig.add_subplot(gs[0, 2])
        con_heridos = len(self.siniestros[self.siniestros['GRAVEDAD'] == 2])
        ax3.text(0.5, 0.5, f'{con_heridos:,}', ha='center', va='center', 
                fontsize=40, fontweight='bold', color='#f39c12')
        ax3.text(0.5, 0.2, 'Con Heridos', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        ax3.axis('off')
        ax3.set_facecolor('#fdebd0')
        
        # 4. Evolución anual pequeña
        ax4 = fig.add_subplot(gs[1, :2])
        siniestros_año = self.siniestros.groupby('AÑO').size()
        ax4.plot(siniestros_año.index, siniestros_año.values, marker='o', 
                linewidth=2, markersize=6, color='#3498db')
        ax4.fill_between(siniestros_año.index, siniestros_año.values, alpha=0.3, color='#3498db')
        ax4.set_title('Evolución Anual', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.set_xlabel('Año', fontweight='bold', fontsize=10)
        ax4.set_ylabel('Siniestros', fontweight='bold', fontsize=10)
        
        # 5. Top 5 tipos de accidente
        ax5 = fig.add_subplot(gs[1, 2])
        clase_counts = self.siniestros['CLASE'].value_counts().head(5)
        labels_clase = [self.get_descripcion('SINIESTROS', 'CLASE', cod)[:15] for cod in clase_counts.index]
        ax5.pie(clase_counts.values, labels=labels_clase, autopct='%1.0f%%', 
               textprops={'fontsize': 8, 'fontweight': 'bold'})
        ax5.set_title('Top 5 Tipos', fontweight='bold', fontsize=11)
        
        # 6. Distribución horaria compacta
        if 'HORA_NUM' in self.siniestros.columns:
            ax6 = fig.add_subplot(gs[2, :])
            hora_counts = self.siniestros['HORA_NUM'].value_counts().sort_index()
            ax6.bar(hora_counts.index, hora_counts.values, color='#9b59b6', alpha=0.7, edgecolor='black')
            ax6.set_title('Distribución Horaria', fontweight='bold')
            ax6.set_xlabel('Hora', fontweight='bold', fontsize=10)
            ax6.set_ylabel('Siniestros', fontweight='bold', fontsize=10)
            ax6.set_xticks(range(0, 24, 2))
            ax6.grid(axis='y', alpha=0.3)
        
        plt.suptitle('DASHBOARD - Análisis de Siniestros Viales', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        output_path = os.path.join(self.charts_dir, '10_dashboard_resumen.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✓ Guardada: {output_path}")
        plt.show()
    
    def generar_todas_graficas(self):
        """
        Genera todas las visualizaciones de análisis.
        """
        print("\n" + "="*70)
        print("🚗 INICIANDO ANÁLISIS COMPLETO DE SINIESTROS VIALES 🚗")
        print("="*70)
        
        # Cargar datos
        if not self.load_data():
            print("\n❌ No se pudieron cargar los datos. Abortando análisis.")
            return
        
        print("\n" + "="*70)
        print("📊 GENERANDO VISUALIZACIONES ANALÍTICAS")
        print("="*70)
        
        try:
            self.plot_gravedad_distribucion()
            self.plot_evolucion_temporal()
            self.plot_tipo_accidente()
            self.plot_distribucion_horaria()
            self.plot_top_localidades()
            self.plot_perfil_victimas()
            self.plot_vehiculos_involucrados()
            self.plot_heatmap_dia_hora()
            self.plot_causas_principales()
            self.plot_resumen_dashboard()
            
            print("\n" + "="*70)
            print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
            print(f"📁 Todas las gráficas guardadas en: {self.charts_dir}")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error durante la generación de gráficas: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Función principal para ejecutar el análisis completo."""
    analyzer = SiniestrosVialesAnalyzer()
    analyzer.generar_todas_graficas()

if __name__ == "__main__":
    main()
