from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import url_for, redirect, request
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, expose
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
from main.user.models import User, db
from main.pages.models import Pages
from main.tags.models import Tag
from main.articles.models import Articles
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin.contrib.fileadmin import FileAdmin
from .config import base_config
from jinja2 import Markup
import os
from flask_admin import form as admin_form
from werkzeug.utils import secure_filename
import random




class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not user.check_password(self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class MyPageView(ModelView):
    form_overrides = dict(content=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'
    def is_accessible(self):
        return login.current_user.is_authenticated


class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAllView(ModelView):
    create_template = 'edit.html'
    edit_template = 'edit.html'
    def is_accessible(self):
        return login.current_user.is_authenticated




class MyArticleView(ModelView):
    column_list =  ('title', 'date', 'anons')
    form_overrides = dict(text=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'
    img_dir=base_config.UPLOADED_PATH+"/article"
    try:
        os.mkdir(img_dir)
    except:
        ...
    def prefix_name(obj, file_data):
        parts = os.path.splitext(file_data.filename)
        rand_string = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm1234567890') for _ in range(random.randint(15,40)))
        return secure_filename(rand_string+'_file-%s%s' % parts)

    form_extra_fields = {
        'image': admin_form.ImageUploadField('Image', base_path=img_dir,
                                             endpoint="uploads",
                                             namegen=prefix_name,
                                             url_relative_path="article/",
                                             thumbnail_size=(100, 80, True))}
    def is_accessible(self):
        return login.current_user.is_authenticated


admin = Admin(name='Админ панель',
              index_view=MyAdminIndexView(),
              base_template='admin/my_admin.html',
              template_mode='bootstrap3')

admin.add_view(MyPageView(Pages, db.session))
admin.add_view(MyArticleView(Articles, db.session))
admin.add_view(MyAllView(Tag, db.session))
admin.add_view(MyFileAdmin(base_config.UPLOADED_PATH, '/uploads/', name='Uploads'))