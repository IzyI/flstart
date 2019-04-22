import datetime
from main.database import db, CRUDMixin


class Tag(CRUDMixin, db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, index=True, default=0)
    slug = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name