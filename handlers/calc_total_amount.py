from google.appengine.api import users

from common import RequestHandler, App
from models import Status, TotalAmount

class CalcTotalAmount(RequestHandler):
    def get(self):
        statuses = Status.all()

        amounts = {}
        users = {}
        for status in statuses:
            nickname = status.user.nickname()
            amount = amounts.get(nickname, {
                'nama_cup': 0,
                'nama_small': 0,
                'nama_middle': 0,
                'nama_big': 0,
                'kan_350': 0,
                'kan_500': 0,
            })
            amount[status.beer] += status.amount
            amounts[nickname] = amount

            if not users.has_key(nickname):
                users[nickname] = status.user

        for nickname, amount in amounts.items():
            total = TotalAmount.all().filter('user = ', users[nickname]).get()
            if total:
                for beer, value in amount.items():
                    setattr(total, beer, value)
                    self.response.out.write("%s: %s(%s)<br>\n" % (nickname, beer, value))
                total.put()
        self.response.out.write("done.")

if __name__ == "__main__":
    app = App([('/calc_total_amount', CalcTotalAmount),
                ])
    app.run()

