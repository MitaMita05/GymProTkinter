from database.db import fetch_all, fetch_one, execute


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        """SELECT id_paket AS id, nama_paket, durasi_hari, harga, deskripsi
           FROM paket_membership
           WHERE nama_paket LIKE ? OR deskripsi LIKE ?
           ORDER BY durasi_hari""", (kw, kw))


def get_by_id(id_):
    return fetch_one(
        """SELECT nama_paket, durasi_hari, harga, deskripsi
           FROM paket_membership WHERE id_paket = ?""", (id_,))


def create(nama_paket, durasi_hari, harga, deskripsi):
    return execute(
        "INSERT INTO paket_membership (nama_paket, durasi_hari, harga, deskripsi) VALUES (?,?,?,?)",
        (nama_paket, durasi_hari, harga, deskripsi))


def update(id_, nama_paket, durasi_hari, harga, deskripsi):
    execute(
        """UPDATE paket_membership SET nama_paket = ?, durasi_hari = ?, harga = ?, deskripsi = ?
           WHERE id_paket = ?""", (nama_paket, durasi_hari, harga, deskripsi, id_))


def delete(id_):
    execute("DELETE FROM paket_membership WHERE id_paket = ?", (id_,))


def options():
    rows = fetch_all("SELECT id_paket, nama_paket, durasi_hari, harga FROM paket_membership ORDER BY durasi_hari")
    return [(r["id_paket"], f'{r["nama_paket"]} - {r["durasi_hari"]} hari - Rp{r["harga"]:,}')
            for r in rows]
