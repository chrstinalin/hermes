"""views"""

from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    """homepage"""
    return render_template("homepage.html")
