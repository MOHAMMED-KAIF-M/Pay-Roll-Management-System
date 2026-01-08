from flask import session, redirect

def login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def authenticate(username, password):
    return username == "admin" and password == "admin"
