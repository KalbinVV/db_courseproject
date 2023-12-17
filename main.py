import os.path

from flask import Flask, render_template

from models import db
from pages import auth, users, profile, api, search
from security import is_user_authed
from utils.housings_utils import get_housings_statistic
from utils.locations_utils import get_settlements

app = Flask(__name__,
            template_folder=os.path.abspath('./web/html'),
            static_folder=os.path.abspath('./web/static'))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://user:pass@db/db"
db.init_app(app)


@app.route('/')
def index() -> str:
    housings_types = [{'name': key,
                       'variables': item}
                      for key, item in get_housings_statistic().items()]

    return render_template('index.html', housings_types=housings_types,
                           settlements=get_settlements(),
                           is_authed=is_user_authed())


def main() -> None:
    with app.app_context():
        db.create_all()

    pages_routing = {
        # Authorization section
        '/auth': (auth.auth, ['POST', 'GET']),
        '/register': (auth.register, ['POST', 'GET']),
        '/logout': (auth.logout, ['POST', 'GET']),
        # Users sections
        '/users/me': (users.users_me, ['GET']),
        # Api section
        '/api/get_settlements_by_country': (api.get_settlements_by_country, ['GET']),
        '/api/get_streets_by_settlement': (api.get_streets_by_settlement, ['GET']),
        '/api/add_housing': (api.add_housing, ['POST']),
        '/api/export_data': (api.export_data, ['GET']),
        '/api/get_streets_by_like_name': (api.get_streets_by_like_name, ['GET']),
        # Profiles section
        '/profile': (profile.profile, ['GET']),
        '/my_housings': (profile.my_housings, ['GET']),
        '/create_housing': (profile.create_housing, ['GET', 'POST']),
        '/view_housing': (profile.view_housing, ['GET']),
        '/remove_housing': (profile.remove_housing, ['PUT', 'GET']),
        '/change_housing': (profile.change_housing, ['GET', 'POST']),
        '/create_record': (profile.create_record, ['GET', 'POST']),
        '/view_record': (profile.view_record, ['GET']),
        '/activate_record': (profile.activate_record, ['GET']),
        '/hide_record': (profile.hide_record, ['GET']),
        # Search section
        '/search': (search.search_page, ['GET'])
    }

    for routing, args in pages_routing.items():
        print(f'Page "{routing}" with name "{args[0].__name__}" registered with args: {args}')

        app.add_url_rule(routing, args[0].__name__, args[0], methods=args[1])

    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
