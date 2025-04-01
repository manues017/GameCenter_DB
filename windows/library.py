import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, get_biblioteca_by_user, remove_game_from_library

class LibraryPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.username = username
        self.on_back = on_back

        self.create_widgets()
        self.load_library()

    def create_widgets(self):
        tk.Label(self, text=f"Biblioteca de {self.username}", font=("Arial", 14)).pack(pady=10)

        # Contenedor donde mostrar los juegos
        self.library_frame = tk.Frame(self)
        self.library_frame.pack(pady=5)

        tk.Button(self, text="Volver", command=self.go_back).pack(pady=10)
        
    def go_back(self):
        self.on_back(self.user_id)
        
    def remove_game(self, juego_id):
        # Llamar a la función en db.py
        conn = get_connection()
        try:
            remove_game_from_library(conn, self.user_id, juego_id)
            messagebox.showinfo("Eliminado", "Juego eliminado de tu biblioteca.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el juego: {str(e)}")
        conn.close()

        # Recargar la biblioteca
        self.load_library()
 

    def load_library(self):
        for widget in self.library_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        juegos = get_biblioteca_by_user(conn, self.user_id)
        conn.close()

        if not juegos:
            tk.Label(self.library_frame, text="No tienes juegos en tu biblioteca.").pack()
        else:
            for j in juegos:
                juego_id = j["idJuego"]
                titulo = j["titulo"]
                fecha = j["fechaCompra"] or "N/A"

                frm_juego = tk.Frame(self.library_frame)
                frm_juego.pack(fill="x", pady=2)

                # Etiqueta con info
                lbl_info = tk.Label(frm_juego, text=f"{titulo} (Comprado el {fecha})")
                lbl_info.pack(side="left")

                # Botón "Eliminar"
                btn_remove = tk.Button(
                    frm_juego,
                    text="Eliminar",
                    command=lambda jID=juego_id: self.remove_game(jID)
                )
                btn_remove.pack(side="right", padx=5)
            
