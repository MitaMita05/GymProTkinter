"""Komponen UI bersama (tkinter biasa, berwarna): banner, tombol, kartu statistik, tabel."""
import tkinter as tk
from tkinter import ttk

import theme

_MONEY_KEYS = {"harga", "harga_dibayar"}
_STATUS_TAG = {"Aktif": "ok", "Segera Berakhir": "warn",
               "Kedaluwarsa": "bad", "Tidak Aktif": "bad"}


def page_banner(parent, title, subtitle, color):
    """Pita judul berwarna di bagian atas halaman."""
    frame = tk.Frame(parent, bg=color)
    frame.title_label = tk.Label(frame, text=title, bg=color, fg="#FFFFFF",
                                 font=theme.font(16, "bold"), anchor="w")
    frame.title_label.pack(fill="x", padx=18, pady=(10, 0))
    frame.subtitle_label = tk.Label(frame, text=subtitle, bg=color, fg="#EAF1FF",
                                    font=theme.font(10), anchor="w")
    frame.subtitle_label.pack(fill="x", padx=18, pady=(0, 10))
    return frame


def make_button(parent, text, color, command=None, width=None):
    """Tombol berwarna dengan efek hover."""
    hover = theme.darken(color)
    kw = {"width": width} if width else {}
    btn = tk.Button(parent, text=text, command=command, bg=color, fg="#FFFFFF",
                    activebackground=hover, activeforeground="#FFFFFF", relief="flat",
                    bd=0, padx=18, pady=7, cursor="hand2", font=theme.font(10, "bold"), **kw)
    btn.bind("<Enter>", lambda _e: btn.configure(bg=hover))
    btn.bind("<Leave>", lambda _e: btn.configure(bg=color))
    return btn


class StatCard(tk.Frame):
    """Kartu statistik berwarna penuh."""

    def __init__(self, parent, icon, label, color):
        super().__init__(parent, bg=color, padx=18, pady=14)
        tk.Label(self, text=icon, bg=color, fg="#FFFFFF",
                 font=(theme.FONT, 22)).place(relx=1.0, x=-4, y=-4, anchor="ne")
        tk.Label(self, text=label, bg=color, fg="#FFFFFF", anchor="w",
                 font=theme.font(10, "bold")).pack(fill="x")
        self.value = tk.Label(self, text="0", bg=color, fg="#FFFFFF", anchor="w",
                              font=theme.font(24, "bold"))
        self.value.pack(fill="x", pady=(4, 0))
        self.sub = tk.Label(self, text="", bg=color, fg="#EAF1FF", anchor="w",
                            font=theme.font(9))
        self.sub.pack(fill="x")

    def set(self, value, sub=""):
        self.value.configure(text=str(value))
        self.sub.configure(text=sub)


def make_tree(parent, columns, **kwargs):
    """Treeview berwarna + scrollbar. Return (frame_pembungkus, tree)."""
    wrap = tk.Frame(parent, bg=theme.WHITE, highlightthickness=1,
                    highlightbackground=theme.BORDER)
    keys = [c[0] for c in columns]
    tree = ttk.Treeview(wrap, columns=keys, show="headings", selectmode="browse",
                        style="Gym.Treeview", **kwargs)
    for key, heading, width in columns:
        tree.heading(key, text=heading, anchor="w")
        tree.column(key, width=width, minwidth=40, anchor="w", stretch=(key != "id"))
    sb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    tree.tag_configure("odd", background="#FFFFFF")
    tree.tag_configure("even", background="#EAF1FB")
    tree.tag_configure("ok", foreground="#1B8F4B")
    tree.tag_configure("warn", foreground="#C46A00")
    tree.tag_configure("bad", foreground="#D32F2F")
    return wrap, tree


def format_cell(key, value):
    if value is None:
        return ""
    if key in _MONEY_KEYS and isinstance(value, int):
        return "Rp " + f"{value:,}".replace(",", ".")
    return value


def fill_tree(tree, rows, keys, use_id=True):
    """Isi tabel: baris belang-belang + warna teks sesuai kolom 'status'."""
    tree.delete(*tree.get_children())
    for n, row in enumerate(rows):
        tags = ["even" if n % 2 else "odd"]
        if "status" in keys:
            tag = _STATUS_TAG.get(row["status"])
            if tag:
                tags.append(tag)
        values = [format_cell(k, row[k]) for k in keys]
        if use_id:
            tree.insert("", "end", iid=str(row["id"]), values=values, tags=tags)
        else:
            tree.insert("", "end", values=values, tags=tags)
