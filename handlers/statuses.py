from google.appengine.api import users
from google.appengine.ext import db

from common import RequestHandler, App
from models import Status

class StatusPage(RequestHandler):
    def get(self, key):
        try:
            status = Status.get(key)
            user = users.get_current_user()
            if status.user == user:
                self.render_response('status.html', { 'status': status })
            else:
                self.redirect('/')
        except Exception:
            raise

if __name__ == "__main__":
    app = App([('/statuses/(?P<key>.+)', StatusPage),
                ])
    app.run()

