from datetime import datetime
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types

class StatusLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'Status',
                                 [('user', datastore_types.users.User),
                                  ('beer', str),
                                  ('amount', int),
                                  ('status', datastore_types.Text),
                                  ('updated_at', lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
                                 ])

if __name__ == '__main__':
    bulkload.main(StatusLoader())

