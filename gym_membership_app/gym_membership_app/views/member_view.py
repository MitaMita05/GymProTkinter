from datetime import date, datetime

from models import member_model
from views.base_view import BaseCrudView


class MemberView(BaseCrudView):
    title = "Data Member"
    subtitle = "Kelola data anggota gym, dari pendaftaran sampai status keanggotaan."
    accent = "#1E88E5"
    model = member_model
    columns = [("id", "ID", 40), ("no_member", "No. Member", 90), ("nama", "Nama", 150),
               ("jenis_kelamin", "JK", 35), ("no_telp", "No. Telp", 110),
               ("email", "Email", 150), ("tgl_daftar", "Tgl Daftar", 90),
               ("status", "Status", 80)]
    fields = [("no_member", "No. Member", "entry", True),
              ("nama", "Nama Lengkap", "entry", True),
              ("jenis_kelamin", "Jenis Kelamin", "combo", True),
              ("no_telp", "No. Telepon", "entry", False),
              ("email", "Email", "entry", False),
              ("tgl_daftar", "Tgl Daftar (YYYY-MM-DD)", "entry", True),
              ("alamat", "Alamat", "entry", False)]

    def combo_options(self, key):
        return [("L", "Laki-laki"), ("P", "Perempuan")]

    def on_form_cleared(self):
        self.widgets["tgl_daftar"].insert(0, date.today().isoformat())

    def extra_validate(self, d):
        try:
            datetime.strptime(d["tgl_daftar"], "%Y-%m-%d")
        except ValueError:
            return "Format tanggal harus YYYY-MM-DD."
        if d["email"] and "@" not in d["email"]:
            return "Format email tidak valid."
        return None

    def _args(self, d):
        return (d["no_member"], d["nama"], d["jenis_kelamin"], d["no_telp"],
                d["email"], d["alamat"], d["tgl_daftar"])

    def save_new(self, d):
        member_model.create(*self._args(d))

    def save_update(self, id_, d):
        member_model.update(id_, *self._args(d))
