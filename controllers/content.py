from flask import Blueprint, jsonify, request, render_template
from flask import jsonify
from uuid import UUID

from services.content_service import get_all_example_by_content

content_bp = Blueprint("content", __name__, url_prefix="/api/content")


@content_bp.route("/example/<string:content>", methods=["GET"])
def get_collection_item(content):
    # collection_id is a uuid.UUID object
    return jsonify(get_all_example_by_content(content))