# coding: utf-8

# Stdlib imports
import csv

# Core Flask imports

# Third-party app imports
from flask.ext.script import Command
from dateutil import parser

# Imports from your apps
from init.database import db
from .models import Name, Category, names_categories_association_table


class AddNames(Command):
    def run(self):
        db.session.query(names_categories_association_table).filter().delete(synchronize_session=False)

        Name.query.delete()
        Category.query.delete()

        db.session.add(Category(id=1, name=u'Санскритское', symbol=u'अ'))
        db.session.add(Category(id=2, name=u'Без категории', symbol=u''))
        db.session.add(Category(id=3, name=u'Тибетское', symbol=u'༁'))
        db.session.add(Category(id=4, name=u'Бурятское', symbol=u'ө'))
        db.session.commit()

        with open('names.csv', 'rb') as f:
            reader = csv.reader(f, delimiter='#', quotechar='$')
            for row in reader:
                if not row:
                    continue
                if row[0] == 'id':
                    continue
                title = row[1]
                desc = row[2]
                created_at = row[4]
                updated_at = row[5]
                notes = row[7]
                category_id = row[8]
                gender_male = row[9] == 't'
                gender_female = row[10] == 't'

                name = Name(
                    title=title,
                    desc=desc,
                    created_at=parser.parse(created_at),
                    updated_at=parser.parse(updated_at),
                    notes=notes,
                    gender_male=gender_male,
                    gender_female=gender_female
                )
                category = Category.query.get(category_id)
                name.categories.append(category)

                db.session.add(name)
                db.session.commit()
