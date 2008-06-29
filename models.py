from google.appengine.ext import db

class Status(db.Model):
    user = db.UserProperty(required=True)
    beer = db.StringProperty(required=True)
    amount = db.IntegerProperty(required=True)
    status = db.TextProperty(required=True)
    updated_at = db.DateTimeProperty(auto_now=True, required=True)

class TotalAmount(db.Model):
    user = db.UserProperty(required=True)
    amount = db.IntegerProperty(default=0)
    nama_cup = db.IntegerProperty(default=0)
    nama_small = db.IntegerProperty(default=0)
    nama_middle = db.IntegerProperty(default=0)
    nama_big = db.IntegerProperty(default=0)
    kan_350 = db.IntegerProperty(default=0)
    kan_500 = db.IntegerProperty(default=0)
    updated_at = db.DateTimeProperty(auto_now=True, required=True)

    @classmethod
    def get_amount_by_beer(cls, beer):
        if beer == "nama_cup":
            return 150
        elif beer == "nama_small":
            return 250
        elif beer == "nama_middle":
            return 500
        elif beer == "nama_big":
            return 800
        elif beer == "kan_350":
            return 350
        elif beer == "kan_500":
            return 500
        else:
            raise LookupError()

    def update(self, beer, num):
        amount = self.get_amount_by_beer(beer) * num
        beer_amount = getattr(self, beer) + amount
        setattr(self, beer, beer_amount)
        self.amount += amount
        self.put()

def delete_status(status):
    total = TotalAmount.all().filter('user = ', status.user).get()
    beer = status.beer
    amount = status.amount

    total.amount -= amount
    setattr(total, beer, getattr(total, beer) - amount)

    total.put()
    status.delete()


