from flask import Blueprint, render_template, session, redirect, url_for

hub_bp = Blueprint("hub", __name__)

@hub_bp.route("/hub")
def hub():
    if "user" in session:
        print(session)
        return render_template("hub.html", username=session["user"]['userinfo']['name'])
    else:
        return redirect(url_for("login.login"))
