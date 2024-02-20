from flask import Flask, render_template, request, redirect, url_for
from flask import make_response, session, flash, jsonify
import json
import re
import ast
from uuid import uuid4
from models import store
from models.user import User
from models.survey import Survey
from models.response import Response
from web_app.auth import Auth
from sqlalchemy.orm.exc import NoResultFound


auth = Auth()
app = Flask(__name__)
app.secret_key = 'surveyapp-2023-alx-cohort11'


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    store.close()


def check_session():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session(session_id)
    if user:
        return True
    return False


def user_data():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session(session_id)
    if user:
        return user
    return None


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    return render_template('index.html')
    

@app.route('/survey', methods=['GET'], strict_slashes=False)
def survey():
    return render_template('survey.html')


@app.route('/response/<sId>', methods=['GET'], strict_slashes=False)
def response(sId):
    if check_session() == False:
        return redirect(url_for("login"))
    user = user_data()
    survey = store.find_survey_id(id=sId)
    form = request.form
    send = {**form}
    send = json.dumps(send)
    response_data = {
        'users_id':user.id,
        'survey_id': sId,
        'title': survey.title,
        'response': send
        }
    res = Response(**response_data)
    res.save()
    return render_template('thank_you.html', user=user)


@app.route('/responses/', methods=['GET'], strict_slashes=False)
def responses():
    return render_template('responses.html')


@app.route('/create_survey', methods=['GET'], strict_slashes=False)
def create_survey():
    return render_template('create_survey.html')


@app.route('/about', methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html')


@app.route('/thank_you', methods=['GET'], strict_slashes=False)
def thanks():
    return render_template('thank_you.html')


@app.route("/login", methods=["GET"], strict_slashes=False)
def login():
    return render_template('login.html')


@app.route('/signup', methods=['GET'], strict_slashes=False)
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    app.run(port=port, host=host, debug=True)
