from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_view
from api.v1.views.pager import Pager
from models import store
from models.user import User
from models.response import Response
from web_app.auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

auth = Auth()


@app_view.route('/response/<sid>', methods=['GET'], strict_slashes=False)
def get_responses(sid):
    """ Get all responses for a survey """
    session_id = request.headers.get('custom-header')
    ind = request.args.get('index')
    head = request.headers
    # print(head)
    # print(session_id)
    user = auth.get_user_from_session(session_id)
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
def get_unique_res(sid, rid):
    """ Get all responses for a survey """
    session_id = request.headers.get('custom-header')
    user = auth.get_user_from_session(session_id)
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