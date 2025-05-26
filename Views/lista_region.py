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

import formulario_region

class lista_region:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Lista de Regiones")
        self.window.geometry("900x600")
        self.window.resizable(True, True)
        
        # Variables
        self.regions_data = []
        
        # Variables para búsqueda
        self.search_var = tk.StringVar()
        self.search_continent_var = tk.StringVar()
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar datos
        self.cargar_regiones()
        
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
        main_frame.rowconfigure(2, weight=1)
        
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
        
        # Frame para botones superiores
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Botones
        btn_refresh = ttk.Button(
            buttons_frame,
            text="Actualizar",
            command=self.cargar_regiones
        )
        btn_refresh.grid(row=0, column=0, padx=(0, 5))
        
        btn_new = ttk.Button(
            buttons_frame,
            text="Nueva Región",
            command=self.crear_region
        )
        btn_new.grid(row=0, column=1, padx=5)
        
        # Frame de búsqueda
        self.crear_frame_busqueda(main_frame)
        
        # TreeView para mostrar regiones
        self.crear_treeview(main_frame)
        
        # Frame para botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        btn_edit = ttk.Button(
            bottom_frame,
            text="Editar Seleccionada",
            command=self.editar_region
        )
        btn_edit.grid(row=0, column=0, padx=(0, 5))
        
        btn_delete = ttk.Button(
            bottom_frame,
            text="Eliminar Seleccionada",
            command=self.borrar_region_seleccionada
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

    def crear_frame_busqueda(self, parent):
        """Crear el frame de búsqueda"""
        search_frame = ttk.LabelFrame(parent, text="Búsqueda", padding="10")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)
        
        # Búsqueda por nombre
        ttk.Label(search_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # Búsqueda por ID de continente
        ttk.Label(search_frame, text="ID Continente:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        continent_entry = ttk.Entry(search_frame, textvariable=self.search_continent_var, width=15)
        continent_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # Botones de búsqueda
        btn_search = ttk.Button(
            search_frame,
            text="Buscar",
            command=self.buscar_regiones
        )
        btn_search.grid(row=0, column=4, padx=5)
        
        btn_clear = ttk.Button(
            search_frame,
            text="Limpiar",
            command=self.limpiar_busqueda
        )
        btn_clear.grid(row=0, column=5, padx=5)
        
        # Configurar eventos para búsqueda en tiempo real (opcional)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        continent_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Evento Enter para buscar
        search_entry.bind('<Return>', lambda e: self.buscar_regiones())
        continent_entry.bind('<Return>', lambda e: self.buscar_regiones())
    
    def crear_treeview(self, parent):
        """Crear el TreeView para mostrar las regiones"""
        # Frame para el TreeView y scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        self.tree.bind('<Double-1>', lambda e: self.editar_region())
    
    def cargar_regiones(self):
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

    def buscar_regiones(self):
        """Buscar regiones según los criterios especificados"""
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            nombre = self.search_var.get().strip()
            continent_id = self.search_continent_var.get().strip()
            
            # Si ambos campos están vacíos, mostrar todas las regiones
            if not nombre and not continent_id:
                self.cargar_regiones()
                return
            
            # Realizar búsqueda avanzada
            self.regions_data = ControlRegion.buscarRegionAvanzada(nombre, continent_id)
            
            # Insertar resultados en el TreeView
            if self.regions_data:
                for region in self.regions_data:
                    self.tree.insert('', tk.END, values=region)
            
            # Actualizar status
            total_found = len(self.regions_data) if self.regions_data else 0
            status_text = f"Búsqueda: {total_found} regiones encontradas"
            self.window.title(f"Lista de Regiones - {status_text}")
            
            if total_found == 0:
                messagebox.showinfo("Búsqueda", "No se encontraron regiones que coincidan con los criterios de búsqueda.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")

    def limpiar_busqueda(self):
        """Limpiar los campos de búsqueda y recargar todas las regiones"""
        self.search_var.set("")
        self.search_continent_var.set("")
        self.cargar_regiones()

    def on_search_change(self, event=None):
        """Manejar cambios en los campos de búsqueda (búsqueda en tiempo real opcional)"""
        # Puedes comentar esta línea si no quieres búsqueda en tiempo real
        # self.buscar_regiones()
        pass
    
    def get_region_seleccionada(self):
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
    
    def crear_region(self):
        """Abrir ventana para crear nueva región"""
        def on_close():
            # Decidir si recargar todas las regiones o mantener la búsqueda actual
            if self.search_var.get().strip() or self.search_continent_var.get().strip():
                self.buscar_regiones()
            else:
                self.cargar_regiones()
        
        formulario_region.formulario_region(self.window, on_close_callback=on_close)
    
    def editar_region(self):
        """Editar la región seleccionada"""
        result = self.get_region_seleccionada()
        if result:
            region, region_id = result
            
            def on_close():
                # Decidir si recargar todas las regiones o mantener la búsqueda actual
                if self.search_var.get().strip() or self.search_continent_var.get().strip():
                    self.buscar_regiones()
                else:
                    self.cargar_regiones()
            
            formulario_region.formulario_region(self.window, region=region, region_id=region_id, on_close_callback=on_close)
    
    def borrar_region_seleccionada(self):
        """Eliminar la región seleccionada"""
        result = self.get_region_seleccionada()
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
                    
                    # Decidir si recargar todas las regiones o mantener la búsqueda actual
                    if self.search_var.get().strip() or self.search_continent_var.get().strip():
                        self.buscar_regiones()
                    else:
                        self.cargar_regiones()
                        
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
    app = lista_region()
    app.window.mainloop()