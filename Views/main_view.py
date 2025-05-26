import tkinter as tk
from tkinter import ttk
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from region_list_view import RegionListView
from region_form_view import RegionFormView

class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Regiones")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Centrar ventana
        self.center_window()
    
    def setup_styles(self):
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12))
        style.configure('Action.TButton', padding=10)
    
    def create_widgets(self):
        """Crear los widgets de la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Sistema de Gestión de Regiones", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame, 
            text="Seleccione una opción para continuar", 
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame para botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=20)
        
        # Botón para ver lista de regiones
        btn_list = ttk.Button(
            buttons_frame,
            text="Ver Lista de Regiones",
            style='Action.TButton',
            command=self.open_region_list,
            width=25
        )
        btn_list.grid(row=0, column=0, pady=10)
        
        # Botón para crear nueva región
        btn_create = ttk.Button(
            buttons_frame,
            text="Crear Nueva Región",
            style='Action.TButton',
            command=self.open_create_region,
            width=25
        )
        btn_create.grid(row=1, column=0, pady=10)
        
        # Botón para salir
        btn_exit = ttk.Button(
            buttons_frame,
            text="Salir",
            command=self.root.quit,
            width=25
        )
        btn_exit.grid(row=2, column=0, pady=20)
        
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_region_list(self):
        """Abrir la ventana de lista de regiones"""
        RegionListView(self.root)
    
    def open_create_region(self):
        """Abrir la ventana para crear nueva región"""
        RegionFormView(self.root)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainView()
    app.run()