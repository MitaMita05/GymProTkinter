# Gym Membership Management (Mini Project UAS)

Aplikasi desktop GUI berbasis **Python (Tkinter)** dengan tampilan berwarna (header, tab, kartu statistik, tabel belang-belang) dengan database **SQLite**.
Fitur CRUD untuk: Member, Paket, Keanggotaan, Trainer, Kelas, dan Pendaftaran Kelas,
ditambah dashboard ringkasan.

## Cara Menjalankan di VS Code
1. Ekstrak zip. Pastikan Anda membuka folder yang LANGSUNG berisi `main.py`
   (hati-hati folder bersarang `gym_membership_app/gym_membership_app`).
2. VS Code: File > Open Folder > pilih folder tersebut.
3. Buka terminal (Ctrl + `) lalu jalankan:
   ```
   python main.py
   ```
   Linux/Mac: `python3 main.py`
4. Database `gym.db` dibuat otomatis beserta data contoh.
5. Login dengan salah satu akun berikut (password semuanya **1234**):
   `Mita`, `Ferdy`, `Rama`, `Tasya`, `Dosen`.
   Daftar akun ada di `ALLOWED_USERS` pada `models/user_model.py`; password disimpan sebagai hash PBKDF2-SHA256.

Catatan: jalankan `main.py`, bukan file di folder `models/` atau `views/`.
Linux: jika error `No module named tkinter` -> `sudo apt install python3-tk`.

## Struktur Folder
```
gym_membership_app/
├── main.py
├── theme.py               # warna, font, gaya ttk
├── requirements.txt
├── README.md
├── database/
│   ├── db.py              # koneksi, helper, data contoh
│   └── schema.sql         # DDL 6 tabel + tabel pengguna (login)
├── models/                # query SQL / logika bisnis
│   ├── paket_model.py
│   ├── member_model.py
│   ├── keanggotaan_model.py
│   ├── trainer_model.py
│   ├── kelas_model.py
│   ├── pendaftaran_model.py
│   └── user_model.py      # login, daftar akun yang diizinkan, hash password
├── views/                 # tampilan GUI
│   ├── auth_view.py       # layar login
│   ├── shell.py           # header + tab (Notebook)
│   ├── components.py      # banner, tombol, kartu statistik, tabel
│   ├── base_view.py       # kelas dasar halaman CRUD
│   ├── dashboard_view.py
│   ├── member_view.py
│   ├── paket_view.py
│   ├── keanggotaan_view.py
│   ├── trainer_view.py
│   ├── kelas_view.py
│   └── pendaftaran_view.py
└── docs/
    └── ERD.md             # ERD (Mermaid)
```
