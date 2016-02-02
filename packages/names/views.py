# coding: utf-8

# Stdlib imports
import json

# Core Flask imports
from flask import Blueprint
from flask import request
from flask.views import MethodView

# Third-party app imports
from sqlalchemy import or_

# Imports from your apps
from init.database import db
from packages.utils.views import JSONMethodView
from .models import *
from .schemas import *


names = Blueprint('names', __name__, url_prefix='/api/names')


class BooksPublicListView(JSONMethodView):
    def get(self):
        names_q = Name.query.filter(
            Name.is_deleted == False
        ).order_by(Name.title)

        search_query = SearchQuery(q_ip=self.get_client_ip())

        category_id = request.args.get('category_id')
        if category_id:
            names_q = names_q.filter(
                Name.categories.any(Category.id.in_([category_id]))
            )
            category = Category.query.get(category_id)
            search_query.q_category = category.name

        q = request.args.get('q')
        if q:
            q = u'%{}%'.format(q)
            names_q = names_q.filter(
                or_(
                    Name.title.ilike(q),
                    Name.desc.ilike(q),
                    Name.notes.ilike(q),
                )
            )
            search_query.q_text = q

        gender = request.args.get('gender')
        if gender == 'male':
            search_query.q_male = True
            names_q = names_q.filter(
                Name.gender_male == True
            )
        elif gender == 'female':
            search_query.q_female = True
            names_q = names_q.filter(
                Name.gender_female == True
            )

        total = names_q.count()
        per_page = int(request.args.get('per_page', 20))
        page = int(request.args.get('page', 1))
        names_q = names_q.slice(
            (page - 1) * per_page,
            page * per_page
        )

        if page == 1:
            db.session.add(search_query)
            db.session.commit()

        if page * per_page < total:
            page += 1
        else:
            page = None

        data = NamesSchema().dump({
            'page': page,
            'total': total,
            'items': names_q
        }).data
        return self.render_response(data)

    @staticmethod
    def get_client_ip():
        x_forwarded_for = request.headers.getlist('X-Forwarded-For')
        if x_forwarded_for:
            ip = x_forwarded_for[0]
        else:
            ip = request.remote_addr
        return ip


class CategoriesPublicListView(JSONMethodView):
    def get(self):
        categories_q = Category.query.filter(
            Category.is_deleted == False
        ).order_by(Category.name)

        data = CategorySchema().dump(categories_q, many=True).data
        return self.render_response(data)


names.add_url_rule('', view_func=BooksPublicListView.as_view('names'))
names.add_url_rule('/categories', view_func=CategoriesPublicListView.as_view('names_categories'))
