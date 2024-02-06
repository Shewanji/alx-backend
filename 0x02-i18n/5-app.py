#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, render_template, request
from flask_babel import Babel

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


def get_user(user_id: int) -> dict or None:
    """
    Get user details from the user database
    """
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Function to be executed before all other functions
    Finds the user if logged in and sets it as a global on flask.g.user
    """
    user_id = int(request.args.get('login_as', 0))
    g.user = get_user(user_id)


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages
    """
    if 'locale' in request.args and request.args['locale'] in Config.LANGUAGES:
        return request.args['locale']
    else:
        return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def greet() -> str:
    """
    Renders index.html template

    Returns:
        str: Rendered HTML content
    """
    return render_template('5-index.html')
