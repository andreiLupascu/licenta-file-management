from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.helpers import upload, retrieve, verify_can_upload, verify_can_download

app = Blueprint("file_management", __name__, url_prefix="")


@app.route("/api/files/<file_type>/<directory>", methods=['POST'])
@jwt_required
def upload_file(file_type, directory):
    # NEEDS form-data parameter with name = 'file' and value being the chosen file
    # <file_type> is one of: 'conference_logo', 'conference_description', 'article'
    # <directory> is either name of the article or name of the conference
    try:
        verify_can_upload(get_jwt_identity())
        response, status_code = upload(request, file_type, directory)
        return jsonify({"msg": response}), status_code
    except TypeError:
        return jsonify({"msg": "Invalid file"}), 400


@app.route("/api/files/<file_type>/<directory>/<file_name>", methods=['GET'])
def retrieve_file(file_type, directory, file_name):
    # <file_type> is one of: 'conference_logo', 'conference_description', 'article_paper', 'article_abstract'
    # <directory> is either name of the article or name of the conference
    verify_can_download(get_jwt_identity())
    return retrieve(file_type, directory, file_name)
