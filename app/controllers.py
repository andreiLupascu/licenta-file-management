from flask import Blueprint, request, jsonify

from app.helpers import upload, retrieve

app = Blueprint("file_management", __name__, url_prefix="")


@app.route("/api/files/<file_type>/<directory>", methods=['POST'])
def upload_file(file_type, directory):
    # NEEDS form-data parameter with name = 'file' and value being the chosen file
    # <file_type> is one of: 'conference_logo', 'conference_description', 'article'
    # <directory> is either name of the article or name of the conference
    try:
        response, status_code = upload(request, file_type, directory)
        return jsonify({"msg": response}), status_code
    except TypeError:
        return jsonify({"msg": "Invalid file"}), 400


@app.route("/api/files/<file_type>/<directory>/<file_name>", methods=['GET'])
def retrieve_file(file_type, directory, file_name):
    # <file_type> is one of: 'conference_logo', 'conference_description', 'article'
    # <directory> is either name of the article or name of the conference
    return retrieve(file_type, directory, file_name)
