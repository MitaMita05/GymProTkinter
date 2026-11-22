"""Koneksi, helper SQLite, dan data contoh."""
import os
import sqlite3
from contextlib import closing
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "gym.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Buat tabel (jika belum ada) lalu isi data contoh bila database masih kosong."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        script = f.read()
    with closing(get_connection()) as conn:
        conn.executescript(script)
        _seed(conn)
        conn.commit()


def _seed(conn):
    if conn.execute("SELECT COUNT(*) FROM paket_membership").fetchone()[0]:
        return
    today = date.today()
    d = lambda n: (today + timedelta(days=n)).isoformat()

    conn.executemany(
        "INSERT INTO paket_membership (nama_paket, durasi_hari, harga, deskripsi) VALUES (?,?,?,?)",
        [("Bulanan", 30, 250000, "Akses gym 1 bulan"),
         ("Triwulan", 90, 650000, "Akses gym 3 bulan + 1 sesi PT"),
         ("Tahunan", 365, 2200000, "Akses gym 1 tahun + bonus kaos")])
    conn.executemany(
        "INSERT INTO trainer (nama, spesialisasi, no_telp) VALUES (?,?,?)",
        [("Rizky Maulana", "Strength & Conditioning", "081200000001"),
         ("Dewi Anggraini", "Yoga & Pilates", "081200000002"),
         ("Fajar Nugroho", "Cardio & HIIT", "081200000003")])
    conn.executemany(
        "INSERT INTO kelas (nama_kelas, id_trainer, hari, jam, kuota) VALUES (?,?,?,?,?)",
        [("Morning Yoga", 2, "Senin", "07:00", 15),
         ("HIIT Blast", 3, "Rabu", "18:00", 12),
         ("Strength 101", 1, "Jumat", "17:00", 10)])
    conn.executemany(
        """INSERT INTO member (no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar)
           VALUES (?,?,?,?,?,?,?)""",
        [("GYM-001", "Andi Pratama", "L", "081234567890", "andi@mail.com", "Samarinda", d(-10)),
         ("GYM-002", "Siti Aisyah", "P", "081298765432", "siti@mail.com", "Balikpapan", d(-27)),
         ("GYM-003", "Budi Santoso", "L", "085211223344", "budi@mail.com", "Samarinda", d(-45))])
    # 1 aktif, 1 segera berakhir, 1 kedaluwarsa (untuk demo)
    conn.executemany(
        """INSERT INTO keanggotaan (id_member, id_paket, tgl_mulai, tgl_berakhir, harga_dibayar)
           VALUES (?,?,?,?,?)""",
        [(1, 1, d(-10), d(20), 250000),
         (2, 1, d(-27), d(3), 250000),
         (3, 1, d(-45), d(-15), 250000)])
    conn.executemany(
        "INSERT INTO pendaftaran_kelas (id_member, id_kelas, tgl_daftar) VALUES (?,?,?)",
        [(1, 2, d(-2)), (2, 1, d(-1))])


def fetch_all(sql, params=()):
    with closing(get_connection()) as conn:
        return conn.execute(sql, params).fetchall()


def fetch_one(sql, params=()):
    with closing(get_connection()) as conn:
        return conn.execute(sql, params).fetchone()


def execute(sql, params=()):
    with closing(get_connection()) as conn:
        with conn:
            cur = conn.execute(sql, params)
            return cur.lastrowid
