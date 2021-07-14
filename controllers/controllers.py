# -*- coding: utf-8 -*-
from odoo import http

# class Tsc(http.Controller):
#     @http.route('/tsc/tsc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tsc/tsc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tsc.listing', {
#             'root': '/tsc/tsc',
#             'objects': http.request.env['tsc.tsc'].search([]),
#         })

#     @http.route('/tsc/tsc/objects/<model("tsc.tsc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tsc.object', {
#             'object': obj
#         })