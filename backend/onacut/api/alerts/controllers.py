import datetime

from onacut import db, app
from flask import abort
from onacut.models import City, Alert
from flask_restful import Resource, fields
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from .parsers import alert_get_parser, AlertGetParser
from .fields import AlertGetResponseSchema

class AlertsApi(MethodResource, Resource):
    @doc(description='GET all Alerts.', tags=['Alerts'])
    @use_kwargs(AlertGetParser, location=("json"))
    @marshal_with(AlertGetResponseSchema(many=True))
    def get(self):
        args = alert_get_parser.parse_args()
        alert_id = args["id"]
        if alert_id:
            alert = Alert.query.get(alert_id)
            if not alert:
                abort(404)
            return [alert], 200
        
        alerts = Alert.query.all()
        
        return alerts, 200