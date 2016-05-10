# coding: utf-8

# Stdlib imports

# Core Flask imports

# Third-party app imports

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel


__all__ = (
    'Category',
    'Name',
    'SearchQuery',
)


names_categories_association_table = db.Table(
    'names_categories_association',
    db.Model.metadata,
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('name_id', db.Integer, db.ForeignKey('name.id'), primary_key=True)
)


class Category(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'category'

    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(8))

    is_deleted = db.Column(db.Boolean, default=False)


class Name(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'name'

    categories = db.relationship(
        'Category', secondary=names_categories_association_table,
        backref=db.backref('names')
    )

    title = db.Column(db.String(512), nullable=False)
    desc = db.Column(db.Text)
    notes = db.Column(db.Text)
    gender_male = db.Column(db.Boolean, default=True)
    gender_female = db.Column(db.Boolean, default=True)

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


class SearchQuery(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'search_query'

    q_text = db.Column(db.String(255))
    q_male = db.Column(db.Boolean, default=False)
    q_female = db.Column(db.Boolean, default=False)
    q_category = db.Column(db.Text)
    q_ip = db.Column(db.String(128))

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
