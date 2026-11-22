from models import trainer_model
from views.base_view import BaseCrudView


class TrainerView(BaseCrudView):
    title = "Data Trainer"
    subtitle = "Daftar trainer beserta spesialisasi dan kontaknya."
    accent = "#00897B"
    model = trainer_model
    columns = [("id", "ID", 50), ("nama", "Nama", 200),
               ("spesialisasi", "Spesialisasi", 250), ("no_telp", "No. Telp", 150)]
    fields = [("nama", "Nama Trainer", "entry", True),
              ("spesialisasi", "Spesialisasi", "entry", False),
              ("no_telp", "No. Telepon", "entry", False)]

    def save_new(self, d):
        trainer_model.create(d["nama"], d["spesialisasi"], d["no_telp"])

    def save_update(self, id_, d):
        trainer_model.update(id_, d["nama"], d["spesialisasi"], d["no_telp"])
