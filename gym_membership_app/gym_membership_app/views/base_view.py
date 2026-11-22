"""Kelas dasar halaman CRUD: banner berwarna, form, tombol, pencarian, dan tabel."""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import theme
from views.components import page_banner, make_button, make_tree, fill_tree


class BaseCrudView(tk.Frame):
    # Diisi oleh subclass
    title = ""
    subtitle = ""
    accent = theme.PRIMARY   # warna banner & judul form
    columns = []   # [(key, heading, width), ...]  -> key pertama harus "id"
    fields = []    # [(key, label, kind, required), ...]  kind: "entry" | "combo"
    model = None   # modul model

    def __init__(self, parent):
        super().__init__(parent, bg=theme.BG)
        self.widgets = {}
        self.combo_maps = {}      # key -> {label: id}
        self.selected_id = None
        self.search_var = tk.StringVar()
        self._build()
        self.refresh()

    # ---------- UI ----------
    def _build(self):
        page_banner(self, self.title, self.subtitle, self.accent).pack(fill="x")
        body = tk.Frame(self, bg=theme.BG)
        body.pack(fill="both", expand=True, padx=14, pady=12)

        # Form
        self.form = tk.LabelFrame(body, text=" Tambah Data Baru ", bg=theme.WHITE,
                                  fg=self.accent, font=theme.font(10, "bold"),
                                  bd=2, relief="groove", padx=14, pady=10)
        self.form.pack(fill="x")
        self.form.grid_columnconfigure(1, weight=1)
        self.form.grid_columnconfigure(3, weight=1)
        for i, (key, label, kind, required) in enumerate(self.fields):
            r, c = divmod(i, 2)
            tk.Label(self.form, text=label + (" *" if required else ""), bg=theme.WHITE,
                     fg=theme.TEXT, font=theme.font(10, "bold")
                     ).grid(row=r, column=c * 2, sticky="w", padx=(0, 8), pady=5)
            if kind == "combo":
                w = ttk.Combobox(self.form, state="readonly", width=34, font=theme.font(10))
            else:
                w = tk.Entry(self.form, width=38, font=theme.font(10), relief="flat",
                             bg=theme.FIELD, fg=theme.TEXT, insertbackground=theme.TEXT,
                             highlightthickness=1, highlightbackground=theme.BORDER,
                             highlightcolor=self.accent)
            w.grid(row=r, column=c * 2 + 1, sticky="ew", padx=(0, 24), pady=5, ipady=3)
            self.widgets[key] = w

        # Tombol
        btns = tk.Frame(body, bg=theme.BG)
        btns.pack(fill="x", pady=10)
        make_button(btns, "＋ Tambah", theme.GREEN, self.on_add).pack(side="left", padx=(0, 8))
        make_button(btns, "✎ Ubah", theme.BLUE, self.on_update).pack(side="left", padx=8)
        make_button(btns, "🗑 Hapus", theme.RED, self.on_delete).pack(side="left", padx=8)
        make_button(btns, "↺ Bersihkan", theme.PURPLE, self.clear_form).pack(side="left", padx=8)
        self.extra_buttons(btns)

        # Pencarian
        search = tk.Frame(body, bg=theme.BG)
        search.pack(fill="x", pady=(0, 6))
        tk.Label(search, text="🔍 Cari:", bg=theme.BG, fg=theme.PRIMARY,
                 font=theme.font(10, "bold")).pack(side="left")
        tk.Entry(search, textvariable=self.search_var, width=40, font=theme.font(10),
                 relief="flat", bg=theme.WHITE, fg=theme.TEXT, insertbackground=theme.TEXT,
                 highlightthickness=1, highlightbackground=theme.BORDER,
                 highlightcolor=self.accent).pack(side="left", padx=8, ipady=4)
        self.search_var.trace_add("write", lambda *_: self.load_table())
        self.count_label = tk.Label(search, text="", bg=theme.BG, fg=theme.MUTED,
                                    font=theme.font(10, "bold"))
        self.count_label.pack(side="right")

        # Tabel
        wrap, self.tree = make_tree(body, self.columns)
        wrap.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def extra_buttons(self, frame):
        """Hook untuk tombol tambahan (opsional)."""

    # ---------- Hook subclass ----------
    def combo_options(self, key):
        return []

    def extra_validate(self, data):
        return None

    def save_new(self, data):
        raise NotImplementedError

    def save_update(self, id_, data):
        raise NotImplementedError

    def on_form_cleared(self):
        """Hook: isi nilai default form (opsional)."""

    # ---------- Data ----------
    def refresh(self):
        for key, _l, kind, _r in self.fields:
            if kind == "combo":
                opts = self.combo_options(key)
                self.combo_maps[key] = {label: id_ for id_, label in opts}
                self.widgets[key]["values"] = [label for _id, label in opts]
        self.load_table()
        self.clear_form()

    def load_table(self):
        keys = [c[0] for c in self.columns]
        rows = self.model.get_all(self.search_var.get().strip())
        fill_tree(self.tree, rows, keys)
        self.count_label.configure(text=f"{len(rows)} data")

    def get_form_data(self):
        data = {}
        for key, _l, kind, _r in self.fields:
            val = self.widgets[key].get().strip()
            data[key] = self.combo_maps[key].get(val) if kind == "combo" else val
        return data

    def set_form(self, record):
        for key, _l, kind, _r in self.fields:
            w = self.widgets[key]
            val = record[key]
            if kind == "combo":
                label = next((l for l, i in self.combo_maps[key].items() if i == val), "")
                w.set(label)
            else:
                w.delete(0, "end")
                w.insert(0, "" if val is None else str(val))

    def clear_form(self):
        self.selected_id = None
        for key, _l, kind, _r in self.fields:
            w = self.widgets[key]
            if kind == "combo":
                w.set("")
            else:
                w.delete(0, "end")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.on_form_cleared()
        self._update_mode()

    def _update_mode(self):
        if self.selected_id is None:
            self.form.configure(text=" Tambah Data Baru ")
        else:
            self.form.configure(text=f" Edit Data  ·  ID {self.selected_id} ")

    # ---------- Event ----------
    def on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        self.selected_id = int(sel[0])
        record = self.model.get_by_id(self.selected_id)
        if record:
            self.set_form(record)
        self._update_mode()

    def _validate(self, data):
        for key, label, _k, required in self.fields:
            if required and (data[key] is None or data[key] == ""):
                return f"Kolom '{label}' wajib diisi."
        return self.extra_validate(data)

    def _run(self, action, success_msg):
        try:
            action()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Gagal", self._format_integrity_error(e))
            return
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))
            return
        messagebox.showinfo("Berhasil", success_msg)
        self.refresh()

    @staticmethod
    def _format_integrity_error(e):
        msg = str(e)
        if "UNIQUE" in msg:
            return "Data duplikat: nilai yang bersifat unik sudah dipakai."
        if "FOREIGN KEY" in msg:
            return "Data tidak dapat dihapus/diubah karena masih dipakai di tabel lain."
        if "CHECK" in msg:
            return "Nilai tidak valid (cek angka/status)."
        return msg

    def on_add(self):
        data = self.get_form_data()
        err = self._validate(data)
        if err:
            messagebox.showwarning("Validasi", err)
            return
        self._run(lambda: self.save_new(data), "Data berhasil ditambahkan.")

    def on_update(self):
        if self.selected_id is None:
            messagebox.showwarning("Pilih Data", "Pilih data pada tabel terlebih dahulu.")
            return
        data = self.get_form_data()
        err = self._validate(data)
        if err:
            messagebox.showwarning("Validasi", err)
            return
        self._run(lambda: self.save_update(self.selected_id, data), "Data berhasil diubah.")

    def on_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Pilih Data", "Pilih data pada tabel terlebih dahulu.")
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return
        self._run(lambda: self.model.delete(self.selected_id), "Data berhasil dihapus.")
