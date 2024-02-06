#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def greet() -> str:
    """
    Renders index.html template

    Returns:
        str: Rendered HTML content
    """
    return render_template('0-index.html')
