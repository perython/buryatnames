# coding: utf-8

# Stdlib imports
import json

# Core Flask imports
from flask import Response
from flask.views import MethodView

# Third-party app imports

# Imports from your apps


__all__ = (
    'JSONMethodView',
)


class JSONMethodView(MethodView):
    @staticmethod
    def render_response(data, status=200, headers={}):
        return Response(
            status=status,
            response=json.dumps(data),
            content_type='application/json',
            headers=headers
        )
