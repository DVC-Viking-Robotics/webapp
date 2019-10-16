"""
This script allows you to create a local database with a default admin user.

Run it with ``python -m tools.init_test_db``
"""

# pylint: disable=invalid-name

from werkzeug.security import generate_password_hash
from webapp.app import build_flask_app
from webapp.users import User, DB

# TODO: add force flag
if __name__ == "__main__":
    app = build_flask_app(use_local_db=True)

    with app.app_context():
        # Initialize the database with all the tables
        print('Initializing database with needed tables...', end='')
        DB.create_all()
        print('done!')

        # Try to find the test admin user
        print('Attempting to find default "admin" user...')
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user is None:
            print('Default "admin" user not found! Creating...', end='')
            # Add the test admin user
            admin = User(username='admin', password=generate_password_hash('admin'))

            # Save the user
            DB.session.add(admin)
            DB.session.commit()
            print('done!')
        else:
            print('Found default "admin" user!')

        print('Note for admin user:')
        print("  Username: admin")
        print("  Password: admin")
