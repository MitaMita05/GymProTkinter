import re

from models import kelas_model, trainer_model
from views.base_view import BaseCrudView

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


class KelasView(BaseCrudView):
    title = "Jadwal Kelas"
    subtitle = "Atur jadwal kelas, trainer pengajar, dan kuota peserta."
    accent = "#FB8C00"
    model = kelas_model
    columns = [("id", "ID", 40), ("nama_kelas", "Nama Kelas", 170),
               ("nama_trainer", "Trainer", 150), ("hari", "Hari", 80), ("jam", "Jam", 70),
               ("kuota", "Kuota", 60), ("terisi", "Terisi", 60)]
    fields = [("nama_kelas", "Nama Kelas", "entry", True),
              ("id_trainer", "Trainer", "combo", True),
              ("hari", "Hari", "combo", True),
              ("jam", "Jam (HH:MM)", "entry", True),
              ("kuota", "Kuota", "entry", True)]

    def combo_options(self, key):
        if key == "id_trainer":
            return trainer_model.options()
        return [(h, h) for h in HARI]

    def extra_validate(self, d):
        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", d["jam"]):
            return "Format jam harus HH:MM, contoh 07:30."
        if not d["kuota"].isdigit() or int(d["kuota"]) <= 0:
            return "Kuota harus berupa angka bulat > 0."
        return None

    def _args(self, d):
        return d["nama_kelas"], d["id_trainer"], d["hari"], d["jam"], int(d["kuota"])

    def save_new(self, d):
        kelas_model.create(*self._args(d))

    def save_update(self, id_, d):
        kelas_model.update(id_, *self._args(d))
