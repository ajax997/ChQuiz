from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__, url_prefix="auth")
@auth_bp.route("/login", methods=["POST"])
def login():
    return ""

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return ""