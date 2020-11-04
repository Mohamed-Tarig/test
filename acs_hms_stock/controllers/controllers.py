# -*- coding: utf-8 -*-
from odoo import http

# class AcsHmsStock(http.Controller):
#     @http.route('/acs_hms_stock/acs_hms_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/acs_hms_stock/acs_hms_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('acs_hms_stock.listing', {
#             'root': '/acs_hms_stock/acs_hms_stock',
#             'objects': http.request.env['acs_hms_stock.acs_hms_stock'].search([]),
#         })

#     @http.route('/acs_hms_stock/acs_hms_stock/objects/<model("acs_hms_stock.acs_hms_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('acs_hms_stock.object', {
#             'object': obj
#         })