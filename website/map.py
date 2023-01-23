"""map"""

from flask import Blueprint, render_template

mapB = Blueprint('map', __name__)


@mapB.route('/map')
def map():
    """map page"""
    return render_template("map.html")
