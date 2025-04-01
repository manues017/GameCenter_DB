import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, get_friends_of_user,add_friend,user_exists_by_name,get_user_id_by_name

class FriendsPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.username = username
        self.on_back = on_back

        self.create_widgets()
        self.load_friends()

    def create_widgets(self):
        tk.Label(self, text=f"Amigos de {self.username}", font=("Arial", 14)).pack(pady=10)

        self.friends_frame = tk.Frame(self)
        self.friends_frame.pack(pady=5)

        # Campo para añadir amigo
        add_frame = tk.Frame(self)
        add_frame.pack(pady=5)

        tk.Label(add_frame, text="Añadir amigo (nombre):").pack(side="left")
        self.entry_friend = tk.Entry(add_frame)
        self.entry_friend.pack(side="left", padx=5)

        btn_add = tk.Button(add_frame, text="Añadir", command=self.add_new_friend)
        btn_add.pack(side="left")

        tk.Button(self, text="Volver", command=self.go_back).pack(pady=10)
        
    def go_back(self):
        self.on_back(self.user_id)

    def load_friends(self):
        # Limpia la lista de amigos
        for widget in self.friends_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        friends = get_friends_of_user(conn, self.user_id)  # Retorna [ {idUsuario, nombre}, ...]
        conn.close()

        if not friends:
            tk.Label(self.friends_frame, text="No tienes amigos añadidos.").pack()
        else:
            for f in friends:
                tk.Label(self.friends_frame, text=f"- {f['nombre']} (ID: {f['idUsuario']})").pack(anchor="w")

    def add_new_friend(self):
        friend_name = self.entry_friend.get().strip()
        if not friend_name:
            messagebox.showerror("Error", "Nombre vacío.")
            return

        conn = get_connection()
        # Verificar si existe
        if not user_exists_by_name(conn, friend_name):
            messagebox.showerror("Error", f"El usuario '{friend_name}' no existe.")
            conn.close()
            return

        friend_id = get_user_id_by_name(conn, friend_name)
        if friend_id == self.user_id:
            messagebox.showerror("Error", "No puedes añadirte a ti mismo.")
            conn.close()
            return

        try:
            add_friend(conn, self.user_id, friend_id)
            messagebox.showinfo("Amigo añadido", f"Has añadido a {friend_name} como amigo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir al amigo. {str(e)}")

        conn.close()
        self.entry_friend.delete(0, tk.END)
        self.load_friends()