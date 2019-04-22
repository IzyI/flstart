from flask import Blueprint
from flask_restful import Api, Resource, url_for
api_bp = Blueprint('api', __name__, template_folder='templates')
api = Api(api_bp)

from . import views
