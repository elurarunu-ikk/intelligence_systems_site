from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from urllib.parse import urlparse
from ...models import User
from ...extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/login")
def login():
    next_url = request.args.get("next", "")
    return render_template("admin/login.html", next=next_url)

@auth_bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    next_url = request.form.get("next", "")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password) or not user.is_admin:
        flash("Invalid credentials.", "danger")
        return redirect(url_for("auth.login", next=next_url))

    login_user(user, remember=True)

    # Safety: only allow relative next url
    if next_url and urlparse(next_url).netloc == "":
        return redirect(next_url)

    return redirect(url_for("admin.index"))

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("public.home"))
