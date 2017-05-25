from flask_admin.contrib import sqla
from flask_admin import form
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



# Administrative views
# class FileView(sqla.ModelView):
#     # Override form field to use Flask-Admin FileUploadField
#     form_overrides = {
#         'path': form.FileUploadField
#     }

#     # Pass additional parameters to 'path' to FileUploadField constructor
#     form_args = {
#         'path': {
#             'label': 'File',
#             'base_path': file_path,
#             'allow_overwrite': False
#         }
#     }


# class ImageView(sqla.ModelView):
#     def _list_thumbnail(view, context, model, name):
#         if not model.path:
#             return ''

#         return Markup('<img src="%s">' % url_for('static',
#                                                  filename=form.thumbgen_filename(model.path)))

#     column_formatters = {
#         'path': _list_thumbnail
#     }

#     # Alternative way to contribute field is to override it completely.
#     # In this case, Flask-Admin won't attempt to merge various parameters for the field.
#     form_extra_fields = {
#         'path': form.ImageUploadField('Image',
#                                       base_path=file_path,
#                                       thumbnail_size=(100, 100, True))
#     }


class UserView(sqla.ModelView):
    """
    This class demonstrates the use of 'rules' for controlling the rendering of forms.
    """
    

    create_template = 'rule_create.html'
    edit_template = 'rule_edit.html'







