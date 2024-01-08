from bcrypt import hashpw, checkpw, gensalt
from models import store
from models.user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

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
