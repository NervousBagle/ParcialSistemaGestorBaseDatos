### 
# Vista donde se ingrezan los datos de la entrada que se quiera añadir y al darle a un boton se pasa al controlador para añadirlo 
###
from datetime import datetime
import re

class EntradaModel:
    """Modelo para representar una entrada de datos"""
    
    def __init__(self, nombre, email, telefono=None, descripcion=None):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.descripcion = descripcion
        self.fecha_creacion = datetime.now()
        self.id = None  # Se asignará al guardar

class EntradaController:
    """Controlador para manejar las operaciones de entrada de datos"""
    
    def __init__(self):
        self.entradas = []  # Simula base de datos
        self.contador_id = 1
    
    def agregar_entrada(self, datos):
        """
        Añade una nueva entrada al sistema
        
        Args:
            datos (dict): Diccionario con los datos de la entrada
                        {'nombre': str, 'email': str, 'telefono': str, 'descripcion': str}
        
        Returns:
            dict: Resultado de la operación
        """
        
        # Validar datos de entrada
        validacion = self._validar_datos(datos)
        if not validacion['es_valido']:
            return {
                'exito': False,
                'errores': validacion['errores'],
                'codigo': 400
            }
        
        # Crear nueva entrada
        try:
            nueva_entrada = EntradaModel(
                nombre=datos['nombre'].strip(),
                email=datos['email'].strip().lower(),
                telefono=datos.get('telefono', '').strip() if datos.get('telefono') else None,
                descripcion=datos.get('descripcion', '').strip() if datos.get('descripcion') else None
            )
            
            # Asignar ID y guardar
            nueva_entrada.id = self.contador_id
            self.entradas.append(nueva_entrada)
            self.contador_id += 1
            
            # Log de la operación
            self._log_operacion('CREAR', nueva_entrada)
            
            return {
                'exito': True,
                'mensaje': 'Entrada creada exitosamente',
                'id': nueva_entrada.id,
                'datos': self._entrada_a_dict(nueva_entrada),
                'codigo': 201
            }
            
        except Exception as e:
            return {
                'exito': False,
                'error': f'Error al crear entrada: {str(e)}',
                'codigo': 500
            }
    
    def _validar_datos(self, datos):
        """Valida los datos de entrada"""
        errores = []
        
        # Validar tipo de datos
        if not isinstance(datos, dict):
            return {'es_valido': False, 'errores': ['Los datos deben ser un diccionario']}
        
        # Validar nombre
        nombre = datos.get('nombre', '').strip()
        if not nombre:
            errores.append('El nombre es obligatorio')
        elif len(nombre) < 2:
            errores.append('El nombre debe tener al menos 2 caracteres')
        elif len(nombre) > 100:
            errores.append('El nombre no puede exceder 100 caracteres')
        
        # Validar email
        email = datos.get('email', '').strip()
        if not email:
            errores.append('El email es obligatorio')
        elif not self._es_email_valido(email):
            errores.append('El formato del email no es válido')
        elif self._email_existe(email):
            errores.append('Ya existe una entrada con este email')
        
        # Validar teléfono (opcional)
        telefono = datos.get('telefono', '')
        if telefono and len(telefono.strip()) > 15:
            errores.append('El teléfono no puede exceder 15 caracteres')
        
        # Validar descripción (opcional)
        descripcion = datos.get('descripcion', '')
        if descripcion and len(descripcion.strip()) > 500:
            errores.append('La descripción no puede exceder 500 caracteres')
        
        return {
            'es_valido': len(errores) == 0,
            'errores': errores
        }
    
    def _es_email_valido(self, email):
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def _email_existe(self, email):
        """Verifica si el email ya existe"""
        email_lower = email.lower()
        return any(entrada.email == email_lower for entrada in self.entradas)
    
    def _entrada_a_dict(self, entrada):
        """Convierte objeto entrada a diccionario"""
        return {
            'id': entrada.id,
            'nombre': entrada.nombre,
            'email': entrada.email,
            'telefono': entrada.telefono,
            'descripcion': entrada.descripcion,
            'fecha_creacion': entrada.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _log_operacion(self, operacion, entrada):
        """Registra las operaciones realizadas"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{timestamp}] {operacion} - ID: {entrada.id}, Nombre: {entrada.nombre}, Email: {entrada.email}')
    
    def obtener_todas_las_entradas(self):
        """Obtiene todas las entradas registradas"""
        return {
            'exito': True,
            'total': len(self.entradas),
            'entradas': [self._entrada_a_dict(entrada) for entrada in self.entradas]
        }
    
    def obtener_entrada_por_id(self, entrada_id):
        """Obtiene una entrada específica por ID"""
        for entrada in self.entradas:
            if entrada.id == entrada_id:
                return {
                    'exito': True,
                    'entrada': self._entrada_a_dict(entrada)
                }
        
        return {
            'exito': False,
            'error': f'No se encontró entrada con ID {entrada_id}'
        }

# Función de utilidad para procesar datos del frontend
def procesar_datos_entrada(datos_formulario):
    """
    Función que procesaría los datos que vienen del frontend
    
    Args:
        datos_formulario (dict): Datos del formulario web
    
    Returns:
        dict: Respuesta para el frontend
    """
    controller = EntradaController()
    return controller.agregar_entrada(datos_formulario)

# Clase de servicio para operaciones más complejas
class EntradaService:
    """Servicio que encapsula la lógica de negocio"""
    
    def __init__(self):
        self.controller = EntradaController()
    
    def crear_entrada(self, datos):
        """Método principal del servicio para crear entradas"""
        # Aquí podrías añadir lógica adicional como:
        # - Notificaciones
        # - Auditoría
        # - Integración con otros sistemas
        
        resultado = self.controller.agregar_entrada(datos)
        
        if resultado['exito']:
            # Lógica post-creación
            self._procesar_post_creacion(resultado['datos'])
        
        return resultado
    
    def _procesar_post_creacion(self, entrada_datos):
        """Procesa acciones después de crear una entrada"""
        # Ejemplo: enviar notificación, actualizar estadísticas, etc.
        print(f"Post-procesamiento para entrada ID: {entrada_datos['id']}")