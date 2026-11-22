from contextlib import closing
from datetime import date

from database.db import fetch_all, fetch_one, get_connection


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        """SELECT p.id_pendaftaran AS id, m.nama AS nama_member, k.nama_kelas,
                  k.hari || ' ' || k.jam AS jadwal, t.nama AS nama_trainer, p.tgl_daftar
           FROM pendaftaran_kelas p
           JOIN member m ON m.id_member = p.id_member
           JOIN kelas k ON k.id_kelas = p.id_kelas
           JOIN trainer t ON t.id_trainer = k.id_trainer
           WHERE m.nama LIKE ? OR k.nama_kelas LIKE ? OR t.nama LIKE ?
           ORDER BY p.id_pendaftaran DESC""", (kw, kw, kw))


def get_by_id(id_):
    return fetch_one(
        "SELECT id_member, id_kelas FROM pendaftaran_kelas WHERE id_pendaftaran = ?", (id_,))


def _cek(conn, id_member, id_kelas, exclude_id=0):
    """Aturan bisnis: member harus aktif & kuota kelas belum penuh."""
    aktif = conn.execute(
        """SELECT 1 FROM keanggotaan
           WHERE id_member = ? AND tgl_berakhir >= date('now', 'localtime')""",
        (id_member,)).fetchone()
    if not aktif:
        raise ValueError("Member tidak memiliki keanggotaan aktif.")
    kelas = conn.execute("SELECT kuota FROM kelas WHERE id_kelas = ?", (id_kelas,)).fetchone()
    if kelas is None:
        raise ValueError("Kelas tidak ditemukan.")
    terisi = conn.execute(
        "SELECT COUNT(*) FROM pendaftaran_kelas WHERE id_kelas = ? AND id_pendaftaran != ?",
        (id_kelas, exclude_id)).fetchone()[0]
    if terisi >= kelas["kuota"]:
        raise ValueError("Kuota kelas sudah penuh.")


def create(id_member, id_kelas):
    with closing(get_connection()) as conn:
        with conn:
            _cek(conn, id_member, id_kelas)
            conn.execute(
                "INSERT INTO pendaftaran_kelas (id_member, id_kelas, tgl_daftar) VALUES (?,?,?)",
                (id_member, id_kelas, date.today().isoformat()))


def update(id_, id_member, id_kelas):
    with closing(get_connection()) as conn:
        with conn:
            _cek(conn, id_member, id_kelas, exclude_id=id_)
            conn.execute(
                "UPDATE pendaftaran_kelas SET id_member = ?, id_kelas = ? WHERE id_pendaftaran = ?",
                (id_member, id_kelas, id_))


def delete(id_):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM pendaftaran_kelas WHERE id_pendaftaran = ?", (id_,))
