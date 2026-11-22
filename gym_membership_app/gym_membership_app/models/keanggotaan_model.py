from contextlib import closing
from datetime import datetime, timedelta

from database.db import fetch_all, fetch_one, execute, get_connection

FMT = "%Y-%m-%d"

# Status dihitung otomatis dari tanggal berakhir
STATUS_SQL = """CASE
    WHEN k.tgl_berakhir < date('now', 'localtime') THEN 'Kedaluwarsa'
    WHEN k.tgl_berakhir <= date('now', 'localtime', '+7 days') THEN 'Segera Berakhir'
    ELSE 'Aktif' END"""


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        f"""SELECT k.id_keanggotaan AS id, m.nama AS nama_member, p.nama_paket,
                   k.tgl_mulai, k.tgl_berakhir, k.harga_dibayar, {STATUS_SQL} AS status
            FROM keanggotaan k
            JOIN member m ON m.id_member = k.id_member
            JOIN paket_membership p ON p.id_paket = k.id_paket
            WHERE m.nama LIKE ? OR m.no_member LIKE ? OR p.nama_paket LIKE ?
            ORDER BY k.id_keanggotaan DESC""", (kw, kw, kw))


def get_by_id(id_):
    return fetch_one(
        "SELECT id_member, id_paket, tgl_mulai FROM keanggotaan WHERE id_keanggotaan = ?", (id_,))


def _hitung(conn, id_paket, tgl_mulai):
    """Hitung tanggal berakhir & harga dari paket yang dipilih."""
    paket = conn.execute(
        "SELECT durasi_hari, harga FROM paket_membership WHERE id_paket = ?", (id_paket,)).fetchone()
    if paket is None:
        raise ValueError("Paket tidak ditemukan.")
    berakhir = datetime.strptime(tgl_mulai, FMT) + timedelta(days=paket["durasi_hari"])
    return berakhir.strftime(FMT), paket["harga"]


def create(id_member, id_paket, tgl_mulai):
    with closing(get_connection()) as conn:
        with conn:
            berakhir, harga = _hitung(conn, id_paket, tgl_mulai)
            conn.execute(
                """INSERT INTO keanggotaan (id_member, id_paket, tgl_mulai, tgl_berakhir, harga_dibayar)
                   VALUES (?,?,?,?,?)""", (id_member, id_paket, tgl_mulai, berakhir, harga))


def update(id_, id_member, id_paket, tgl_mulai):
    with closing(get_connection()) as conn:
        with conn:
            berakhir, harga = _hitung(conn, id_paket, tgl_mulai)
            conn.execute(
                """UPDATE keanggotaan SET id_member = ?, id_paket = ?, tgl_mulai = ?,
                          tgl_berakhir = ?, harga_dibayar = ?
                   WHERE id_keanggotaan = ?""",
                (id_member, id_paket, tgl_mulai, berakhir, harga, id_))


def delete(id_):
    execute("DELETE FROM keanggotaan WHERE id_keanggotaan = ?", (id_,))


def segera_berakhir():
    """Keanggotaan yang kedaluwarsa atau berakhir <= 7 hari lagi."""
    return fetch_all(
        f"""SELECT m.nama AS nama_member, m.no_telp, p.nama_paket, k.tgl_berakhir,
                   {STATUS_SQL} AS status
            FROM keanggotaan k
            JOIN member m ON m.id_member = k.id_member
            JOIN paket_membership p ON p.id_paket = k.id_paket
            WHERE k.tgl_berakhir <= date('now', 'localtime', '+7 days')
              AND NOT EXISTS (SELECT 1 FROM keanggotaan k2
                              WHERE k2.id_member = k.id_member
                                AND k2.tgl_berakhir > k.tgl_berakhir)
            ORDER BY k.tgl_berakhir""")


def statistik():
    q = lambda sql: fetch_one(sql)[0]
    pendapatan = q("""SELECT COALESCE(SUM(harga_dibayar), 0) FROM keanggotaan
                      WHERE strftime('%Y-%m', tgl_mulai) = strftime('%Y-%m', 'now', 'localtime')""")
    return {
        "Total Member": q("SELECT COUNT(*) FROM member"),
        "Member Aktif": q("""SELECT COUNT(DISTINCT id_member) FROM keanggotaan
                             WHERE tgl_berakhir >= date('now', 'localtime')"""),
        "Segera Berakhir": q("""SELECT COUNT(DISTINCT id_member) FROM keanggotaan
                                WHERE tgl_berakhir BETWEEN date('now', 'localtime')
                                      AND date('now', 'localtime', '+7 days')"""),
        "Pendapatan Bulan Ini": f"Rp{pendapatan:,}",
    }
