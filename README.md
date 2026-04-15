# Tablero Kanban - EstudiO JEREMY CARRASCO

Una aplicación de escritorio para gestión de tareas mediante el método Kanban, desarrollada con Python y Tkinter.

## Características

- **Gestión de Materias**: Organiza tus tareas por diferentes materias o proyectos
- **Tablero Kanban**: Tres columnas clásicas (Por hacer, Haciendo, Hecho)
- **Temas Personalizables**: Modo claro y oscuro con estilo de madera y papel
- **Cronómetro Integrado**: Temporizador Pomodoro para mejorar la productividad
- **Persistencia de Datos**: Guarda automáticamente tu progreso en formato JSON
- **Notas Adhesivas**: Tarjetas de colores para organizar tus tareas visualmente

## Requisitos

- Python 3.x
- Tkinter (generalmente incluido con Python)

## Instalación

1. Clona o descarga este repositorio
2. Asegúrate de tener Python 3 instalado
3. Ejecuta la aplicación directamente:

```bash
python kanba.py
```

## Uso

### Primeros Pasos

1. Al iniciar, la aplicación cargará automáticamente los datos guardados previamente
2. El tablero mostrará las tareas de la materia actualmente seleccionada

### Gestión de Materias

- Usa el selector de materias en la parte superior para cambiar entre diferentes materias/proyectos
- Crea nuevas materias desde el menú de control
- Cada materia mantiene su propio conjunto de tareas independientes

### Gestionar Tareas

1. **Agregar Tarea**: 
   - Haz clic en "Agregar Tarea" o usa el botón correspondiente
   - Ingresa el nombre de la tarea y selecciona una categoría/color
   
2. **Mover Tareas**:
   - Arrastra las tarjetas entre columnas para actualizar su estado
   - Columnas disponibles: "Por hacer" → "Haciendo" → "Hecho"

3. **Editar/Eliminar Tareas**:
   - Haz doble clic en una tarjeta para editarla
   - Usa el menú contextual (clic derecho) para eliminar tareas

### Cronómetro Pomodoro

- Configura el temporizador desde el panel de control
- Ideal para sesiones de estudio enfocadas
- Recibe una notificación cuando el tiempo termine

### Temas

- Cambia entre modo claro y oscuro desde el menú de configuración
- El tema seleccionado se guarda automáticamente
- Diseño inspirado en madera (tablero) y papel (tarjetas)

## Estructura de Datos

La aplicación guarda toda la información en `kanban_data.json` con la siguiente estructura:

```json
{
  "current_theme": "light",
  "current_subject": "Materia por defecto",
  "subjects": {
    "Nombre Materia": {
      "Por hacer": [...],
      "Haciendo": [...],
      "Hecho": [...]
    }
  }
}
```

## Archivos

- `kanba.py`: Código principal de la aplicación
- `kanban_data.json`: Archivo de persistencia de datos (generado automáticamente)

## Capturas de Pantalla

La aplicación presenta:
- Interfaz con estilo de tablero de madera
- Columnas con fondo marrón claro
- Tarjetas tipo nota adhesiva en colores (verde, amarillo, rosa)
- Panel de control superior con selector de materias y cronómetro

## Desarrollo

La aplicación está construida con:
- **Tkinter**: Para la interfaz gráfica
- **JSON**: Para almacenamiento de datos
- **UUID**: Para identificación única de tareas
- **Programación Orientada a Objetos**: Estructura modular y mantenible

## Autor

Desarrollado por **EstudiO JEREMY CARRASCO**

## Licencia

Este proyecto es de uso libre para fines educativos y personales.

---

¡Organiza tus tareas y mejora tu productividad con este tablero Kanban! 📋✅
