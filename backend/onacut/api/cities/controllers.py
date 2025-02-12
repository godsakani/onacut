from flask import abort
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from onacut.models import City

from .fields import CityGetResponseSchema
from .parsers import CityGetParser, city_get_parser


class CitiesApi(MethodResource, Resource):
    @doc(description="GET all Cities.", tags=["Cities"])
    @use_kwargs(CityGetParser, location=("json"))
    @marshal_with(CityGetResponseSchema(many=True))
    def get(self):
        cities = []
        try:
            args = city_get_parser.parse_args()
            city_id = args.get("id", None)
            if city_id:
                city = City.query.get(city_id)
                if not city:
                    abort(404)
                return [city], 200

            cities = City.query.all()
            return cities, 200

        except BadRequest:
            # FIXME , this is a temp solution 9we should not return results
            # on bad request +that's means no arguments got passed or a weird argument was
            # passed so that the json parsing crashed
            cities = City.query.all()

        return cities, 200
