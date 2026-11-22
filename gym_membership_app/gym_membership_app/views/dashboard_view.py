import tkinter as tk

import theme
from models import keanggotaan_model
from views.components import page_banner, StatCard, make_tree, fill_tree


class DashboardView(tk.Frame):
    COLS = [("nama_member", "Member", 180), ("no_telp", "No. Telp", 140),
            ("nama_paket", "Paket", 120), ("tgl_berakhir", "Berakhir", 120),
            ("status", "Status", 130)]

    def __init__(self, parent):
        super().__init__(parent, bg=theme.BG)
        self.banner = page_banner(self, "Dashboard", "", theme.INDIGO)
        self.banner.pack(fill="x")

        body = tk.Frame(self, bg=theme.BG)
        body.pack(fill="both", expand=True, padx=14, pady=12)

        # Kartu statistik berwarna
        cards = tk.Frame(body, bg=theme.BG)
        cards.pack(fill="x")
        cards.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        spec = [("Total Member", theme.BLUE),
                ("Member Aktif", theme.GREEN),
                ("Segera Berakhir", theme.ORANGE),
                ("Pendapatan Bulan Ini", theme.PURPLE)]
        self.cards = {}
        for i, (label, color) in enumerate(spec):
            card = StatCard(cards, "", label, color)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 3 else 6))
            self.cards[label] = card

        # Tabel follow-up
        panel = tk.LabelFrame(body, text=" Perlu Follow-up: keanggotaan kedaluwarsa / berakhir ≤ 7 hari ",
                              bg=theme.WHITE, fg=theme.RED, font=theme.font(10, "bold"),
                              bd=2, relief="groove", padx=10, pady=10)
        panel.pack(fill="both", expand=True, pady=(14, 0))
        wrap, self.tree = make_tree(panel, self.COLS)
        wrap.pack(fill="both", expand=True)
        self.empty = tk.Label(wrap, text="🎉  Semua keanggotaan aman, tidak ada yang perlu ditindaklanjuti.",
                              bg=theme.WHITE, fg=theme.MUTED, font=theme.font(10))
        self.refresh()

    def set_user(self, nama_lengkap):
        first = nama_lengkap.split()[0] if nama_lengkap.strip() else "Admin"
        self.banner.title_label.configure(text=f"Halo, {first} 👋")

    def refresh(self):
        self.banner.subtitle_label.configure(
            text=f"Ringkasan keanggotaan  ·  {theme.tanggal_indo()}")

        stats = keanggotaan_model.statistik()
        total = stats["Total Member"]
        aktif = stats["Member Aktif"]
        pct = round(aktif / total * 100) if total else 0
        self.cards["Total Member"].set(total, "terdaftar di sistem")
        self.cards["Member Aktif"].set(aktif, f"{pct}% dari total member")
        self.cards["Segera Berakhir"].set(stats["Segera Berakhir"], "berakhir ≤ 7 hari lagi")
        self.cards["Pendapatan Bulan Ini"].set(stats["Pendapatan Bulan Ini"], "dari transaksi bulan ini")

        rows = keanggotaan_model.segera_berakhir()
        fill_tree(self.tree, rows, [c[0] for c in self.COLS], use_id=False)
        if rows:
            self.empty.place_forget()
        else:
            self.empty.place(relx=0.5, rely=0.4, anchor="center")
