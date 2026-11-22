"""Model pengguna (login). Password disimpan sebagai hash PBKDF2-SHA256 + salt acak.

Hanya akun pada ALLOWED_USERS yang boleh login (password sama: DEFAULT_PASSWORD).
"""
import hashlib
import hmac
import os
from datetime import date

from database.db import fetch_all, fetch_one, execute

ITERATIONS = 200_000

# Daftar akun yang boleh login (username tidak membedakan huruf besar/kecil)
ALLOWED_USERS = ["Mita", "Ferdy", "Rama", "Tasya", "Dosen"]
DEFAULT_PASSWORD = "1234"


def hash_password(password, salt_hex=None):
    """Return 'salt$hash' (keduanya hex)."""
    salt_hex = salt_hex or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt_hex), ITERATIONS)
    return f"{salt_hex}${digest.hex()}"


def verify_password(password, stored):
    salt_hex, _hash = stored.split("$", 1)
    return hmac.compare_digest(hash_password(password, salt_hex), stored)


def authenticate(username, password):
    """Return data pengguna bila username & password benar, selain itu None."""
    row = fetch_one(
        "SELECT id_user, username, nama_lengkap, password_hash FROM pengguna WHERE username = ?",
        (username,))
    if row is None or not verify_password(password, row["password_hash"]):
        return None
    return {"id_user": row["id_user"], "username": row["username"],
            "nama_lengkap": row["nama_lengkap"]}


def sync_allowed_users():
    """Pastikan hanya ALLOWED_USERS yang ada di tabel pengguna (password = DEFAULT_PASSWORD)."""
    allowed_lower = {u.lower() for u in ALLOWED_USERS}
    # Hapus akun lain (misalnya akun lama dari versi sebelumnya)
    for row in fetch_all("SELECT id_user, username FROM pengguna"):
        if row["username"].lower() not in allowed_lower:
            execute("DELETE FROM pengguna WHERE id_user = ?", (row["id_user"],))
    # Tambahkan yang belum ada / perbaiki password bila berbeda
    for name in ALLOWED_USERS:
        row = fetch_one("SELECT id_user, password_hash FROM pengguna WHERE username = ?", (name,))
        if row is None:
            execute(
                "INSERT INTO pengguna (username, nama_lengkap, password_hash, dibuat) VALUES (?,?,?,?)",
                (name, name, hash_password(DEFAULT_PASSWORD), date.today().isoformat()))
        elif not verify_password(DEFAULT_PASSWORD, row["password_hash"]):
            execute("UPDATE pengguna SET password_hash = ? WHERE id_user = ?",
                    (hash_password(DEFAULT_PASSWORD), row["id_user"]))
