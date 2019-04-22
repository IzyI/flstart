from flask import Flask, g, render_template, request, url_for, send_from_directory,jsonify, send_file
from main import config
from main.extensions import lm,  mail, migrate,limiter, ck_editor,thum
from main.fadmin import admin
from main.database import db
from flask_login import login_required

# Arrow - это модуль Python для работы с датой и временем
import arrow
import time
from main.utils import url_for_other_page
import requests
from main.front import front
from main.user import user
from main.api import api_bp
from main.pages import page
from main.articles import article
# from main.commands import create_db, drop_db, populate_db, recreate_db


import os
from flask_ckeditor import upload_fail, upload_success


def create_app(config=config.base_config, basedir_not_main=config.basedir_not_main):
    """Returns an initialized Flask application."""
    node = Flask(__name__, template_folder="templates")
    node.config.from_object(config)
    register_extensions(node)
    register_blueprints(node)
    register_errorhandlers(node)
    register_jinja_env(node)
    register_commands(node)

    @node.before_request
    def before_request():
        """Prepare some things before the application handles a request."""
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
        g.pjax = 'X-PJAX' in request.headers


    @node.route('/upload', methods=['POST'])
    @login_required
    def upload():
        f = request.files.get('upload')
        extension = f.filename.split('.')[1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        f.save(os.path.join(node.config['UPLOADED_PATH'], f.filename))
        url = url_for('uploads', filename=f.filename)

        return upload_success(url=url)

    @node.route('/uploads/<path:filename>', methods=['GET'])
    def uploads(filename):
        return send_file(basedir_not_main + '/uploads/' + filename)

    @node.route('/check-file', methods=['GET'])
    def check_file_handler():
        dirr =  request.args.get('dir')
        if dirr:
            dir_path=dirr+"/"
            bp=dirr.split("/")
            if len(bp)==1:
                back_page="NONE"
            else:
                back_page="/".join(bp[:-1])
        else:
            dir_path=""
            back_page=""
        f = os.listdir(basedir_not_main + '/uploads/'+dir_path)
        files=[]
        folder=[]
        for i in f:
            r=i.split(".")
            if r[-1] in ['jpg', 'gif', 'png', 'jpeg']:
                files.append(dir_path+i)
            else:
                folder.append({"path":dir_path+i,"name":i})
        return render_template('file-browse.html' ,files=files,folder=folder,back_page=back_page)

    # @node.route('/_image-url')
    # def _get_image_url():
    #
    #     img_id = request.args.get('img_id')
    #     img = Cases.query.get(img_id)
    #     if img is None:
    #         response = jsonify(status='not found')
    #         return response
    #     return jsonify(img_path=img.path, status='ok')
    #


    return node



def register_extensions(node):
    """Register extensions with the Flask application."""
    db.init_app(node)
    lm.init_app(node)
    admin.init_app(node)
    mail.init_app(node)
    migrate.init_app(node, db)
    register_errorhandlers(node)
    limiter.init_app(node)
    ck_editor.init_app(node)
    thum.init_app(node)


def register_blueprints(node):
    """Register blueprints with the Flask application."""
    node.register_blueprint(front, url_prefix='/')
    node.register_blueprint(user, url_prefix='/')
    node.register_blueprint(page, url_prefix='/page')
    node.register_blueprint(article, url_prefix='/articles')
    node.register_blueprint(api_bp, url_prefix='/api')




def register_errorhandlers(app):
    """Register error handlers with the Flask application."""

    def render_error(e):
        return render_template('errors/%s.html' % e.code), e.code

    for e in [
        requests.codes.INTERNAL_SERVER_ERROR,
        requests.codes.NOT_FOUND,
        requests.codes.UNAUTHORIZED,
    ]:
        app.errorhandler(e)(render_error)

def register_jinja_env(app):
    """Configure the Jinja env to enable some functions in templates."""
    app.jinja_env.globals.update({
        'timeago': lambda x: arrow.get(x).humanize(),
        'url_for_other_page': url_for_other_page,
})


def register_commands(app):
    """Register custom commands for the Flask CLI."""
    # for command in [create_db, drop_db, populate_db, recreate_db]:
    #     app.cli.command()(command)