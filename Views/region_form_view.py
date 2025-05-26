import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar directorios al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("Models")

from ControlRegion import ControlRegion # type: ignore
from Region import Region # type: ignore

class RegionFormView:
    def __init__(self, parent=None, region=None, region_id=None, on_close_callback=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.parent = parent
        self.region = region
        self.region_id = region_id
        self.on_close_callback = on_close_callback
        
        # Determinar modo (crear o editar)
        self.is_edit_mode = region is not None
        
        # Configurar ventana
        title = "Editar Región" if self.is_edit_mode else "Nueva Región"
        self.window.title(title)
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Variables para los campos
        self.name_var = tk.StringVar()
        self.continent_id_var = tk.StringVar()
        
        # Crear interfaz
        self.create_widgets()
        
        # Si es modo edición, cargar datos
        if self.is_edit_mode:
            self.load_region_data()
        
        # Centrar ventana
        self.center_window()
        
        # Hacer que la ventana sea modal si tiene padre
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
        
        # Configurar evento de cierre
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def create_widgets(self):
        """Crear los widgets del formulario"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_text = "Editar Región" if self.is_edit_mode else "Nueva Región"
        title_label = ttk.Label(
            main_frame, 
            text=title_text, 
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campo Nombre
        ttk.Label(main_frame, text="Nombre de la Región:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        name_entry = ttk.Entry(
            main_frame, 
            textvariable=self.name_var,
            width=30
        )
        name_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        name_entry.focus()  # Poner foco en el primer campo
        
        # Campo ID Continente
        ttk.Label(main_frame, text="ID del Continente:").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        continent_id_entry = ttk.Entry(
            main_frame, 
            textvariable=self.continent_id_var,
            width=30
        )
        continent_id_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        info_text = """
        • El nombre de la región debe ser único
        • El ID del continente debe ser un número entero
        • Ambos campos son obligatorios
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=0, column=0)
        
        # Frame para botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Botón Guardar
        save_text = "Actualizar" if self.is_edit_mode else "Crear"
        btn_save = ttk.Button(
            buttons_frame,
            text=save_text,
            command=self.save_region
        )
        btn_save.grid(row=0, column=0, padx=(0, 10))
        
        # Botón Cancelar
        btn_cancel = ttk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.on_window_close
        )
        btn_cancel.grid(row=0, column=1)
        
        # Bindings para Enter y Escape
        self.window.bind('<Return>', lambda e: self.save_region())
        self.window.bind('<Escape>', lambda e: self.on_window_close())
    
    def load_region_data(self):
        """Cargar datos de la región en modo edición"""
        if self.region:
            self.name_var.set(self.region.get_name() or "")
            self.continent_id_var.set(str(self.region.get_continent_id() or ""))
    
    def validate_form(self):
        """Validar los datos del formulario"""
        name = self.name_var.get().strip()
        continent_id = self.continent_id_var.get().strip()
        
        # Validar campos obligatorios
        if not name:
            messagebox.showerror("Error de Validación", "El nombre de la región es obligatorio")
            return False
        
        if not continent_id:
            messagebox.showerror("Error de Validación", "El ID del continente es obligatorio")
            return False
        
        # Validar que el ID del continente sea un número
        try:
            continent_id_int = int(continent_id)
            if continent_id_int <= 0:
                raise ValueError("El ID debe ser positivo")
        except ValueError:
            messagebox.showerror("Error de Validación", "El ID del continente debe ser un número entero positivo")
            return False
        
        return True
    
    def save_region(self):
        """Guardar la región"""
        if not self.validate_form():
            return
        
        try:
            name = self.name_var.get().strip()
            continent_id = int(self.continent_id_var.get().strip())
            
            if self.is_edit_mode:
                # Actualizar región existente
                region = Region(self.region_id, name, continent_id)
                ControlRegion.actualizarRegion(self.region_id, region)
                messagebox.showinfo("Éxito", "Región actualizada correctamente")
            else:
                # Crear nueva región
                region = Region(None, name, continent_id)
                ControlRegion.ingresarRegion(region)
                messagebox.showinfo("Éxito", "Región creada correctamente")
            
            # Cerrar ventana
            self.on_window_close()
            
        except Exception as e:
            error_msg = f"Error al {'actualizar' if self.is_edit_mode else 'crear'} la región: {str(e)}"
            messagebox.showerror("Error", error_msg)
    
    def on_window_close(self):
        """Manejar el cierre de la ventana"""
        if self.on_close_callback:
            self.on_close_callback()
        self.window.destroy()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    app = RegionFormView()
    app.window.mainloop()