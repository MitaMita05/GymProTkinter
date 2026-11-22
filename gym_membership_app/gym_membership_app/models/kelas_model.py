from database.db import fetch_all, fetch_one, execute


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        """SELECT k.id_kelas AS id, k.nama_kelas, t.nama AS nama_trainer, k.hari, k.jam,
                  k.kuota,
                  (SELECT COUNT(*) FROM pendaftaran_kelas p WHERE p.id_kelas = k.id_kelas) AS terisi
           FROM kelas k JOIN trainer t ON t.id_trainer = k.id_trainer
           WHERE k.nama_kelas LIKE ? OR t.nama LIKE ? OR k.hari LIKE ?
           ORDER BY k.nama_kelas""", (kw, kw, kw))


def get_by_id(id_):
    return fetch_one(
        "SELECT nama_kelas, id_trainer, hari, jam, kuota FROM kelas WHERE id_kelas = ?", (id_,))


def create(nama_kelas, id_trainer, hari, jam, kuota):
    return execute(
        "INSERT INTO kelas (nama_kelas, id_trainer, hari, jam, kuota) VALUES (?,?,?,?,?)",
        (nama_kelas, id_trainer, hari, jam, kuota))


def update(id_, nama_kelas, id_trainer, hari, jam, kuota):
    terisi = fetch_one("SELECT COUNT(*) FROM pendaftaran_kelas WHERE id_kelas = ?", (id_,))[0]
    if kuota < terisi:
        raise ValueError(f"Kuota tidak boleh lebih kecil dari peserta terdaftar ({terisi}).")
    execute(
        """UPDATE kelas SET nama_kelas = ?, id_trainer = ?, hari = ?, jam = ?, kuota = ?
           WHERE id_kelas = ?""", (nama_kelas, id_trainer, hari, jam, kuota, id_))


def delete(id_):
    execute("DELETE FROM kelas WHERE id_kelas = ?", (id_,))


def options():
    rows = fetch_all(
        """SELECT k.id_kelas, k.nama_kelas, k.hari, k.jam, k.kuota,
                  (SELECT COUNT(*) FROM pendaftaran_kelas p WHERE p.id_kelas = k.id_kelas) AS terisi
           FROM kelas k ORDER BY k.nama_kelas""")
    return [(r["id_kelas"],
             f'{r["nama_kelas"]} - {r["hari"]} {r["jam"]} ({r["terisi"]}/{r["kuota"]})')
            for r in rows]
