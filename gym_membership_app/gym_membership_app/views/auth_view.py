"""Layar Login (tkinter biasa, berwarna)."""
import tkinter as tk

import theme
from models import user_model
from views.components import make_button


class AuthView(tk.Frame):
    def __init__(self, parent, on_login):
        super().__init__(parent, bg=theme.BG)
        self.on_login = on_login

        # Pita berwarna di atas + garis aksen
        band = tk.Frame(self, bg=theme.PRIMARY)
        band.place(x=0, y=0, relwidth=1, height=260)
        tk.Frame(self, bg=theme.ACCENT).place(x=0, y=260, relwidth=1, height=4)
        tk.Label(band, text="🏋", bg=theme.PRIMARY, fg="#FFFFFF",
                 font=(theme.FONT, 34)).pack(pady=(26, 0))
        tk.Label(band, text="GymPro", bg=theme.PRIMARY, fg="#FFFFFF",
                 font=theme.font(22, "bold")).pack()
        tk.Label(band, text="Gym Membership Management", bg=theme.PRIMARY, fg="#B8C7EE",
                 font=theme.font(10)).pack()

        # Kartu form (menimpa sebagian pita)
        card = tk.Frame(self, bg=theme.WHITE, highlightthickness=1,
                        highlightbackground=theme.BORDER)
        card.place(relx=0.5, y=170, anchor="n", width=420, height=410)

        tk.Label(card, text="FORM LOGIN", bg=theme.WHITE, fg=theme.PRIMARY,
                 font=theme.font(15, "bold")).pack(pady=(24, 2))
        self.msg = tk.Label(card, text="", bg=theme.WHITE, fg=theme.RED,
                            font=theme.font(9, "bold"), wraplength=330)
        self.msg.pack(pady=(0, 2))

        self.username = self._field(card, "Username")
        self.password = self._field(card, "Password", show="•")

        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(card, text="Tampilkan password", variable=self.show_var,
                       command=self._toggle_password, bg=theme.WHITE, fg=theme.MUTED,
                       activebackground=theme.WHITE, selectcolor=theme.WHITE,
                       font=theme.font(9), cursor="hand2"
                       ).pack(anchor="w", padx=40, pady=(8, 0))

        make_button(card, "LOGIN", theme.ACCENT, self._do_login).pack(
            fill="x", padx=40, pady=(16, 0), ipady=4)

        for e in (self.username, self.password):
            e.bind("<Return>", lambda _e: self._do_login())
        self.username.focus_set()

    def _field(self, card, label, show=None):
        tk.Label(card, text=label, bg=theme.WHITE, fg=theme.TEXT, anchor="w",
                 font=theme.font(10, "bold")).pack(fill="x", padx=40, pady=(10, 3))
        entry = tk.Entry(card, font=theme.font(11), relief="flat", bg=theme.FIELD,
                         fg=theme.TEXT, insertbackground=theme.TEXT, show=show or "",
                         highlightthickness=1, highlightbackground=theme.BORDER,
                         highlightcolor=theme.ACCENT)
        entry.pack(fill="x", padx=40, ipady=6)
        return entry

    def _toggle_password(self):
        self.password.configure(show="" if self.show_var.get() else "•")

    def _do_login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            self.msg.configure(text="Username dan password wajib diisi.")
            return
        user = user_model.authenticate(username, password)
        if user is None:
            self.msg.configure(text="Username atau password salah.")
            self.password.delete(0, "end")
            return
        self.on_login(user)
