import tkinter as tk
from tkinter import ttk
from db import get_connection, get_username_by_id


class HomePage(tk.Frame):
    def __init__(self, master, user_id, on_logout):
        super().__init__(master)
        
        self.master = master
        self.user_id = user_id
        self.on_logout = on_logout
        
        # Obtener el nombre del usuario desde la base de datos
        conn = get_connection()
        self.username = get_username_by_id(conn, user_id)
        conn.close()
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Bienvenido, {self.username}!", font=("Arial", 14)).pack(pady=10)

        tk.Button(self, text="Biblioteca", command=self.go_library).pack(pady=5)
        tk.Button(self, text="Tienda", command=self.go_store).pack(pady=5)
        tk.Button(self, text="Amigos", command=self.go_friends).pack(pady=5)

        tk.Button(self, text="Cerrar Sesión", command=self.on_logout).pack(pady=20)

    def go_library(self):
        self.master.show_library_page(self.user_id, self.username)

    def go_store(self):
        self.master.show_store_page(self.user_id, self.username)

    def go_friends(self):
        self.master.show_friends_page(self.user_id, self.username)

    def show(self):
        self.pack()  # Muestra de nuevo el Frame actual
