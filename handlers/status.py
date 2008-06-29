from google.appengine.api import users
from google.appengine.ext import db

from common import RequestHandler, App
from models import Status, TotalAmount, delete_status

class Update(RequestHandler):
    def post(self):
        user = users.get_current_user()
        beer = self.request.get('beer')
        status_str = self.request.get('status')
        if beer and status_str:
            num = int(self.request.get('num'))
            status = Status(user = user,
                            beer = beer,
                            amount = TotalAmount.get_amount_by_beer(beer) * num,
                            status = status_str,
                            )
            status.put()

            total = TotalAmount.all().filter('user = ', user).get()
            if not total:
                total = TotalAmount(user = user)
            total.update(beer, num)

        self.redirect('/')

class Destroy(RequestHandler):
    def get(self, key):
        try:
            status = Status.get(key)
            user = users.get_current_user()
            if status.user == user:
                delete_status(status)
        except Exception:
            raise
        self.redirect('/')

if __name__ == "__main__":
    app = App([('/status/update', Update),
               ('/status/destroy/(?P<key>.+)', Destroy),
                ])
    app.run()

