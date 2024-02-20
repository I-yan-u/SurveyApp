from bcrypt import hashpw, checkpw, gensalt
from models import store
from models.user import User
from uuid import uuid4
import jwt
from api.v1.views import app_view
import base64
import binascii
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from functools import wraps
from flask import request


def _hash_password(password):
    """ Hash password """
    return hashpw(password.encode(), gensalt())


def _generate_uuid():
    return str(uuid4())


class Auth:
    """Auth class for survey app
    """
    def __init__(self):
        """ Initialize db """
        self._db = store

    def register_user(self, first_name, last_name, email, password, creator=False):
        """Register a new user based on given attributes.

        Args:
            email (String): Users email address.
            password (String): Users password.
            creator (Bool): Survey creator or not.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User already exists")
        except NoResultFound:
            hashdpw = _hash_password(password)
            user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=hashdpw,
                        creator=creator)
            user.save()
            return user
    
    def valid_login(self, email, password):
        """Validate login datails

        Args:
            email (string): Users email address
            password (string): Users password
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.password
            validate = checkpw(password.encode(), hashed_password.encode())
            return validate
        except NoResultFound:
            return False
        
    def create_session(self, email):
        """Generate a new session id

        Args:
            email (string): Users email address.
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            user.save()
            return user.session_id
        except NoResultFound:
            return None
    
    def get_user_from_session(self, session_id):
        """Get user from session id.

        Args:
            session_id (sting): Users session id.
        """
        try:
            if not session_id:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
    
    def destroy_session(self, user_id):
        """Destroy session id

        Args:
            session_id (string): Users session id.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            user.save()
        except NoResultFound:
            raise NoResultFound


class ProtoAuth:
    """Prototype class for Basic auth
    """
    def __init__(self):
        """ Initialize db """
        self._db = store

    def authorization_header(self, request=None):
        """Authorization content in HTTP header

        Args:
            request (_type_, optional): request header. Defaults to None.

        Returns:
            str: None
        """
        if request is None:
            return None
        auth = request.headers.get('Authorization')
        if auth is None:
            return None
        return auth

    def current_user(self, request=None):
        """Current user information
        """
        return None

#
# Basic auth implementation
#

class BasicAuth(ProtoAuth):
    """Auth class for survey app Utilizing Basic Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str):
        """Extract utf-8 format of the authorization header

        Args:
            authorization_header (str): base64 encoded auth header string

        Returns:
            str: utf-8 format of the authorization header
        """
        ah = authorization_header
        if ah is None or isinstance(ah, str) is False:
            return None
        if not ah.startswith('Basic '):
            return None
        return ah[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str):
        """Decode base64 authorization header

        Args:
            base64_authorization_header (str): base64 authorization header

        Returns:
            str: utf-8 encoded base64 authorization header
        """
        bah = base64_authorization_header
        if bah is None or not isinstance(bah, str):
            return None
        try:
            res = base64.b64decode(bah, validate=True)
            return res.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ):
        """EXtract user credentials from authentication header

        Args:
            str (str): decoded_base64_authorization_header
        """
        bbah = decoded_base64_authorization_header
        if not bbah or not isinstance(bbah, str):
            return None, None
        if ':' in bbah:
            email, password = bbah.split(':', 1)
            return email, password
        else:
            return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str):
        """Get user object from credentials

        Args:
            user_email (str): User email
            user_pwd (str): User pwrd
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = self._db.find_user_by(email=user_email)
            hashed_password = user.password
            validate = checkpw(user_pwd.encode(), hashed_password.encode())
            if validate:
                return user
            return None
        except NoResultFound:
            return None

    def current_user(self, request=None):
        """populates auth with current user data
        """
        user_email, password = self.extract_user_credentials(
                self.decode_base64_authorization_header(
                    self.extract_base64_authorization_header(
                        self.authorization_header(request)
                    )
                )
            )
        return self.user_object_from_credentials(
            user_email, password
        )
    
    def validate(self, request=None):
        user_email, user_pwd = self.extract_user_credentials(
            self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(
                    self.authorization_header(request)
                )
            )
        )
        print(user_email, user_pwd)
        if user_email is None or not isinstance(user_email, str):
            return False
        if user_pwd is None or not isinstance(user_pwd, str):
            return False
        try:
            user = self._db.find_user_by(email=user_email)
            hashed_password = user.password
            validate = checkpw(user_pwd.encode(), hashed_password.encode())
            return validate
        except NoResultFound:
            return False

#
# JWT auth implementation
#

class JWTAuth(ProtoAuth):
    """Auth class for survey app Utilizing Basic Auth
    """
    def get_auth_header(self,
                        authorization_header: str):
        """Extract utf-8 format of the authorization header

        Args:
            authorization_header (str): base64 encoded auth header string

        Returns:
            str: utf-8 format of the authorization header
        """
        ah = authorization_header
        if not ah.startswith('Bearer '):
            return None
        return ah[7:]

    def decode_auth_header(
            self,
            base64_authorization_header: str):
        """Decode base64 authorization header

        Args:
            base64_authorization_header (str): base64 authorization header

        Returns:
            str: utf-8 encoded base64 authorization header
        """
        bah = base64_authorization_header
        try:
            res = jwt.decode(bah, app_view.secret_key, algorithms=["HS256"])
            return res
        except Exception:
            return None
        
    def encode_token(self, data):
        if len(data) > 0:
            token = jwt.encode(data, app_view.secret_key)
            return token
        return None
    

jAuth = JWTAuth()

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token_data = jAuth.decode_auth_header(
            jAuth.get_auth_header(
                jAuth.authorization_header(request)
            )
        )
        
        try:
            user_email = token_data.get('email')
            user = jAuth._db.find_user_by(email=user_email)
            return func(user, *args, **kwargs)
        except (NoResultFound, Exception):
            return func(None, *args, **kwargs)
    return decorator