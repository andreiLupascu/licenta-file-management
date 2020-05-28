import os

from flask import current_app, send_from_directory, jsonify
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_FILE_DIRECTIVES = {'conference_logo', 'conference_description', 'article'}


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
        if file_type == 'article':
            if file.mimetype not in {'text/plain', 'application/pdf'}:
                return "Invalid mime type for article.", 400
            path_to_upload = upload_directory + os.path.sep + file_type + os.path.sep + directory + os.path.sep
            if not os.path.exists(path_to_upload):
                os.makedirs(os.path.dirname(path_to_upload))
            # logica legata de salvat articole, de extins if needed
            file.save(os.path.join(path_to_upload, filename))
            return file_type + sep + directory + sep + filename, 200
        else:
            path_to_upload = upload_directory + os.path.sep + 'conferences' + os.path.sep + directory + os.path.sep + file_type + os.path.sep
            if file_type == 'conference_description':
                if file.mimetype not in {'text/plain', 'application/pdf'}:
                    return "Invalid mime type for description.", 400
            elif file_type == 'conference_logo':
                if file.mimetype not in {'image/png', 'image/jpg', 'image/jpeg'}:
                    return "Invalid mime type for logo.", 400
            if not os.path.exists(path_to_upload):
                os.makedirs(os.path.dirname(path_to_upload))
            # logica legata de salvat fisiere in conferinta, de extins if needed
            file.save(os.path.join(path_to_upload, filename))
            return 'conferences' + sep + directory + sep + file_type + sep + filename, 200


def retrieve(file_type, directory, file_name):
    if file_type not in ALLOWED_FILE_DIRECTIVES:
        return "File type is not set correctly, available file types are: " + ', '.join(ALLOWED_FILE_DIRECTIVES), 400
    if file_type == 'article':
        upload_directory = current_app.config[
                               'UPLOAD_DIRECTORY'] + os.path.sep + file_type + os.path.sep + directory + os.path.sep
    else:
        upload_directory = current_app.config[
                               'UPLOAD_DIRECTORY'] + os.path.sep + 'conferences' + os.path.sep + directory + os.path.sep + file_type + os.path.sep
    try:
        return send_from_directory(upload_directory, filename=file_name, as_attachment=True)
    except Exception:
        return jsonify({"msg": "File was not found."}), 404
