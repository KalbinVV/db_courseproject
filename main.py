import os.path

from flask import Flask, render_template

from models import db, create_triggers
from pages import auth, users, profile, api, search, documents
from security import is_user_authed
from utils.housings_utils import get_housings_statistic
from utils.locations_utils import get_settlements, get_countries

app = Flask(__name__,
            template_folder=os.path.abspath('./web/html'),
            static_folder=os.path.abspath('./web/static'))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://user:pass@db/db"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)


@app.route('/')
def index() -> str:
    housings_types = [{'name': key,
                       'variables': item}
                      for key, item in get_housings_statistic().items()]

    return render_template('index.html', housings_types=housings_types,
                           countries=get_countries(),
                           is_authed=is_user_authed())


def main() -> None:
    with app.app_context():
        db.create_all()
        create_triggers()

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
        '/api/get_housings_rent_statistics': (api.get_housings_rent_statistics, ['GET']),
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
        '/update_profile': (profile.update_profile, ['POST']),
        '/update_record': (profile.update_record, ['POST']),
        '/rent_housing': (profile.rent_housing, ['POST', 'GET']),
        '/landlord_history': (profile.landlord_history, ['GET']),
        '/renter_history': (profile.renter_history, ['GET']),
        '/landlord_analytics': (profile.landlord_analytics, ['GET', 'POST']),
        # Search section
        '/search': (search.search_page, ['GET']),
        '/get_search_results': (search.get_search_result, ['GET']),
        # Documents
        '/get_document': (documents.get_document, ['GET'])
    }

    for routing, args in pages_routing.items():
        print(f'Page "{routing}" with name "{args[0].__name__}" registered with args: {args}')

        app.add_url_rule(routing, args[0].__name__, args[0], methods=args[1])

    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
