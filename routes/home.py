from flask import Blueprint, render_template, session
import json
home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html", session=session.get("user") )
