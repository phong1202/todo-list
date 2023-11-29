from flask import Flask, Blueprint, jsonify, render_template, abort, session
from config import Config

from app.extensions import db, migrate, login

def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Blueprints
    from app.Blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.Blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Routes
    @app.route('/', methods=['GET'])
    def home():
        app_config = app.config.copy()
        app_config['PERMANENT_SESSION_LIFETIME'] = str(app.config.get('PERMANENT_SESSION_LIFETIME'))
        return jsonify(app_config)
    login.login_view = 'auth.login'

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', error=404)
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html', error=500)
    @app.route('/500')
    def error500():
        abort(500)
    
    return app
