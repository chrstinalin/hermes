"""about"""

from flask import Blueprint

aboutB = Blueprint('about', __name__)


@aboutB.route('/about')
def about():
    """about page"""
    return "<h1>about</h1>"
