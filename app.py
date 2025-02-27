from flask import Flask, url_for, session, redirect
from extensions import db
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.about import about_bp
from routes.apps import apps_bp
from routes.notes import notes_bp
from routes.admin import admin_bp, init_admin_db
from routes.files import files_bp
from routes.captcha import captcha_bp
from routes.retirement import retirement_bp
from routes.news import news_bp  # Import the new news blueprint
from models.user import User
from models.note import Note
from models.admin import Admin
from models.file import File  
from sqlalchemy import inspect


from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

oauth = OAuth(app)
oauth.register(
    'google',
    client_id  = os.getenv("GOOGLE_CLIENT_ID"),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URL"),
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        'scope': "openid email profile https://www.googleapis.com/auth/gmail.readonly"
    }
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boko_hacks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(hub_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(about_bp)
app.register_blueprint(apps_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(files_bp)
app.register_blueprint(captcha_bp)
app.register_blueprint(news_bp)
app.register_blueprint(retirement_bp)  

@app.route("/google-login")
def google_login():
    return oauth.google.authorize_redirect(redirect_uri=url_for("google_callback", _external = True))

@app.route("/signin-google")
def google_callback():
    token = oauth.google.authorize_access_token()
    session["user"] = token
    return redirect(url_for("hub.hub"))

def setup_database():
    """Setup database and print debug info"""
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            print("No existing tables found. Creating new tables...")
            db.create_all()
            
            init_admin_db()
        else:
            print("Existing tables found:", existing_tables)
            
            db.create_all()
            print("Updated schema with any new tables")
        
        for table in ['users', 'notes', 'admin_credentials', 'files']:
            if table in inspector.get_table_names():
                print(f"\n{table.capitalize()} table columns:")
                for column in inspector.get_columns(table):
                    print(f"- {column['name']}: {column['type']}")
            else:
                print(f"\n{table} table does not exist!")

if __name__ == "__main__":
    setup_database()  
    app.run(debug=True)