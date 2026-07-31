from flask import Blueprint, jsonify, request
from flask import jsonify
from uuid import UUID
from services.collection_service import get_all_collection, get_all_collection_item_by_id
collection_bp = Blueprint("collection", __name__, url_prefix="/api/collection")
@collection_bp.route("/list", methods=["get"])
def get_collection():
    data = get_all_collection()
    return jsonify(data)

@collection_bp.route("/<uuid:collection_id>", methods=["GET"])
def get_collection_item(collection_id: UUID):
    # collection_id is a uuid.UUID object
    data = get_all_collection_item_by_id(str(collection_id), "425dd44f-45a2-45b4-923a-de8a17d39e5a")
    return jsonify(data)