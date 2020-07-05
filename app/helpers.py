import os

from flask import current_app, send_from_directory, jsonify
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_FILE_DIRECTIVES = {'conference_logo', 'conference_description', 'article_paper', 'article_abstract'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_logo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[-3:]


def upload(request, file_type, directory):
    upload_directory = current_app.config['UPLOAD_DIRECTORY']
    if file_type not in ALLOWED_FILE_DIRECTIVES:
        return "File type is not set correctly, available file types are: " + ', '.join(ALLOWED_FILE_DIRECTIVES), 400
    if 'file' not in request.files:
        return "No files selected for upload.", 400
    file = request.files['file']
    if file.filename == '':
        return "No files selected for upload.", 400
    if file and allowed_file(file.filename):
        sep = '/'
        filename = secure_filename(directory + '_' + file_type + os.path.splitext(file.filename)[1])
        superdirectory = ""
        if 'article' in file_type:
            superdirectory = 'articles'
        elif 'conference' in file_type:
            superdirectory = 'conferences'
        path_to_upload = upload_directory + os.path.sep + superdirectory + os.path.sep + directory + os.path.sep + file_type + os.path.sep
        if file_type in ['conference_description', 'article_paper', 'article_abstract']:
            if file.mimetype not in {'text/plain', 'application/pdf'}:
                return "Invalid mime type for description.", 400
        elif file_type == 'conference_logo':
            if file.mimetype not in {'image/png', 'image/jpg', 'image/jpeg'}:
                return "Invalid mime type for logo.", 400
        if not os.path.exists(path_to_upload):
            os.makedirs(os.path.dirname(path_to_upload))
        # logica legata de salvat fisiere in conferinta, de extins if needed
        file.save(os.path.join(path_to_upload, filename))
        return file_type + sep + filename, 200


def retrieve(file_type, directory, file_name):
    if file_type not in ALLOWED_FILE_DIRECTIVES:
        return "File type is not set correctly, available file types are: " + ', '.join(ALLOWED_FILE_DIRECTIVES), 400
    superdirectory = ""
    if 'article' in file_type:
        superdirectory = 'articles'
    elif 'conference' in file_type:
        superdirectory = 'conferences'
    upload_directory = current_app.config[
                           'UPLOAD_DIRECTORY'] + os.path.sep + superdirectory + os.path.sep + directory + os.path.sep + file_type + os.path.sep
    try:
        return send_from_directory(upload_directory, filename=file_name, as_attachment=True)
    except Exception:
        return jsonify({"msg": "File was not found."}), 404


def verify_can_upload(current_user):
    if 'ADMINISTRATOR' not in current_user['roles'] and 'PROGRAM_COMMITTEE' not in current_user['roles']:
        return jsonify({"msg": "Invalid role for request"}), 403


def verify_can_download(current_user):
    if not current_user['roles']:
        return jsonify({"msg": "Invalid role for request"}), 403
