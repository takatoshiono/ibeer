import os
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

class RequestHandler(webapp.RequestHandler):
    def render_response(self, template_file, template_vars):
        user = users.get_current_user()
        if user:
            template_vars['user'] = user
            template_vars['logout_url'] = users.create_logout_url(self.request.uri)
        else:
            template_vars['login_url'] = users.create_login_url(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'templates', template_file)
        self.response.out.write(template.render(path, template_vars))

class App(object):
    def __init__(self, urls):
        self.urls = urls

    def run(self):
        application = webapp.WSGIApplication(self.urls, debug=True)
        wsgiref.handlers.CGIHandler().run(application)

