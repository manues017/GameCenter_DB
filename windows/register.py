import tkinter as tk
from tkinter import ttk

from db import get_connection, register_user


class RegisterPage(tk.Frame):
    def __init__(self, master, on_register_success):
        """
        on_register_success: callback -> (user_id) => None
        """
        super().__init__(master)
        self.master = master
        self.on_register_success = on_register_success
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Register").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self, text="Username:").grid(row=1, column=0, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self, text="Email:").grid(row=2, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1)

        tk.Label(self, text="Password:").grid(row=3, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1)

        reg_btn = tk.Button(self, text="Crear Cuenta", command=self.attempt_register)
        reg_btn.grid(row=4, column=0, columnspan=2, pady=5)
    
    def attempt_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validar nombre
        if len(username) < 3:
            tk.messagebox.showerror("Error", "El nombre debe tener al menos 3 caracteres.")
            return

        # Validar email
        if '@' not in email or len(email.split('@')[0]) < 3 or len(email.split('@')[1]) < 3:
            tk.messagebox.showerror("Error", "El email debe tener un formato válido (al menos 3 caracteres antes y después del @).")
            return

        # Validar contraseña
        if len(password) < 4:
            tk.messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return

        conn = get_connection()
        try:
            user_id = register_user(conn, username, email, password)
            conn.close()
            tk.messagebox.showinfo("Registro Exitoso", f"Usuario {username} creado (ID={user_id}).")
            self.on_register_success(user_id)
        except Exception as e:
            conn.close()
            # Verificar si el error proviene de la restricción UNIQUE
            if "UNIQUE constraint failed: USUARIOS.nombre" in str(e):
                tk.messagebox.showerror("Error", "Este nombre de usuario ya está en uso. Por favor, elige otro.")
            else:
                tk.messagebox.showerror("Error", f"Error al crear el usuario: {str(e)}")

