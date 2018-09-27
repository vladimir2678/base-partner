# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def change_name(self):
        if not self.is_company:
            names = [name for name in [self.first_name, self.middle_name, self.last_name, self.second_last_name] if name]
            self.name = ' '.join(names) 
