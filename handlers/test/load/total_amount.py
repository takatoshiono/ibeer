from datetime import datetime
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types

class TotalAmountLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'TotalAmount',
                                 [('user', datastore_types.users.User),
                                  ('amount', int),
                                  ('nama_cup', int),
                                  ('nama_small', int),
                                  ('nama_middle', int),
                                  ('nama_big', int),
                                  ('kan_350', int),
                                  ('kan_500', int),
                                  ('updated_at', lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
                                 ])

if __name__ == '__main__':
    bulkload.main(TotalAmountLoader())

