# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char("First Name")
    middle_name = fields.Char("Second Name")
    last_name = fields.Char("Last Name")
    second_last_name = fields.Char("Second Last Name")
    
    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def _onchange_person_names(self):
        if not self.is_company:
            names = [name for name in [self.first_name, self.middle_name, self.last_name, self.second_last_name] if name]
            self.name = ' '.join(names)

    @api.one
    @api.depends('name', 'first_name', 'middle_name', 'last_name', 'second_last_name')
    def copy(self, default=None):
        default = default or {}
        if not self.is_company:
            default.update({
                'first_name': self.first_name and self.first_name + '(copy)' or '',
                'middle_name': self.middle_name and self.middle_name + '(copy)' or '',
                'last_name': self.last_name and self.last_name + '(copy)' or '',
                'second_last_name': self.second_last_name and self.second_last_name + '(copy)' or '',
            })
        return super(ResPartner, self).copy(default=default)
        
    
    @api.multi
    def person_name(self,values):
        values = values or {}
        person_field = ['first_name', 'middle_name', 'last_name', 'second_last_name']
        person_names = set(person_field)
        values_keys = set(values.keys())
        if person_names.intersection(values_keys):
            for person in person_field:
                if values.get(person, False):
                    values.update({
                        person: values.get(person).strip(),
                    })
            names = [name for name in [values.get('first_name', False) or self.first_name,
                                       values.get('middle_name', False) or self.middle_name, 
                                       values.get('last_name', False) or self.last_name, 
                                       values.get('second_last_name', False) or self.second_last_name] if name]
            name = ' '.join(names)
            if name and (name != self.name):
                values.update({
                    'name': name,
                })
        if values.get('name', False):
            values.update({
                'name': values.get('name').strip(),
            })
        return values
        
    @api.multi
    def write(self,values):
        values = self.person_name(values)
        return super(ResPartner, self).write(values)

    @api.model
    def create(self,values):
        values = self.person_name(values)
        return super(ResPartner, self).create(values)
        