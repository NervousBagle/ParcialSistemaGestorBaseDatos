import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar directorios al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("Models")
from Region import Region # type: ignore

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("Controllers")
from ControlRegion import ControlRegion # type: ignore

from region_form_view import RegionFormView

class RegionListView:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Lista de Regiones")
        self.window.geometry("900x500")
        self.window.resizable(True, True)
        
        # Variables
        self.regions_data = []
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar datos
        self.load_regions()
        
        # Centrar ventana
        self.center_window()
        
        # Hacer que la ventana sea modal si tiene padre
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título y botones superiores
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(
            header_frame, 
            text="Lista de Regiones", 
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Frame para botones
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Botones
        btn_refresh = ttk.Button(
            buttons_frame,
            text="Actualizar",
            command=self.load_regions
        )
        btn_refresh.grid(row=0, column=0, padx=(0, 5))
        
        btn_new = ttk.Button(
            buttons_frame,
            text="Nueva Región",
            command=self.create_region
        )
        btn_new.grid(row=0, column=1, padx=5)
        
        # TreeView para mostrar regiones
        self.create_treeview(main_frame)
        
        # Frame para botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        btn_edit = ttk.Button(
            bottom_frame,
            text="Editar Seleccionada",
            command=self.edit_selected_region
        )
        btn_edit.grid(row=0, column=0, padx=(0, 5))
        
        btn_delete = ttk.Button(
            bottom_frame,
            text="Eliminar Seleccionada",
            command=self.delete_selected_region
        )
        btn_delete.grid(row=0, column=1, padx=5)
        
        btn_close = ttk.Button(
            bottom_frame,
            text="Cerrar",
            command=self.window.destroy
        )
        btn_close.grid(row=0, column=2, sticky=tk.E)
        
        # Configurar expansión del frame inferior
        bottom_frame.columnconfigure(2, weight=1)
    
    def create_treeview(self, parent):
        """Crear el TreeView para mostrar las regiones"""
        # Frame para el TreeView y scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # TreeView
        columns = ('ID', 'Nombre', 'ID Continente')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID Región')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('ID Continente', text='ID Continente')
        
        self.tree.column('ID', width=100, anchor=tk.CENTER)
        self.tree.column('Nombre', width=300, anchor=tk.W)
        self.tree.column('ID Continente', width=120, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Evento de doble clic
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_region())
    
    def load_regions(self):
        """Cargar regiones desde la base de datos"""
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener datos del controlador
            self.regions_data = ControlRegion.mostrarRegion()
            
            # Insertar datos en el TreeView
            if self.regions_data:
                for region in self.regions_data:
                    self.tree.insert('', tk.END, values=region)
            
            # Actualizar status
            status_text = f"Se encontraron {len(self.regions_data) if self.regions_data else 0} regiones"
            self.window.title(f"Lista de Regiones - {status_text}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar regiones: {str(e)}")
    
    def get_selected_region(self):
        """Obtener la región seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una región")
            return None
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Crear objeto Region con los datos seleccionados
        region = Region(values[0], values[1], values[2])
        return region, values[0]  # Retornar también el ID original
    
    def create_region(self):
        """Abrir ventana para crear nueva región"""
        def on_close():
            self.load_regions()  # Recargar la lista cuando se cierre el formulario
        
        RegionFormView(self.window, on_close_callback=on_close)
    
    def edit_selected_region(self):
        """Editar la región seleccionada"""
        result = self.get_selected_region()
        if result:
            region, region_id = result
            
            def on_close():
                self.load_regions()  # Recargar la lista cuando se cierre el formulario
            
            RegionFormView(self.window, region=region, region_id=region_id, on_close_callback=on_close)
    
    def delete_selected_region(self):
        """Eliminar la región seleccionada"""
        result = self.get_selected_region()
        if result:
            region, region_id = result
            
            # Confirmar eliminación
            confirm = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar la región '{region.get_name()}'?\n\n"
                "Esta acción no se puede deshacer."
            )
            
            if confirm:
                try:
                    ControlRegion.borrarRegion(region.get_name())
                    messagebox.showinfo("Éxito", "Región eliminada correctamente")
                    self.load_regions()  # Recargar la lista
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar región: {str(e)}")
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    app = RegionListView()
    app.window.mainloop()