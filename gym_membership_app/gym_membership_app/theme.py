"""Palet warna, font, dan gaya ttk untuk tampilan tkinter biasa yang tetap berwarna."""
from datetime import date
from tkinter import ttk

FONT = "Segoe UI"

# ---- Warna utama ----
PRIMARY = "#1F3C88"      # biru tua (header, judul tabel)
ACCENT = "#F57C00"       # oranye (tab aktif, tombol utama, pilihan baris)
BG = "#EAF0FA"           # latar halaman
WHITE = "#FFFFFF"
TEXT = "#263238"
MUTED = "#607D8B"
BORDER = "#C5D0E6"
FIELD = "#F7F9FC"

BLUE = "#1E88E5"
GREEN = "#2E9E5B"
RED = "#E53935"
PURPLE = "#8E24AA"
TEAL = "#00897B"
ORANGE = "#FB8C00"
PINK = "#D81B60"
INDIGO = "#3949AB"

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def font(size=10, weight="normal"):
    return (FONT, size, weight)


def darken(color, factor=0.82):
    """Warna hex yang lebih gelap (untuk efek hover tombol)."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02X}{:02X}{:02X}".format(int(r * factor), int(g * factor), int(b * factor))


def tanggal_indo(d=None):
    d = d or date.today()
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def apply_style(root):
    """Terapkan gaya ttk berwarna (panggil sekali setelah root dibuat)."""
    s = ttk.Style(root)
    s.theme_use("clam")

    # Tabel
    s.configure("Gym.Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT,
                rowheight=28, borderwidth=0, font=font(10))
    s.map("Gym.Treeview", background=[("selected", ACCENT)],
          foreground=[("selected", WHITE)])
    s.configure("Gym.Treeview.Heading", background=PRIMARY, foreground=WHITE,
                relief="flat", borderwidth=0, padding=(8, 7), font=font(10, "bold"))
    s.map("Gym.Treeview.Heading", background=[("active", "#2E4FA8")])

    # Tab (Notebook)
    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 6, 0, 0))
    s.configure("TNotebook.Tab", background="#C9D6F0", foreground=PRIMARY,
                padding=(18, 8), font=font(10, "bold"), borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", ACCENT), ("active", "#AFC2EA")],
          foreground=[("selected", WHITE)])

    # Combobox & Scrollbar
    s.configure("TCombobox", fieldbackground=FIELD, background="#C9D6F0",
                foreground=TEXT, arrowcolor=PRIMARY, bordercolor=BORDER, padding=4)
    s.map("TCombobox", fieldbackground=[("readonly", FIELD)],
          foreground=[("readonly", TEXT)], background=[("active", "#AFC2EA")])
    s.configure("Vertical.TScrollbar", background="#9FB3D9", troughcolor="#E3E9F5",
                bordercolor="#E3E9F5", arrowcolor=WHITE)
    s.map("Vertical.TScrollbar", background=[("active", PRIMARY)])

    # Daftar dropdown combobox
    root.option_add("*TCombobox*Listbox.background", WHITE)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", WHITE)
    root.option_add("*TCombobox*Listbox.font", font(10))
