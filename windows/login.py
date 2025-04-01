import tkinter as tk
from tkinter import ttk, messagebox

from db import get_connection, get_user_login

class LoginPage(tk.Frame):
    def __init__(self, master, on_login_success, on_go_register):
        """
        master: la ventana raíz
        on_login_success: callback -> (user_id) => None
        on_go_register: callback para ir a la página de registro
        """
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.on_go_register = on_go_register
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self, text="Username:").grid(row=1, column=0, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self, text="Password:").grid(row=2, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1)

        login_btn = tk.Button(self, text="Login", command=self.attempt_login)
        login_btn.grid(row=3, column=0, pady=5)

        register_btn = tk.Button(self, text="Register", command=self.on_go_register)
        register_btn.grid(row=3, column=1, pady=5)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = get_connection()
        user = get_user_login(conn, username, password)
        conn.close()

        if user:
            # Llamamos al callback y pasamos el idUsuario
            self.on_login_success(user["idUsuario"])
        else:
            tk.messagebox.showerror("Error", "Credenciales inválidas")
            
