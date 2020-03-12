from models import *
from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """ 
    Decorate routes to require login

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if db.session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorator_function