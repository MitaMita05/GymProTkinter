# ERD - Gym Membership Management

Salin blok Mermaid di bawah ke https://mermaid.live untuk membuat gambar ERD
(atau pakai ekstensi "Markdown Preview Mermaid Support" di VS Code).

```mermaid
erDiagram
    MEMBER ||--o{ KEANGGOTAAN : "memiliki"
    PAKET_MEMBERSHIP ||--o{ KEANGGOTAAN : "dipilih pada"
    TRAINER ||--o{ KELAS : "mengajar"
    MEMBER ||--o{ PENDAFTARAN_KELAS : "mengikuti"
    KELAS ||--o{ PENDAFTARAN_KELAS : "diikuti"

    MEMBER {
        int id_member PK
        string no_member UK
        string nama
        string jenis_kelamin
        string no_telp
        string email
        string alamat
        date tgl_daftar
    }
    PAKET_MEMBERSHIP {
        int id_paket PK
        string nama_paket UK
        int durasi_hari
        int harga
        string deskripsi
    }
    KEANGGOTAAN {
        int id_keanggotaan PK
        int id_member FK
        int id_paket FK
        date tgl_mulai
        date tgl_berakhir
        int harga_dibayar
    }
    TRAINER {
        int id_trainer PK
        string nama
        string spesialisasi
        string no_telp
    }
    KELAS {
        int id_kelas PK
        string nama_kelas
        int id_trainer FK
        string hari
        string jam
        int kuota
    }
    PENDAFTARAN_KELAS {
        int id_pendaftaran PK
        int id_member FK
        int id_kelas FK
        date tgl_daftar
    }
```

## Relasi
| Relasi | Kardinalitas | Keterangan |
|---|---|---|
| MEMBER - KEANGGOTAAN | 1 : N | Satu member bisa daftar/perpanjang berkali-kali |
| PAKET_MEMBERSHIP - KEANGGOTAAN | 1 : N | Satu paket dipilih oleh banyak transaksi |
| TRAINER - KELAS | 1 : N | Satu trainer mengajar banyak kelas |
| MEMBER - KELAS | M : N | Dihubungkan oleh tabel PENDAFTARAN_KELAS |

## Aturan Bisnis
- `tgl_berakhir` dan `harga_dibayar` dihitung otomatis dari paket yang dipilih.
- Status keanggotaan otomatis: Aktif, Segera Berakhir (<= 7 hari), Kedaluwarsa.
- Member hanya dapat mendaftar kelas jika keanggotaannya masih aktif.
- Pendaftaran kelas ditolak jika kuota sudah penuh.
- Data induk (member, paket, trainer, kelas) yang masih dipakai tidak bisa dihapus.
