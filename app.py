import tkinter as tk
from tkinter import ttk, messagebox

from windows.login import LoginPage
from windows.friends import FriendsPage
from windows.home import HomePage
from windows.library import LibraryPage
from windows.register import RegisterPage
from windows.store import StorePage
"""
La clase App gestiona todas las distintas paginas de la aplicacion:

Se encarga de mostrar la ventana ("page") indicada.
"""
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini-Steam con Interfaz Gráfica")

        # Iniciamos mostrando la página de Login
        self.current_frame = None
        self.show_login_page()

    def show_login_page(self):
        # Destruir frame anterior si existe
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = LoginPage(self, on_login_success=self.on_login_success, 
                                            on_go_register=self.show_register_page)
        self.current_frame.pack()

    def show_register_page(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = RegisterPage(self, on_register_success=self.on_register_success)
        self.current_frame.pack()

    def on_login_success(self, user_id):
        # Una vez logueado, mostramos el home
        self.show_home_page(user_id)

    def on_register_success(self, user_id):
        # Tras registrarse, llevamos al Home
        self.show_home_page(user_id)

    def show_home_page(self, user_id):
        #Muestra la página principal una vez el usuario ha iniciado sesion
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = HomePage(self, user_id, on_logout=self.logout)
        self.current_frame.pack()

        
    def show_library_page(self, user_id, username):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LibraryPage(self, user_id, username, on_back=self.show_home_page)
        self.current_frame.pack()

    def show_store_page(self, user_id, username):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StorePage(self, user_id, username, on_back=self.show_home_page)
        self.current_frame.pack()

    def show_friends_page(self, user_id, username):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FriendsPage(self, user_id, username, on_back=self.show_home_page)
        self.current_frame.pack()

    def logout(self):
        # Regresamos al login
        self.show_login_page()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
