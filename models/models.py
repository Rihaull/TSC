# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging

_logger = logging.getLogger(__name__)

class Tele(models.Model):
    _name = 'tsc.tele'

    model = fields.Char(string="Modèle du téléviseur")
    prix_HTVA = fields.Float(string="Prix hors TVA")
    resolution_x = fields.Integer()
    resolution_y = fields.Integer()
    resolution = fields.Char(string="Résolution", compute='_resolution_string')

    @api.depends('resolution_x', 'resolution_y')
    def _resolution_string(self):
        for r in self:
            r.resolution = str(r.resolution_x) + ' x ' + str(r.resolution_y)

    def name_get(self):
        tele_list = []
        for tel in self:
            name = "["+tel.resolution+"] "
            if tel.model:
                name += "{}".format(tel.model)
            tele_list.append((tel.id, name))
        return tele_list

class Inventory(models.Model):
    _name = 'tsc.inventory'
    _rec_name = 'tele'

    tele = fields.Many2one('tsc.tele', string="Modèle du téléviseur")
    quantity = fields.Integer(string="Quantité disponible")
    expo = fields.Boolean(string="Modèle d'exposition existant")

    _sql_constraints = [
        ('tele_unique',
         'UNIQUE(tele)',
         "Ce modèle existe déjà dans le stock."),
    ]

class Vendors(models.Model):
    _name = 'tsc.vendors'
    _rec_name = 'fullname'

    lastname = fields.Char(string="Nom de Famille")
    first_name = fields.Char(string="Prénom")
    manager = fields.Boolean(string="Sales Manager")
    fullname = fields.Char(string="Nom complet", compute='_fullname_string')

    @api.depends('lastname', 'first_name')
    def _fullname_string(self):
        for r in self:
            r.fullname = r.lastname + ' ' + r.first_name

class Sales(models.Model):
    _name = 'tsc.sales'


    stock = fields.Many2one('tsc.inventory', string="Modèle du téléviseur")
    vendor = fields.Many2one('tsc.vendors', string="Vendu par")
    quanti = fields.Integer(string="Quantité vendu(s)")
    prix_total = fields.Float(string="Prix total TVA inclus", compute='_prix_total')

    @api.depends('stock','quanti')
    def _prix_total(self):
        for r in self:
            if r.stock.quantity == 1 and r.stock.expo:
                r.prix_total = (r.stock.tele.prix_HTVA * r.quanti) * 1.06
            else:
                r.prix_total = (r.stock.tele.prix_HTVA * r.quanti) * 1.21

    @api.constrains('stock')
    def check_expo(self):
        if self.stock.quantity==1 and self.stock.expo and not self.vendor.manager:
            raise exceptions.ValidationError("Vous ne pouvez pas vendre cet article car la vente de modèle d'exposition est réservé aux managers.")

    @api.constrains('stock')
    def check_if_stock(self):
        if self.stock.quantity == 0:
            raise exceptions.ValidationError("Vous ne pouvez pas vendre cet article car il n'en reste plus en stock.")
