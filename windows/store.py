import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, search_games, buy_game, get_all_generos

class StorePage(tk.Frame):
    def __init__(self, master, user_id, username, on_back):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.username = username
        self.on_back = on_back

        # Variables para filtro
        self.search_var = tk.StringVar()
        self.selected_genre_id = tk.IntVar(value=0)  # 0 -> sin género
        self.create_widgets()
        self.load_genres()
        self.load_store()

    def create_widgets(self):
        tk.Label(self, text="Tienda de Juegos", font=("Arial", 14)).pack(pady=10)

        # Frame para filtros
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)
        
        #Barra de busqueda de videojuegos
        tk.Label(filter_frame, text="Buscar Título:").pack(side="left")
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side="left", padx=5)

        #Boton para filtrar los juegos de la tienda por genero
        tk.Label(filter_frame, text="Género:").pack(side="left", padx=5)
        self.genre_combo = ttk.Combobox(filter_frame, state="readonly")
        self.genre_combo.pack(side="left")

        # Botón filtrar
        tk.Button(filter_frame, text="Filtrar", command=self.apply_filters).pack(side="left", padx=5)

        # Frame para la lista de juegos
        self.store_frame = tk.Frame(self)
        self.store_frame.pack(pady=5)

        tk.Button(self, text="Volver", command=self.go_back).pack(pady=10)

    # Permite volver a la pagina anterior
    def go_back(self):
        self.on_back(self.user_id)

    def load_genres(self):
        """
        Carga la lista de géneros (idGenero, nombre)
        """
        conn = get_connection()
        generos = get_all_generos(conn) 
        conn.close()

        # Insertar 'Todos' al inicio
        genre_names = ["Todos"]
        self.genre_map = {0: "Todos"}  # Mapa idGenero -> nombre

        for g in generos:
            gid = g["idGenero"]
            gname = g["nombre"]
            genre_names.append(gname)
            self.genre_map[gid] = gname

        self.genre_combo["values"] = genre_names
        self.genre_combo.current(0)  # Seleccionar "Todos" por defecto

    def apply_filters(self):
        # Al pulsar "Filtrar"
        text = self.search_var.get().strip()

        # Ver cuál index se seleccionó
        index = self.genre_combo.current()
        # Recuperar idGenero a partir del index
        # El primer valor (index=0) es "Todos" (id=0)
        # El segundo valor (index=1) es el primer género real, etc.
        # Mapear index -> key en self.genre_map
        # Podemos re-crear el mapping con un array, o hacerlo con un loop.

        # Ejemplo: reconstruimos en orden
        possible_ids = list(self.genre_map.keys())  # [0, 1, 2, ...]
        if index < len(possible_ids):
            selected_id = possible_ids[index]
        else:
            selected_id = 0

        self.load_store(search_text=text, genre_id=selected_id)

    def load_store(self, search_text=None, genre_id=None):
        # Limpia el frame antes de añadir contenido
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        # Usamos la nueva función con filtros
        juegos = search_games(conn, search_text=search_text, genero_id=genre_id, limit=15)
        conn.close()

        if not juegos:
            tk.Label(self.store_frame, text="No hay juegos que coincidan con el filtro.").pack()
        else:
            for j in juegos:
                juego_id = j["idJuego"]
                titulo = j["titulo"]
                precio = j["precio"]
                frm_juego = tk.Frame(self.store_frame)
                frm_juego.pack(fill="x", pady=2)

                lbl_info = tk.Label(frm_juego, text=f"{titulo} - ${precio}")
                lbl_info.pack(side="left")

                btn_buy = tk.Button(frm_juego, text="Comprar", 
                                    command=lambda idJ=juego_id: self.buy_game(idJ))
                btn_buy.pack(side="right", padx=5)

    def buy_game(self, juego_id):
        conn = get_connection()
        try:
            buy_game(conn, self.user_id, juego_id)
            messagebox.showinfo("Compra Exitosa", "¡Juego agregado a tu biblioteca!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo comprar el juego. {str(e)}")
        conn.close()

        # Refrescar la lista con los mismos filtros
        self.apply_filters()
