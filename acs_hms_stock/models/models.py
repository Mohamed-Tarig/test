# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError,ValidationError
from datetime import datetime

class MoveItemRequest(models.Model):
    _name = 'move.item.request'
    _description = 'Move Request'

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    request_date = fields.Datetime(string='Date', default=datetime.today())
    user_id = fields.Many2one('res.users', string='Responsible', required=False, default=lambda self: self.env.user)  
    # picking_type_id=fields.Many2one('stock.picking.type', 'Picking Type')
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        required=True,
       )
    # location_id = fields.Many2one(
    #     'stock.location', "Source Location",
    #     default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id,
    #      required=True,
    #     )
    # location_dest_id = fields.Many2one(
    #     'stock.location', "Destination Location",
    #     default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
    #      required=True,
    #     )




    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id.id,
        index=True, required=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})


    # destnation = fields.Many2one('stock.location', 'Destnation Loaction')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),], string='Status', readonly=True, copy=False, index=True, default='draft')
    item_lines = fields.One2many('move.item.request.lines', 'request_id', string='Reqest Lines')


    # @api.model
    # def create(self, vals):
    #     res = super(MoveItemRequest, self).create(vals)
    #     print("?>>>>>>>>>>>>>>>>>>>>>>0",vals)
    #     if not 'item_lines' in vals :
    #         raise UserError(_('Nothing to check the availability for.'))
        
    #     return res


    @api.multi
    def action_confirm (self):
        self.write({'state':'confirm'})
    def on_test(self):
        logging.info("hhhhhhhhhhhhhhhhhhhh")
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('move.item.request') or _('New')
        # if not 'item_lines' in vals :على مستوى اﻹنشاء الجديد
        #     raise UserError(_('Nothing to check the availability for.'))
        result = super(MoveItemRequest, self).create(vals)
        return result

    # @api.model
    # @api.constrains('item_lines') #على مستوى المودل
    # def _check_item_lines(self):
    #     if not self.item_lines:
    #         raise ValidationError(_('please ! insert your item lines'))
    #     if self.item_lines.product_qty <=0:
    #         raise ValidationError(_('product Quantity %s must be grater than zero ')%(self.item_lines.product_qty))
    def create_stock_move(self):
        # source_id = self.source
        # print(">>>>>>>>>>>>>>>>>>>>>>",source_id)
        # dest = self.env.user.company_id.default_lab_location
        stock_move = self.env['stock.picking'].create({
            'origin': self.name,
            'partner_id':self.user_id.partner_id.id,
            'location_id' : self.picking_type_id.default_location_src_id.id,
            'picking_type_id':self.picking_type_id.id,
            'location_dest_id':self.picking_type_id.default_location_dest_id.id,
            'scheduled_date':self.request_date,
            # 'product_uom': product_uom_id.id,
            # 'location_id': source_id.id,
            # 'location_dest_id': ,
        })
        for move in self.item_lines:
            stock_move_line=self.env['stock.move'].create({
                'name':move.request_id.name,
                'picking_id':stock_move.id,
                'product_id': move.product_id.id,
                'product_uom_qty': move.product_qty,
                'location_id':7,
                'location_dest_id':7,
                'product_uom':move.product_id.uom_id.id
            
            })


       

        self.write({'state':'done'})



class MoveItemRequestLines(models.Model):
    _name = 'move.item.request.lines'

    product_qty = fields.Float('Quantity')
    product_id = fields.Many2one('product.product', 'Product')
    request_id = fields.Many2one('move.item.request', 'Reqest Lines')

class SockPicking(models.Model):
    _inherit="stock.picking"


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    user_id = fields.Many2one('res.users', string='Responsible', required=False, default=lambda self: self.env.user)  

class Users(models.Model):
    _inherit = 'res.users'

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
