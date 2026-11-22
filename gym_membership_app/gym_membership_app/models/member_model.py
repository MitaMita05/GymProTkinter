from database.db import fetch_all, fetch_one, execute


def get_all(keyword=""):
    kw = f"%{keyword}%"
    return fetch_all(
        """SELECT m.id_member AS id, m.no_member, m.nama, m.jenis_kelamin, m.no_telp,
                  m.email, m.tgl_daftar,
                  CASE WHEN EXISTS (
                      SELECT 1 FROM keanggotaan k
                      WHERE k.id_member = m.id_member
                        AND k.tgl_berakhir >= date('now', 'localtime'))
                       THEN 'Aktif' ELSE 'Tidak Aktif' END AS status
           FROM member m
           WHERE m.no_member LIKE ? OR m.nama LIKE ? OR m.email LIKE ? OR m.no_telp LIKE ?
           ORDER BY m.nama""", (kw, kw, kw, kw))


def get_by_id(id_):
    return fetch_one(
        """SELECT no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar
           FROM member WHERE id_member = ?""", (id_,))


def create(no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar):
    return execute(
        """INSERT INTO member (no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar)
           VALUES (?,?,?,?,?,?,?)""",
        (no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar))


def update(id_, no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar):
    execute(
        """UPDATE member SET no_member = ?, nama = ?, jenis_kelamin = ?, no_telp = ?,
                  email = ?, alamat = ?, tgl_daftar = ?
           WHERE id_member = ?""",
        (no_member, nama, jenis_kelamin, no_telp, email, alamat, tgl_daftar, id_))


def delete(id_):
    execute("DELETE FROM member WHERE id_member = ?", (id_,))


def options():
    rows = fetch_all("SELECT id_member, no_member, nama FROM member ORDER BY nama")
    return [(r["id_member"], f'{r["no_member"]} - {r["nama"]}') for r in rows]
