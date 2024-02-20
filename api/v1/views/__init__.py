#!/usr/bin/python3
from flask import Blueprint, request


app_view = Blueprint('app_view', __name__, url_prefix='/api/v1')
app_view.secret_key = 'c213db81-85b4-49d3-a027-33722ef28d44'

from api.v1.views.index import *
from api.v1.views.user_api import *
from api.v1.views.response_api import *
from api.v1.views.survey_api import *