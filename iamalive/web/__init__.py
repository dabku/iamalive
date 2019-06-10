import os
global web_app


def create_web(app):
    global web_app
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app.template_folder = os.path.join(dir_path, 'templates')
    app.static_folder = os.path.join(dir_path, 'static')
    web_app = app
    from iamalive.web import views
