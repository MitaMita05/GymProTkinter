"""Kerangka aplikasi setelah login: header berwarna + tab (Notebook)."""
import tkinter as tk
from tkinter import ttk, messagebox

import theme
from views.components import make_button
from views.dashboard_view import DashboardView
from views.member_view import MemberView
from views.paket_view import PaketView
from views.keanggotaan_view import KeanggotaanView
from views.trainer_view import TrainerView
from views.kelas_view import KelasView
from views.pendaftaran_view import PendaftaranView

TABS = [
    ("Dashboard", DashboardView),
    ("Member", MemberView),
    ("Paket", PaketView),
    ("Keanggotaan", KeanggotaanView),
    ("Trainer", TrainerView),
    ("Kelas", KelasView),
    ("Daftar Kelas", PendaftaranView),
]


class MainShell(tk.Frame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent, bg=theme.BG)
        self.user = user
        self.on_logout = on_logout

        # Header berwarna
        header = tk.Frame(self, bg=theme.PRIMARY)
        header.pack(fill="x")
        tk.Label(header, text="🏋  GymPro", bg=theme.PRIMARY, fg="#FFFFFF",
                 font=theme.font(16, "bold")).pack(side="left", padx=(16, 10), pady=10)
        tk.Label(header, text="Gym Membership Management", bg=theme.PRIMARY, fg="#B8C7EE",
                 font=theme.font(10)).pack(side="left")
        make_button(header, "Logout", theme.RED, self._logout).pack(side="right", padx=14, pady=8)
        tk.Label(header, text=f"👤  {user['nama_lengkap']}", bg=theme.PRIMARY, fg="#FFFFFF",
                 font=theme.font(10, "bold")).pack(side="right", padx=6)
        tk.Frame(self, bg=theme.ACCENT, height=3).pack(fill="x")

        # Tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.pages = {}
        for name, cls in TABS:
            page = cls(self.notebook)
            self.pages[name] = page
            self.notebook.add(page, text=f"  {name}  ")
        self.pages["Dashboard"].set_user(user["nama_lengkap"])

        # Muat ulang data (termasuk combobox) setiap pindah tab
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, _event):
        self.nametowidget(self.notebook.select()).refresh()

    def _logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin keluar dari akun ini?"):
            self.on_logout()
