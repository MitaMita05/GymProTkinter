from datetime import date, datetime

from models import keanggotaan_model, member_model, paket_model
from views.base_view import BaseCrudView


class KeanggotaanView(BaseCrudView):
    title = "Transaksi Keanggotaan (Daftar / Perpanjang Paket)"
    subtitle = "Daftarkan atau perpanjang paket member. Tanggal berakhir & harga dihitung otomatis."
    accent = "#2E9E5B"
    model = keanggotaan_model
    columns = [("id", "ID", 40), ("nama_member", "Member", 150), ("nama_paket", "Paket", 100),
               ("tgl_mulai", "Mulai", 90), ("tgl_berakhir", "Berakhir", 90),
               ("harga_dibayar", "Dibayar (Rp)", 100), ("status", "Status", 110)]
    fields = [("id_member", "Member", "combo", True),
              ("id_paket", "Paket", "combo", True),
              ("tgl_mulai", "Tgl Mulai (YYYY-MM-DD)", "entry", True)]

    def combo_options(self, key):
        return member_model.options() if key == "id_member" else paket_model.options()

    def on_form_cleared(self):
        self.widgets["tgl_mulai"].insert(0, date.today().isoformat())

    def extra_validate(self, d):
        try:
            datetime.strptime(d["tgl_mulai"], "%Y-%m-%d")
        except ValueError:
            return "Format tanggal harus YYYY-MM-DD."
        return None

    def save_new(self, d):
        keanggotaan_model.create(d["id_member"], d["id_paket"], d["tgl_mulai"])

    def save_update(self, id_, d):
        keanggotaan_model.update(id_, d["id_member"], d["id_paket"], d["tgl_mulai"])
