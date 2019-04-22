import datetime
from main.database import db, CRUDMixin
from main.tags.models import Tag

article_tags_meta = db.Table(
    'article_tags',
    db.Model.metadata,
    db.Column('article_id_2', db.Integer, db.ForeignKey('article_model.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    extend_existing=True
)


class Articles(CRUDMixin, db.Model):
    __tablename__ = 'article_model'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, name="Название", nullable=False)
    url = db.Column(db.String, name="Url", nullable=False)
    anons = db.Column(db.Text, name="Анонс")
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    tags = db.relationship(Tag, secondary=article_tags_meta)
    author = db.Column(db.String, name="Автор")
    text = db.Column(db.Text, name="Результат")
    image = db.Column(db.String, nullable=False)
