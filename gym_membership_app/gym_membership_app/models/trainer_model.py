from database.db import fetch_all, fetch_one, execute


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        """SELECT id_trainer AS id, nama, spesialisasi, no_telp
           FROM trainer
           WHERE nama LIKE ? OR spesialisasi LIKE ?
           ORDER BY nama""", (kw, kw))


def get_by_id(id_):
    return fetch_one(
        "SELECT nama, spesialisasi, no_telp FROM trainer WHERE id_trainer = ?", (id_,))


def create(nama, spesialisasi, no_telp):
    return execute("INSERT INTO trainer (nama, spesialisasi, no_telp) VALUES (?,?,?)",
                   (nama, spesialisasi, no_telp))


def update(id_, nama, spesialisasi, no_telp):
    execute("UPDATE trainer SET nama = ?, spesialisasi = ?, no_telp = ? WHERE id_trainer = ?",
            (nama, spesialisasi, no_telp, id_))


def delete(id_):
    execute("DELETE FROM trainer WHERE id_trainer = ?", (id_,))


def options():
    rows = fetch_all("SELECT id_trainer, nama, spesialisasi FROM trainer ORDER BY nama")
    return [(r["id_trainer"], f'{r["nama"]} ({r["spesialisasi"] or "-"})') for r in rows]
