"""contact"""

from flask import Blueprint

contactB = Blueprint('contact', __name__)


@contactB.route('/contact')
def contact():
    """contact page"""
    return "<h1>contact</h1>"
