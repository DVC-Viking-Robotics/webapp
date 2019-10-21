"""
This script allows you to create a local database with a default admin user.

Run it with ``python -m tools.init_test_db``
"""

from werkzeug.security import generate_password_hash
from webapp.app import build_flask_app
from webapp.users import User, DB
from webapp.utils.super_logger import logger

# TODO: add force flag
if __name__ == "__main__":
    app = build_flask_app(use_local_db=True)

    with app.app_context():
        # Initialize the database with all the tables
        logger.info('Tools', 'Initializing database with needed tables...')
        DB.create_all()

        # Try to find the test admin user
        logger.info('Tools', 'Attempting to find default "admin" user...')
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user is None:
            logger.info('Tools', 'Default "admin" user not found! Creating...')
            # Add the test admin user
            admin = User(username='admin', password=generate_password_hash('admin'))

            # Save the user
            DB.session.add(admin)
            DB.session.commit()
        else:
            logger.info('Tools', 'Found default "admin" user!')

        logger.info('Tools', 'Note for admin user:')
        logger.info('Tools', "  Username: admin")
        logger.info('Tools', "  Password: admin")
