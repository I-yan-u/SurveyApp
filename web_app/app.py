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


@app.route("/", methods=["GET", "POST"], strict_slashes=False)
def index():
    return render_template('index.html')
# session_id = request.cookies.get('session_id')
# user = auth.get_user_from_session(session_id)
# if user:
#     return render_template('index.html', user=user)
# else:
#     return redirect(url_for("login"))
    

@app.route('/survey', methods=['GET'], strict_slashes=False)
def survey():
    return render_template('survey.html')
    # if check_session() == False:
    #     return redirect(url_for("login"))
    # if not sId:
    #     user = user_data()
    #     if request.method == 'POST':
    #         survey_link = request.form.get('survey-link')
    #         if len(survey_link) > 8:
    #             survey_id = survey_link.split('/')[-1]
    #         else:
    #             survey_id = survey_link
    #         try:
    #             survey = store.find_survey_id(id=survey_id)
    #             survey_form = json.loads(survey.form)
    #             return render_template('survey.html',
    #                                 survey=survey,
    #                                 survey_form=survey_form,
    #                                 user=user)
    #         except NoResultFound:
    #             return redirect('/')
    #     if request.method == 'GET':
    #         survey_id = request.args.get('id')
    #         survey = store.find_survey_id(id=survey_id)
    #         survey_form = json.loads(survey.form)
    #         return render_template('survey.html',
    #                             survey=survey,
    #                             survey_form=survey_form,
    #                             user=user)
    # else:
    #     survey = store.find_survey_id(id=sId)
    #     survey_form = json.loads(survey.form)
    #     user = user_data()
    #     return render_template('survey.html',
    #                         survey=survey,
    #                         survey_form=survey_form,
    #                         user=user)


@app.route('/response/<sId>', methods=['POST'], strict_slashes=False)
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
    # if check_session() == False:
    #     return redirect(url_for("login"))
    # user = user_data()
    # if user.creator == False:
    #     logout()
    #     flash('Sign Up as a creator!')
    #     return redirect(url_for('login'))
    # return render_template('responses.html', user=user)


@app.route('/create_survey', methods=['GET','POST'], strict_slashes=False)
def create_survey():
    return render_template('create_survey.html')
    # session_id = request.cookies.get('session_id')
    # user = auth.get_user_from_session(session_id)
    # if not check_session():
    #     return redirect(url_for('login'))
    # if not user.creator:
    #     logout()
    #     flash('Sign Up as a creator!')
    #     return redirect('/login')
    # if request.method == 'GET':
    #     return render_template('create_survey.html', user=user)
    # if request.method == 'POST':
    #     form = request.form
    #     title = form['title']
    #     desc = form['description']
        
    #     forms = []
    #     count = 1
    #     print(form)
    #     for k, v in form.items():
    #         if k.startswith(f'Question-{count}'):
    #             count += 1
    #             v = v.replace('\r\n', ', ')

    #             # Get the option type.
    #             re_pattern = r'text:|radio:|choices:|checkbox:|date:|password:|range:'
    #             option_type = re.search(re_pattern, v)
    #             if option_type:
    #                 option = option_type.group().strip(':')
    #             else:
    #                 return "Invalid Input"

    #             #  Extract the matching string.
    #             match_pattern = rf"question: (.+), {re.escape(option)}: (.+)"
    #             match = re.match(match_pattern, v)

    #             if match:
    #                 question = match.group(1).strip()
    #                 choices_str = match.group(2).strip()
    #                 try:
    #                     options = ast.literal_eval(choices_str)
    #                     if options is None:
    #                         options = []
    #                 except Exception as e:
    #                     options = choices_str

    #                 if option == 'range':
    #                     options = options.split('to')
    #                 to_dict = {'question': question, f'{option}': options}
    #                 print(to_dict)
    #                 forms.append(to_dict)
    #     new_survey = Survey(creators_id=user.id,
    #                         title=title,
    #                         description=desc,
    #                         form=json.dumps(forms))
    #     new_survey.save()
    #     return render_template('generate_link.html',
    #                            id=new_survey.id,
    #                            link=f'http://0.0.0.0:5000/survey/{new_survey.id}')


@app.route('/about', methods=['GET'], strict_slashes=False)
def about():
    user = user_data()
    if user:
        return render_template('about.html', user=user)
    else:
        return render_template('about.html')


@app.route('/thank_you', methods=['GET'], strict_slashes=False)
def thanks():
    user = user_data()
    return render_template('thank_you.html', user=user)


@app.route("/login", methods=["GET"], strict_slashes=False)
def login():
    return render_template('login.html')
    # if request.method == "POST":
    #     email = request.form.get("email")
    #     password = request.form.get("password")
    #     validate = auth.valid_login(email, password)
    #     if validate:
    #         session_id = auth.create_session(email)
    #         response = make_response(redirect("/"))
    #         response.set_cookie('session_id', session_id)
    #         return response
    #     flash('Invalid Email or Password')
    #     return render_template("login.html")
    # else:
    #     session_id = request.cookies.get('session_id')
    #     user = auth.get_user_from_session(session_id)
    #     if user:
    #         return redirect(url_for('index'))
    #     else:
            # return render_template('login.html', unsuccessful=True)


@app.route('/signup', methods=['GET'], strict_slashes=False)
def signup():
    return render_template('signup.html')
    # if not check_session():
    #     if request.method == 'POST':
    #         first_name = request.form.get('first-name')
    #         last_name = request.form.get('last-name')
    #         email = request.form.get('email')
    #         confirm_password = request.form.get('confirm-password')
    #         password = request.form.get('password')
    #         if confirm_password != password:
    #             flash("Password doesn't match")
    #             return render_template('signup.html')

    #         creator = request.form.get('creator', False)
    #         creator = True if creator else False
    #         user = auth.register_user(first_name=first_name,
    #                                   last_name=last_name,
    #                                   email=email, password=password,
    #                                   creator=creator)
    #         return redirect(url_for('login'))
    #     if request.method == 'GET':
    #         return render_template('signup.html')
    # return redirect(url_for('index'))


@app.route('/logout', methods=['DELETE', 'GET'], strict_slashes=True)
def logout():
    user = user_data()
    if not user:
        return redirect('/login')
    else:
        auth.destroy_session(user.id)
        return redirect('/login')


if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    app.run(port=port, host=host, debug=True)
