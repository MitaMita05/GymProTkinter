from models import paket_model
from views.base_view import BaseCrudView


class PaketView(BaseCrudView):
    title = "Paket Membership"
    subtitle = "Atur paket membership: durasi, harga, dan deskripsi."
    accent = "#8E24AA"
    model = paket_model
    columns = [("id", "ID", 50), ("nama_paket", "Nama Paket", 150),
               ("durasi_hari", "Durasi (hari)", 100), ("harga", "Harga (Rp)", 120),
               ("deskripsi", "Deskripsi", 350)]
    fields = [("nama_paket", "Nama Paket", "entry", True),
              ("durasi_hari", "Durasi (hari)", "entry", True),
              ("harga", "Harga (Rp)", "entry", True),
              ("deskripsi", "Deskripsi", "entry", False)]

    def extra_validate(self, d):
        if not d["durasi_hari"].isdigit() or int(d["durasi_hari"]) <= 0:
            return "Durasi harus berupa angka bulat > 0."
        if not d["harga"].isdigit():
            return "Harga harus berupa angka bulat >= 0 (tanpa titik/koma)."
        return None

    def _args(self, d):
        return d["nama_paket"], int(d["durasi_hari"]), int(d["harga"]), d["deskripsi"]

    def save_new(self, d):
        paket_model.create(*self._args(d))

    def save_update(self, id_, d):
        paket_model.update(id_, *self._args(d))
