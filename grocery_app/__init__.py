from flask_login import LoginManager
from grocery_app.extensions import app, db
from grocery_app.models import User
from flask_bcrypt import Bcrypt
from grocery_app.routes import auth, main

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


# Register the new blueprint from routes.py
app.register_blueprint(main)
app.register_blueprint(auth)

# with app.app_context():
#   db.create_all()
