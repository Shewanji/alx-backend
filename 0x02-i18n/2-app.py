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


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def greet() -> str:
    """
    Renders index.html template

    Returns:
        str: Rendered HTML content
    """
    return render_template('2-index.html')
