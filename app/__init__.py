from flask import Flask
from config import config
from app.extensions import db, migrate, login_manager, mail

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    
    # Register Blueprints
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.blueprints.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.blueprints.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.blueprints.bible import bp as bible_bp
    app.register_blueprint(bible_bp)

    from app.blueprints.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.docs import bp as docs_bp
    app.register_blueprint(docs_bp, url_prefix='/docs')

    from flask import render_template
        
    configure_logging(app)
    
    # Create default admin inside app context
    with app.app_context():
        create_default_admin(app)
        
    return app

def create_default_admin(app):
    from app.models.user import User
    from app.extensions import db
    
    try:
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin12345')
            db.session.add(admin)
            db.session.commit()
            app.logger.info("Created default admin account: admin/admin12345")
    except Exception as e:
        app.logger.error(f"Failed to create default admin: {e}")
        db.session.rollback()

def configure_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler
    import os

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        # StreamHandler for Docker/Cloud logs
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask SaaS Boilerplate startup')
