from main.database import db,CRUDMixin


class Pages(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(264), index=True, unique=True)
    url = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Url Page {}>'.format(self.url)



