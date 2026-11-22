PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS paket_membership (
    id_paket    INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_paket  TEXT NOT NULL UNIQUE,
    durasi_hari INTEGER NOT NULL CHECK (durasi_hari > 0),
    harga       INTEGER NOT NULL CHECK (harga >= 0),
    deskripsi   TEXT
);

CREATE TABLE IF NOT EXISTS member (
    id_member     INTEGER PRIMARY KEY AUTOINCREMENT,
    no_member     TEXT NOT NULL UNIQUE,
    nama          TEXT NOT NULL,
    jenis_kelamin TEXT NOT NULL CHECK (jenis_kelamin IN ('L', 'P')),
    no_telp       TEXT,
    email         TEXT,
    alamat        TEXT,
    tgl_daftar    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trainer (
    id_trainer   INTEGER PRIMARY KEY AUTOINCREMENT,
    nama         TEXT NOT NULL,
    spesialisasi TEXT,
    no_telp      TEXT
);

CREATE TABLE IF NOT EXISTS kelas (
    id_kelas   INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kelas TEXT NOT NULL,
    id_trainer INTEGER NOT NULL,
    hari       TEXT NOT NULL,
    jam        TEXT NOT NULL,
    kuota      INTEGER NOT NULL CHECK (kuota > 0),
    FOREIGN KEY (id_trainer) REFERENCES trainer(id_trainer)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS keanggotaan (
    id_keanggotaan INTEGER PRIMARY KEY AUTOINCREMENT,
    id_member      INTEGER NOT NULL,
    id_paket       INTEGER NOT NULL,
    tgl_mulai      TEXT NOT NULL,
    tgl_berakhir   TEXT NOT NULL,
    harga_dibayar  INTEGER NOT NULL,
    FOREIGN KEY (id_member) REFERENCES member(id_member)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_paket) REFERENCES paket_membership(id_paket)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pendaftaran_kelas (
    id_pendaftaran INTEGER PRIMARY KEY AUTOINCREMENT,
    id_member      INTEGER NOT NULL,
    id_kelas       INTEGER NOT NULL,
    tgl_daftar     TEXT NOT NULL,
    UNIQUE (id_member, id_kelas),
    FOREIGN KEY (id_member) REFERENCES member(id_member)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_kelas) REFERENCES kelas(id_kelas)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pengguna (
    id_user       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
    nama_lengkap  TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    dibuat        TEXT NOT NULL
);
