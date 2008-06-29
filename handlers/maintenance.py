from common import RequestHandler, App

class MaintenancePage(RequestHandler):
    def get(self):
        self.response.out.write("Sorry, we are under maintenance.")

if __name__ == "__main__":
    app = App([('/', MaintenancePage),
                ])
    app.run()

