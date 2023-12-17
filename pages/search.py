from flask import render_template

from utils.comforts_utils import get_comforts
from utils.housings_utils import get_housings_types


def search_page():
    return render_template('search.html', housings_types=get_housings_types(),
                           comforts=get_comforts())
