import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os # Para verificar si el archivo de datos existe
import uuid # Para generar IDs únicos

class KanbanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablero Kanban de EstudiO JEREMY CARRASCO")
        self.root.geometry("1200x700") # Tamaño inicial de la ventana, un poco más grande

        self.data_file = "kanban_data.json"
        # Estructura de datos global para almacenar el tema, la materia actual y todas las materias
        self.data = {
            "current_theme": "light",
            "current_subject": "Materia por defecto",
            "subjects": {}
        }
        self.current_subject = self.data["current_subject"] # Variable de instancia para la materia actual

        self.timer_id = None # Para controlar el bucle del cronómetro
        self.timer_running = False
        self.time_left = 0
        self.COLUMNS = ["Por hacer", "Haciendo", "Hecho"]

        self.column_window_ids = {} # Diccionario para almacenar los IDs de las ventanas dentro de los canvas
        self.column_title_labels = {} # Diccionario para almacenar las etiquetas de título de las columnas

        # Definición de los temas con colores para el estilo de madera y papel
        self.themes = {
            "light": {
                "root_bg": "#F0F0F0", # Gris muy claro para el fondo principal
                "frame_bg": "#F0F0F0", # Gris muy claro para los frames de control
                "kanban_board_bg": "#8B4513", # Marrón oscuro (SaddleBrown) para el tablero de madera
                "column_bg": "#A0522D", # Marrón más claro (Sienna) para las columnas
                "canvas_bg": "#D2B48C", # Marrón claro (Tan) para el fondo del canvas
                "viewport_bg": "#D2B48C", # Igual que canvas_bg
                "label_fg": "black",
                "timer_fg": "blue",
                "button_bg": "#E0E0E0", # Gris claro para botones
                "button_fg": "black",
                "entry_bg": "white",
                "entry_fg": "black",
                "topic_paper_bg": "#FFF8DC", # Blanco cremoso (Cornsilk) para notas de papel
                "topic_frame_bg_green": "#90EE90", # Verde claro
                "topic_frame_bg_yellow": "#FFFFE0", # Amarillo muy claro
                "topic_frame_bg_red": "#FFB6C1", # Rosa claro
                "topic_label_fg": "black",
                "subject_label_fg": "white" # Color del texto del título de la materia
            },
            "dark": {
                "root_bg": "#2e2e2e", # Gris oscuro para el fondo principal
                "frame_bg": "#3c3c3c", # Gris un poco más claro para los frames de control
                "kanban_board_bg": "#362417", # Marrón muy oscuro para el tablero de madera
                "column_bg": "#4A3226", # Marrón oscuro para las columnas
                "canvas_bg": "#5C4033", # Marrón medio para el fondo del canvas
                "viewport_bg": "#5C4033", # Igual que canvas_bg
                "label_fg": "white",
                "timer_fg": "#88eeff", # Azul claro/cian
                "button_bg": "#5a5a5a", # Gris oscuro para botones
                "button_fg": "white",
                "entry_bg": "#6a6a6a",
                "entry_fg": "white",
                "topic_paper_bg": "#D4CFC7", # Gris claro desaturado para notas de papel en modo oscuro
                "topic_frame_bg_green": "#228B22", # Verde oscuro
                "topic_frame_bg_yellow": "#FFD700", # Oro
                "topic_frame_bg_red": "#B22222", # Rojo ladrillo
                "topic_label_fg": "black", # Texto negro sobre papel claro en modo oscuro
                "subject_label_fg": "white" # Color del texto del título de la materia
            }
        }

        self.load_data() # Cargar datos al iniciar la aplicación (incluye el tema)
        self.current_theme = self.data["current_theme"] # Establecer el tema desde los datos cargados
        self.current_subject = self.data["current_subject"] # Establecer la materia actual desde los datos cargados

        self.setup_ui()
        self.apply_theme_colors() # Aplicar el tema inicial después de configurar la UI
        self.display_topics() # Mostrar los temas de la materia actual

    def load_data(self):
        """Carga los datos del tablero Kanban desde un archivo JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                    # Manejar formato antiguo (solo materias) o formato nuevo
                    if "subjects" not in loaded_data:
                        self.data["subjects"] = loaded_data # Formato antiguo, asume que es solo el diccionario de materias
                        self.data["current_theme"] = "light" # Tema por defecto para datos antiguos
                        self.data["current_subject"] = "Materia por defecto" # Materia por defecto para datos antiguos
                    else:
                        self.data = loaded_data

                # Paso de Migración: Convertir temas antiguos a formato con ID único y asegurar color
                for subject_name, columns_data in self.data["subjects"].items():
                    for col_name in self.COLUMNS:
                        if col_name in columns_data:
                            converted_topics = []
                            for item in columns_data[col_name]:
                                if isinstance(item, str): # Si es un tema antiguo (solo string)
                                    converted_topics.append({"id": uuid.uuid4().hex, "text": item, "color": "white"})
                                else: # Asumir que ya está en el nuevo formato de diccionario
                                    if "color" not in item: # Asegurar que los temas existentes tengan color
                                        item["color"] = "white"
                                    converted_topics.append(item)
                            columns_data[col_name] = converted_topics
                
                # Asegurarse de que la materia actual sea válida
                if not self.data["subjects"]:
                    self._initialize_default_data() # Inicializa self.data completamente
                elif self.data["current_subject"] not in self.data["subjects"]:
                    # Si la materia actual guardada no existe, selecciona la primera disponible
                    self.data["current_subject"] = list(self.data["subjects"].keys())[0]

            except json.JSONDecodeError:
                messagebox.showerror("Error de Carga", "El archivo de datos está corrupto. Se creará uno nuevo.")
                self._initialize_default_data() # Inicializa todos los datos por defecto
        else:
            self._initialize_default_data() # Inicializa todos los datos por defecto si el archivo no existe

    def _initialize_default_data(self):
        """Inicializa la estructura de datos completa con una materia por defecto."""
        self.data = {
            "current_theme": "light",
            "current_subject": "Materia por defecto",
            "subjects": {
                "Materia por defecto": {
                    "Por hacer": [],
                    "Haciendo": [],
                    "Hecho": []
                }
            }
        }
        self.save_data() # Guardar la estructura por defecto inmediatamente

    def save_data(self):
        """Guarda los datos actuales del tablero Kanban en un archivo JSON."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            # messagebox.showinfo("Guardado", "Datos guardados exitosamente.")
        except IOError as e:
            messagebox.showerror("Error de Guardado", f"No se pudo guardar el archivo: {e}")

    def setup_ui(self):
        """Configura la interfaz de usuario de la aplicación."""
        # --- Barra de Menú ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modo", menu=mode_menu)
        mode_menu.add_command(label="Claro", command=lambda: self.set_theme("light"))
        mode_menu.add_command(label="Oscuro", command=lambda: self.set_theme("dark"))

        # --- Sección de Gestión de Materias y Guardado ---
        self.top_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        self.top_frame.pack(pady=10, fill="x")

        # Dropdown para seleccionar materias
        tk.Label(self.top_frame, text="Materia:").pack(side=tk.LEFT, padx=5)
        self.subject_var = tk.StringVar(self.root)
        self.subject_var.set(self.current_subject) # Establecer la materia actual
        
        self.subject_option_menu = tk.OptionMenu(self.top_frame, self.subject_var, *self.data["subjects"].keys(), command=self.change_subject)
        self.subject_option_menu.pack(side=tk.LEFT, padx=5)

        # Botones para gestionar materias
        add_subject_button = tk.Button(self.top_frame, text="Añadir Materia", command=self.add_subject)
        add_subject_button.pack(side=tk.LEFT, padx=5)

        delete_subject_button = tk.Button(self.top_frame, text="Eliminar Materia", command=self.delete_subject)
        delete_subject_button.pack(side=tk.LEFT, padx=5)

        # Botón de guardar
        save_button = tk.Button(self.top_frame, text="Guardar Cambios", command=self.save_data)
        save_button.pack(side=tk.RIGHT, padx=5)

        # --- Etiqueta del Nombre de la Materia ---
        self.subject_display_label = tk.Label(self.root, text=self.current_subject, font=("Arial", 20, "bold"))
        self.subject_display_label.pack(pady=(10, 5)) # Un poco de padding arriba y abajo

        # --- Sección de Input para Añadir Temas ---
        self.input_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        self.input_frame.pack(pady=10, fill="x")

        tk.Label(self.input_frame, text="Nuevo Tema:").pack(side=tk.LEFT, padx=5)
        self.new_topic_entry = tk.Entry(self.input_frame, width=60)
        self.new_topic_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
        self.new_topic_entry.bind("<Return>", self.add_topic_from_enter)

        add_button = tk.Button(self.input_frame, text="Añadir Tema", command=self.add_topic)
        add_button.pack(side=tk.LEFT, padx=5)

        # --- Sección del Tablero Kanban ---
        self.kanban_frame = tk.Frame(self.root, bd=2, relief="raised", padx=10, pady=10) # Borde elevado para el tablero
        self.kanban_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.column_frames = {}
        self.column_canvases = {}
        self.column_viewports = {}

        for i, col_name in enumerate(self.COLUMNS):
            column_frame = tk.Frame(self.kanban_frame, bd=2, relief="ridge", padx=5, pady=5)
            column_frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            self.kanban_frame.grid_columnconfigure(i, weight=1)

            # Guardar la referencia a la etiqueta del título de la columna
            column_title_label = tk.Label(column_frame, text=col_name, font=("Arial", 14, "bold"))
            column_title_label.pack(pady=5)
            self.column_title_labels[col_name] = column_title_label # Guardar la referencia

            canvas = tk.Canvas(column_frame, highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(column_frame, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))

            viewport_frame = tk.Frame(canvas)
            # Almacenar el ID de la ventana creada dentro del canvas
            window_id = canvas.create_window((0, 0), window=viewport_frame, anchor="nw", width=canvas.winfo_width())
            self.column_window_ids[col_name] = window_id # Guardar el ID para referencia futura

            # Actualizar el ancho del viewport_frame cuando el canvas cambie de tamaño
            # Usar el ID de la ventana en lugar de winfo_children()[0]
            canvas.bind('<Configure>', lambda e, c=canvas, wid=window_id: c.itemconfigure(wid, width=e.width))

            self.column_frames[col_name] = viewport_frame
            self.column_canvases[col_name] = canvas
            self.column_viewports[col_name] = viewport_frame

            self.root.bind("<Configure>", self.on_resize)

        self.root.grid_rowconfigure(0, weight=1)

        # --- Sección de Temporizadores ---
        self.timer_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        self.timer_frame.pack(pady=10, fill="x")

        self.timer_label = tk.Label(self.timer_frame, text="00:00", font=("Arial", 24, "bold"))
        self.timer_label.pack(side=tk.LEFT, padx=20)

        study_button = tk.Button(self.timer_frame, text="Estudiar (30 min)", command=lambda: self.start_timer(30 * 60))
        study_button.pack(side=tk.LEFT, padx=10)

        break_button = tk.Button(self.timer_frame, text="Descanso (15 min)", command=lambda: self.start_timer(15 * 60))
        break_button.pack(side=tk.LEFT, padx=10)

        stop_timer_button = tk.Button(self.timer_frame, text="Detener Temporizador", command=self.stop_timer)
        stop_timer_button.pack(side=tk.LEFT, padx=10)

    def apply_theme_colors(self):
        """Aplica los colores del tema actual a todos los widgets de la UI."""
        current_theme_colors = self.themes[self.current_theme]

        # Root y frames principales
        self.root.config(bg=current_theme_colors["root_bg"])
        self.top_frame.config(bg=current_theme_colors["frame_bg"])
        self.input_frame.config(bg=current_theme_colors["frame_bg"])
        self.timer_frame.config(bg=current_theme_colors["frame_bg"])

        # Kanban board background
        self.kanban_frame.config(bg=current_theme_colors["kanban_board_bg"])

        # Labels generales (Materia, Nuevo Tema)
        for widget in self.top_frame.winfo_children() + self.input_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(fg=current_theme_colors["label_fg"], bg=current_theme_colors["frame_bg"])
        
        # Etiqueta del nombre de la materia
        self.subject_display_label.config(bg=current_theme_colors["kanban_board_bg"], fg=current_theme_colors["subject_label_fg"])
        
        self.timer_label.config(fg=current_theme_colors["timer_fg"], bg=current_theme_colors["frame_bg"])

        # Entry
        self.new_topic_entry.config(bg=current_theme_colors["entry_bg"], fg=current_theme_colors["entry_fg"])

        # Buttons (general)
        for widget in self.top_frame.winfo_children() + self.input_frame.winfo_children() + self.timer_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=current_theme_colors["button_bg"], fg=current_theme_colors["button_fg"])
        
        # OptionMenu (dropdown de materias)
        self.subject_option_menu.config(bg=current_theme_colors["button_bg"], fg=current_theme_colors["button_fg"])
        # Asegurarse de que el menú desplegable también tenga los colores correctos
        if self.subject_option_menu["menu"]:
            self.subject_option_menu["menu"].config(bg=current_theme_colors["button_bg"], fg=current_theme_colors["button_fg"])


        # Columnas Kanban y Canvas
        for col_name in self.COLUMNS:
            column_frame = self.column_frames[col_name].master # Obtener el Frame padre del viewport_frame
            column_frame.config(bg=current_theme_colors["column_bg"])
            # Usar la referencia guardada para la etiqueta del título de la columna
            if col_name in self.column_title_labels:
                self.column_title_labels[col_name].config(bg=current_theme_colors["column_bg"], fg=current_theme_colors["label_fg"])
            
            canvas = self.column_canvases[col_name]
            canvas.config(bg=current_theme_colors["canvas_bg"])
            
            viewport_frame = self.column_viewports[col_name]
            viewport_frame.config(bg=current_theme_colors["viewport_bg"])
            # Re-asociar la ventana para asegurar que el color de fondo del viewport se actualice
            canvas.itemconfigure(self.column_window_ids[col_name], window=viewport_frame) 

        # Volver a mostrar los temas para aplicar los nuevos colores a los items de tema
        self.display_topics()

    def set_theme(self, theme_name):
        """Establece el tema de la aplicación (claro u oscuro)."""
        self.current_theme = theme_name
        self.apply_theme_colors()
        self.data["current_theme"] = self.current_theme # Actualizar en los datos
        self.save_data() # Guardar la preferencia de tema

    def on_resize(self, event):
        """Ajusta el ancho de los viewports de las columnas cuando la ventana se redimensiona."""
        for col_name, canvas in self.column_canvases.items():
            window_id = self.column_window_ids.get(col_name) # Obtener el ID de la ventana
            if window_id: # Asegurarse de que el ID existe
                canvas.itemconfigure(window_id, width=canvas.winfo_width())
            canvas.configure(scrollregion=canvas.bbox("all"))

    def add_topic_from_enter(self, event):
        """Añade un tema cuando se presiona Enter en el campo de entrada."""
        self.add_topic()

    def add_topic(self):
        """Añade un nuevo tema a la columna 'Por hacer' de la materia actual."""
        topic_text = self.new_topic_entry.get().strip()
        if topic_text:
            # Almacenar el tema como un diccionario con un ID único y color por defecto
            self.data["subjects"][self.current_subject]["Por hacer"].append({"id": uuid.uuid4().hex, "text": topic_text, "color": "white"})
            self.new_topic_entry.delete(0, tk.END)
            self.display_topics()
            self.save_data() # Guardar automáticamente al añadir
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un tema.")

    def display_topics(self):
        """Muestra los temas en sus respectivas columnas para la materia actual."""
        # Actualizar la etiqueta del nombre de la materia
        self.subject_display_label.config(text=self.current_subject)

        # Limpiar los frames de las columnas antes de redibujar
        for col_name in self.column_frames:
            for widget in self.column_frames[col_name].winfo_children():
                widget.destroy()

        current_topics = self.data["subjects"][self.current_subject]
        current_theme_colors = self.themes[self.current_theme]

        # Mostrar los temas en sus respectivas columnas
        for col_index, col_name in enumerate(self.COLUMNS):
            for topic_data in current_topics[col_name]: # topic_data es ahora un diccionario
                topic_text = topic_data["text"] # Extraer el texto para mostrar
                topic_id = topic_data["id"] # Extraer el ID para operaciones
                topic_color_key = topic_data.get("color", "white") # Extraer el color, por defecto blanco

                # Determinar el color de fondo del tema para el item del tema
                # Usar el color de papel por defecto, y luego aplicar el color de dificultad si existe
                topic_bg_color = current_theme_colors["topic_paper_bg"]
                if topic_color_key == "green":
                    topic_bg_color = current_theme_colors["topic_frame_bg_green"]
                elif topic_color_key == "yellow":
                    topic_bg_color = current_theme_colors["topic_frame_bg_yellow"]
                elif topic_color_key == "red":
                    topic_bg_color = current_theme_colors["topic_frame_bg_red"]

                # Frame para cada tema con sus botones
                topic_item_frame = tk.Frame(self.column_frames[col_name], bg=topic_bg_color, relief="solid", bd=1)
                topic_item_frame.pack(fill="x", padx=5, pady=2)

                # Botón para mover a la izquierda
                if col_index > 0:
                    # Capturar el índice de la columna anterior en la lambda
                    move_left_button = tk.Button(topic_item_frame, text="<", width=2,
                                                 command=lambda tid=topic_id, c=col_name, prev_idx=col_index - 1: self.move_topic(tid, c, self.COLUMNS[prev_idx]),
                                                 bg=current_theme_colors["button_bg"], fg=current_theme_colors["button_fg"])
                    move_left_button.pack(side=tk.LEFT, padx=(0, 2))

                # Etiqueta del tema
                topic_label = tk.Label(topic_item_frame, text=topic_text, bg=topic_bg_color, fg=current_theme_colors["topic_label_fg"], padx=5, pady=5)
                topic_label.pack(side=tk.LEFT, expand=True, fill="x")
                # Bind right-click to show context menu for color selection
                topic_label.bind("<Button-3>", lambda event, tid=topic_id: self.show_color_context_menu(event, tid))


                # Botón para mover a la derecha
                if col_index < len(self.COLUMNS) - 1:
                    # Capturar el índice de la columna siguiente en la lambda
                    move_right_button = tk.Button(topic_item_frame, text=">", width=2,
                                                  command=lambda tid=topic_id, c=col_name, next_idx=col_index + 1: self.move_topic(tid, c, self.COLUMNS[next_idx]),
                                                  bg=current_theme_colors["button_bg"], fg=current_theme_colors["button_fg"])
                    move_right_button.pack(side=tk.RIGHT, padx=(2, 0))
                
                # Botón para eliminar el tema
                delete_topic_button = tk.Button(topic_item_frame, text="X", fg="red", width=2,
                                                command=lambda tid=topic_id, c=col_name: self.delete_topic(tid, c),
                                                bg=current_theme_colors["button_bg"]) # El color del texto 'X' es fijo rojo
                delete_topic_button.pack(side=tk.RIGHT, padx=(2, 0))


            # Actualizar el scrollregion del canvas después de añadir los temas
            self.column_canvases[col_name].update_idletasks()
            self.column_canvases[col_name].configure(scrollregion=self.column_canvases[col_name].bbox("all"))

    def show_color_context_menu(self, event, topic_id):
        """Muestra el menú contextual para cambiar el color de un tema."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Fácil (Verde)", command=lambda: self.change_topic_color(topic_id, "green"))
        menu.add_command(label="Medio (Amarillo)", command=lambda: self.change_topic_color(topic_id, "yellow"))
        menu.add_command(label="Difícil (Rojo)", command=lambda: self.change_topic_color(topic_id, "red"))
        menu.add_separator()
        menu.add_command(label="Sin color", command=lambda: self.change_topic_color(topic_id, "white"))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def change_topic_color(self, topic_id, new_color):
        """Cambia el color de un tema específico y actualiza la UI."""
        found = False
        for col_name in self.COLUMNS:
            for topic_data in self.data["subjects"][self.current_subject][col_name]:
                if topic_data["id"] == topic_id:
                    topic_data["color"] = new_color
                    found = True
                    break
            if found:
                break
        
        if found:
            self.display_topics()
            self.save_data()
        else:
            print(f"Error: Tema con ID '{topic_id}' no encontrado para cambiar color.")


    def move_topic(self, topic_id, from_column, to_column):
        """Mueve un tema de una columna a otra utilizando su ID único."""
        print(f"Solicitud de movimiento: topic_id='{topic_id}', de='{from_column}', a='{to_column}'")
        topic_to_move = None
        current_column_list = self.data["subjects"][self.current_subject][from_column]
        target_column_list = self.data["subjects"][self.current_subject][to_column]

        found_index = -1
        for i, topic_data in enumerate(current_column_list):
            if topic_data["id"] == topic_id:
                topic_to_move = topic_data
                found_index = i
                break
        
        if topic_to_move:
            current_column_list.pop(found_index) # Eliminar por índice
            target_column_list.append(topic_to_move)
            print(f"Tema '{topic_to_move['text']}' movido exitosamente.")
            self.display_topics()
            self.save_data() # Guardar automáticamente al mover
        else:
            print(f"Error: Tema con ID '{topic_id}' no encontrado en '{from_column}'.")

    def delete_topic(self, topic_id, from_column):
        """Elimina un tema de una columna utilizando su ID único."""
        print(f"Solicitud de eliminación: topic_id='{topic_id}', de='{from_column}'")
        topic_to_delete_text = ""
        current_column_list = self.data["subjects"][self.current_subject][from_column]
        
        # Encontrar el texto del tema para el mensaje de confirmación
        for topic_data in current_column_list:
            if topic_data["id"] == topic_id:
                topic_to_delete_text = topic_data["text"]
                break

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar '{topic_to_delete_text}'?"):
            # Eliminar el tema por su ID
            found_index = -1
            for i, topic_data in enumerate(current_column_list):
                if topic_data["id"] == topic_id:
                    found_index = i
                    break
            
            if found_index != -1:
                current_column_list.pop(found_index) # Eliminar por índice
                print(f"Tema '{topic_to_delete_text}' eliminado exitosamente.")
            else:
                print(f"Error: Tema con ID '{topic_id}' no encontrado en '{from_column}' para eliminar.")
            
            self.display_topics()
            self.save_data() # Guardar automáticamente al eliminar

    def update_subject_option_menu(self):
        """Actualiza el menú desplegable de materias con las materias actuales."""
        self.subject_option_menu['menu'].delete(0, 'end')
        # Asegurarse de que el menú se actualice incluso si no hay materias (aunque debería haber al menos una)
        if not self.data["subjects"]:
            self._initialize_default_data() # Re-inicializar si por alguna razón se vació
        
        for subject in self.data["subjects"].keys():
            self.subject_option_menu['menu'].add_command(label=subject, command=tk._setit(self.subject_var, subject, self.change_subject))
        self.subject_var.set(self.current_subject) # Asegurarse de que el valor mostrado es el actual

    def add_subject(self):
        """Añade una nueva materia."""
        new_subject_name = simpledialog.askstring("Nueva Materia", "Ingresa el nombre de la nueva materia:")
        if new_subject_name: # Asegurarse de que el usuario ingresó algo
            new_subject_name = new_subject_name.strip()
            if new_subject_name not in self.data["subjects"]:
                self.data["subjects"][new_subject_name] = {
                    "Por hacer": [],
                    "Haciendo": [],
                    "Hecho": []
                }
                self.data["current_subject"] = new_subject_name
                self.current_subject = new_subject_name
                self.update_subject_option_menu()
                self.display_topics()
                self.save_data()
            else:
                messagebox.showwarning("Advertencia", "Esa materia ya existe.")

    def delete_subject(self):
        """Elimina la materia actualmente seleccionada."""
        if len(self.data["subjects"]) == 1:
            messagebox.showwarning("Advertencia", "No puedes eliminar la única materia.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar la materia '{self.current_subject}' y todos sus temas?"):
            del self.data["subjects"][self.current_subject]
            # Seleccionar la primera materia restante como la nueva materia actual
            self.data["current_subject"] = list(self.data["subjects"].keys())[0]
            self.current_subject = self.data["current_subject"] # Actualizar la variable de instancia
            self.subject_var.set(self.current_subject) # Actualizar el StringVar
            self.update_subject_option_menu()
            self.display_topics()
            self.save_data()

    def change_subject(self, new_subject):
        """Cambia a la materia seleccionada y actualiza el tablero."""
        self.data["current_subject"] = new_subject
        self.current_subject = new_subject
        self.display_topics()
        self.save_data() # Guardar el cambio de materia

    def start_timer(self, duration_seconds):
        """Inicia el cronómetro con la duración especificada."""
        if self.timer_running:
            self.stop_timer() # Detener el cronómetro anterior si está corriendo

        self.time_left = duration_seconds
        self.timer_running = True
        self.update_timer_display()
        self.countdown()

    def countdown(self):
        """Función recursiva para el cronómetro."""
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_id = self.root.after(1000, self.countdown) # Llamarse a sí misma después de 1 segundo
        elif self.time_left <= 0 and self.timer_running:
            self.timer_running = False
            self.timer_label.config(text="¡Tiempo!")
            messagebox.showinfo("Temporizador", "¡Tiempo terminado!")
            self.stop_timer() # Asegurarse de detener el after()

    def stop_timer(self):
        """Detiene el cronómetro."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        self.timer_label.config(text="00:00") # Resetear el display

    def update_timer_display(self):
        """Actualiza la etiqueta del cronómetro con el tiempo restante."""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)


if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanApp(root)
    root.mainloop()