#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, format_time
import pytz
from datetime import datetime

app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    Config class for Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Get user details from the user database
    """
    user_id = request.args.get("login_as")
    if not user_id:
        return None
    for id, user in users.items():
        if id == int(user_id):
            return user
    return None


@app.before_request
def before_request():
    """
    Function to be executed before all other functions
    Finds the user if logged in and sets it as a global on flask.g.user
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages
    """
    if 'locale' in request.args and request.args['locale'] in Config.LANGUAGES:
        return request.args['locale']
    elif g.user and g.user['locale'] in Config.LANGUAGES:
        return g.user['locale']
    else:
        return request.accept_languages.best_match(Config.LANGUAGES)


@babel.timezoneselector
def get_timezone():
    """determines the timezone to be used"""
    url_timezone = request.args.get("timezone")
    if url_timezone:
        try:
            pytz.timezone(url_timezone)
            return url_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user and g.user.get("timezone"):
        return g.user.get("timezone")
    return Config.BABEL_DEFAULT_TIMEZONE


@app.route('/')
def greet() -> str:
    """
    Renders index.html template

    Returns:
        str: Rendered HTML content
    """
    time = datetime.utcnow()
    return render_template('index.html', user=g.user, time=time)
