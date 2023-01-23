"""views"""

from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    """homepage"""
    return render_template("homepage.html")
