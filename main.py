import os.path

from flask import Flask, render_template

from models import db
from pages import auth, users, api, profiles

app = Flask(__name__,
            template_folder=os.path.abspath('./web/html'),
            static_folder=os.path.abspath('./web/static'))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://user:pass@db/db"
db.init_app(app)


@app.route('/')
def index() -> str:
    return render_template('index.html')


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
        '/api/housings_statistic': (api.housings_statistic, ['GET']),
        # Profiles section
        '/profile': (profiles.my_profile, ['GET'])
    }

    for routing, args in pages_routing.items():
        print(f'Page "{routing}" registered with args: {args}')

        app.add_url_rule(routing, routing[1:], args[0], methods=args[1])

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
