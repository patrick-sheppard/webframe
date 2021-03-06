"""
Session handling middleware.
Should be seperated into small operations so user can pick and choose
how to use it.
"""

from webframe.core.http.session import Session
from webframe.utils import errors


def fetch_or_create_session(request, response):
    """Create a new session of get the session if it exists."""
    request.session = Session(request)

def set_session_token_on_response(request, response):
    """Set the session token."""
    request.session.set_response_session_token(response)

def check_csrf_on_post(request, response):
    """
    Check the existence or validity of a csrf token in on post.
    Checks request.json if content type is application/json
    """
    if request.method.upper() == 'POST':
        token = request.post('_token')
        if token is None and request.content_type == 'application/json':
            token = request.get_json('_token')
        if not request.session.check_csrf(token):
            errors.abort(401, 'Invalid form request.')

def session_commit(request, response):
    """
    Commit the session at the end of the request.
    This is designed to be run at GLOBAL_AFTER_MIDDLEWARE.
    """
    request.session.commit()

