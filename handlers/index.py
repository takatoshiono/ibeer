# -*- coding: utf-8 -*-

from google.appengine.api import users

from common import RequestHandler, App
from models import Status, TotalAmount

limit = 10

class IndexPage(RequestHandler):
    def get(self):
        user = users.get_current_user()
        total = TotalAmount.all().filter('user = ', user).get()

        if user and total:
            page = int(self.request.get('page', 1))

            if page > 0:
                offset = limit * (page - 1)
            else:
                self.redirect('/')
                return

            chart_labels, chart_values = mk_chart_data(total)
            total_status = Status.all().filter('user = ', user).count(1000)
            statuses = Status.all().filter('user = ', user).order('-updated_at').fetch(limit, offset)

            if len(statuses):
                self.render_response('index.html', {
                    'statuses': statuses,
                    'total_amount': total.amount,
                    'chart_labels': chart_labels,
                    'chart_values': chart_values,
                    'is_paginated': limit < total_status,
                    'has_previous': page > 1,
                    'has_next': (offset + limit) < total_status,
                    'previous_page': page - 1,
                    'next_page': page + 1,
                })
            else:
                self.render_response('index.html', {
                    'statuses': [],
                })
        else:
            self.render_response('index.html', {})

def mk_chart_data(total):
    amounts = {
        'nama_cup': total.nama_cup,
        'nama_small': total.nama_small,
        'nama_middle': total.nama_middle,
        'nama_big': total.nama_big,
        'kan_350': total.kan_350,
        'kan_500': total.kan_500,
    }
    items = amounts.items()
    items.sort(lambda x, y: cmp(x[1], y[1]))
    items.reverse()

    labels = []
    values = []
    for item in items:
        if item[1] > 0:
            labels.append(get_label(item[0], item[1]))
            values.append('%.4f' % (1.0 * item[1] / total.amount))

    return labels, values

def get_label(k, v):
    label = ''

    if k == "nama_cup":
        label = "little bit"
    elif k == "nama_small":
        label = "glass"
    elif k == "nama_middle":
        label = "draft(regular)"
    elif k == "nama_big":
        label = "draft(large)"
    elif k == "kan_350":
        label = "canned(350)"
    elif k == "kan_500":
        label = "canned(500)"
    else:
        label = ""

    return '%s(%s ml)' % (label, v)

if __name__ == "__main__":
    app = App([('/', IndexPage),
                ])
    app.run()

