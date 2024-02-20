from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_view
from api.v1.views.pager import Pager
from models import store
import json
from models.user import User
from models.response import Response
from api.v1.auth.auth import JWTAuth, token_required
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

auth = JWTAuth()


@app_view.route('/response/<sid>', methods=['GET'], strict_slashes=False)
@token_required
def get_responses(user, sid):
    """ Get all responses for a survey """
    ind = request.args.get('index')
    if not user:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)
    if user.creator != True:
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    creators_id = user.id
    try:
        response = store.find_response(creators_id, sid)
        pager = Pager(response)
        # pager.dataset(response)
        resp = pager.get_hyper_index(int(ind))
        print(resp)
    except NoResultFound:
        return make_response(jsonify({'error': 'No survey or response found'}), 400)
    except InvalidRequestError:
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    return make_response(jsonify(resp), 200)


@app_view.route('/response/<sid>/<rid>', methods=['GET'], strict_slashes=False)
@token_required
def get_unique_res(user, sid, rid):
    """ Get all responses for a survey """
    if not user:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)
    if user.creator != True:
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    creators_id = user.id
    try:
        response = store.find_unique_response(creators_id, sid, rid)
    except NoResultFound:
        return make_response(jsonify({'error': 'Survey not found'}), 400)
    except InvalidRequestError:
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    return make_response(jsonify(response), 200)


@app_view.route('/submit_response/<sid>', methods=['POST'], strict_slashes=False)
@token_required
def submit_response(user, sId):
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
    return make_response(jsonify({'message': 'Done'}), 200)