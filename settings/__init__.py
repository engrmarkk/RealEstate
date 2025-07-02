from flask import Flask, render_template
from configs import app_configs
from constants import CONFIG_NAME
from routes.authentication import authentication_blp
from routes.users import users_blp
from routes.admin import admin_blp
from routes.errors import error_blp
from routes.transactions import transactions_blp
from extensions import login_manager, db, migrate
from models import (
    Users,
    UserProfile,
    Agent,
    CommissionRateChange,
    CommissionRecord,
    Favorite,
    Tour,
    Inquiry,
    Property,
    HouseDetails,
    LandDetails,
    PropertyImages,
    Newsletter,
    PropertyView,
    Contact,
    Transaction,
    PropertyPurchased,
    AgentWallet,
    AgentBankDetails,
)
from middlewares import register_middlewares


def create_app(config_name=CONFIG_NAME):
    app = Flask(__name__)

    app.config.from_object(app_configs[config_name])

    register_middlewares(app)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # for current user
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    # 500 internal server error
    @app.errorhandler(500)
    def internal_server_error(e):
        # TODO
        """
        send the errro message to an email
        """
        return render_template("error_pages/500.html"), 500

    # 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error_pages/404.html"), 404

    app.register_blueprint(authentication_blp)
    app.register_blueprint(users_blp)
    app.register_blueprint(admin_blp, url_prefix="/admin")
    app.register_blueprint(error_blp, url_prefix="/error")
    app.register_blueprint(transactions_blp, url_prefix="/transactions")
    return app
