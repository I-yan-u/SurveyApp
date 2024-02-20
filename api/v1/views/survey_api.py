from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_view
from api.v1.views.pager import Pager
import json
from models import store
from models.user import User
from models.response import Response
from models.survey import Survey
from api.v1.auth.auth import Auth, BasicAuth, JWTAuth, token_required
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

jAuth = JWTAuth()

def checkFile(file):
    if file.get('title') is None:
        return {'error': 'Title missing'}, 400
    if file.get('description') is None:
        return {'error': 'Description missing'}, 400
    if file.get('form') is None:
        return {'error': 'Form missing'}, 400
    
    new_dict = {
        'title': file.get('title'),
        'description': file.get('desc') or file.get('description'),
        'form': file.get('form')
    }
    return new_dict, 200


@app_view.route('/create_survey', methods=['POST'], strict_slashes=False)
@token_required
def create_survey(user):
    forms = request.get_json()
    print(forms)
    new_survey = Survey(creators_id=user.id,
                            title=forms.get('title'),
                            description=forms.get('description'),
                            form=json.dumps(forms.get('form')))
    new_survey.save()
    return make_response(jsonify({'survey_id': new_survey.id}), 200)


@app_view.route('/upload_json', methods=['POST'], strict_slashes=False)
@token_required
def upload_json(user):
    if not user:
        return make_response(jsonify({'error': 'Unauthorized',
        'message': 'User not signed in'}), 401)
    if user.creator != True:
        return make_response(jsonify({'error': 'Unauthorized',
        'message': 'User not a creator'}), 401)

    file = request.get_json('myfile')
    data, data_stat = checkFile(file)
    if data_stat != 200:
        return make_response(jsonify(data), data_stat)
    new_survey = Survey(creators_id=user.id,
                            title=data.get('title'),
                            description=data.get('description'),
                            form=json.dumps(data.get('form')))
    new_survey.save()
    return make_response(jsonify({'survey_id': new_survey.id}), 200)


@app_view.route('/survey', methods=['GET'], strict_slashes=False)
@token_required
def survey(user):
    if user:
        survey_link = request.args.get('survey_link')
        if len(survey_link) > 8:
            survey_id = survey_link.split('/')[-1]
        else:
            survey_id = survey_link
        try:
            survey = store.find_survey_id(id=survey_id)
            survey_form = json.loads(survey.form)
            return make_response(jsonify({
                'survey': survey.to_dict(),
                'form': survey_form}),
                200)
        except NoResultFound:
            return make_response(jsonify({'error': 'No survey found'}), 404)
    else:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)