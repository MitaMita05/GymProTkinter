"""Titik masuk aplikasi: Gym Membership Management (Tkinter + SQLite).

Jalankan file INI:  python main.py
Akun login:         Mita, Ferdy, Rama, Tasya, Dosen  (password semua: 1234)
"""
import os
import sys

# Pastikan folder project masuk ke sys.path (aman dijalankan dari mana saja)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk

import theme
from database.db import init_db
from models import user_model
from views.auth_view import AuthView
from views.shell import MainShell


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Membership Management")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.configure(bg=theme.BG)
        theme.apply_style(self)
        self.screen = None
        self.show_login()

    def _set_screen(self, frame):
        if self.screen is not None:
            self.screen.destroy()
        self.screen = frame
        frame.pack(fill="both", expand=True)

    def show_login(self):
        self._set_screen(AuthView(self, on_login=self.show_main))

    def show_main(self, user):
        self._set_screen(MainShell(self, user, on_logout=self.show_login))


if __name__ == "__main__":
    init_db()
    user_model.sync_allowed_users()
    App().mainloop()
