from models import kelas_model, member_model, pendaftaran_model
from views.base_view import BaseCrudView


class PendaftaranView(BaseCrudView):
    title = "Pendaftaran Kelas Member"
    subtitle = "Daftarkan member ke kelas yang tersedia."
    accent = "#D81B60"
    model = pendaftaran_model
    columns = [("id", "ID", 40), ("nama_member", "Member", 160), ("nama_kelas", "Kelas", 150),
               ("jadwal", "Jadwal", 110), ("nama_trainer", "Trainer", 140),
               ("tgl_daftar", "Tgl Daftar", 90)]
    fields = [("id_member", "Member", "combo", True),
              ("id_kelas", "Kelas", "combo", True)]

    def combo_options(self, key):
        return member_model.options() if key == "id_member" else kelas_model.options()

    def save_new(self, d):
        pendaftaran_model.create(d["id_member"], d["id_kelas"])

    def save_update(self, id_, d):
        pendaftaran_model.update(id_, d["id_member"], d["id_kelas"])
