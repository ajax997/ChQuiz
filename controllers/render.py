from flask import Blueprint, jsonify, request, render_template
from flask import jsonify
from uuid import UUID

learning_bp = Blueprint("learning", __name__, url_prefix="/learning")
@learning_bp.route("/collection", methods=["get"])
def get_collection():
    return render_template("collections.html")

@learning_bp.route("/collection/<uuid:collection_id>", methods=["GET"])
def get_collection_item(collection_id: UUID):
    # collection_id is a uuid.UUID object
    return render_template("collection_details.html")

@learning_bp.route("/collection/<uuid:collection_id>/quiz/matching", methods=["GET"])
def mad_matching(collection_id: UUID):
    # collection_id is a uuid.UUID object
    return render_template("mad_matching.html")