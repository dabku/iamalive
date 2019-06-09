
global web_app

def create_web(app):
    global web_app
    app.template_folder = 'web/templates'
    app.static_folder = 'web/static'
    web_app = app
    from iamalive.web import views
