#!/usr/bin/python3
from flask import Blueprint

app_view = Blueprint('app_view', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.user_api import *
from api.v1.views.response_api import *