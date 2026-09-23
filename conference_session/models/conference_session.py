from odoo import api, fields, models
from odoo.tools import populate


class ConferenceSession(models.Model):
    _name = 'conference.session'
    _description = 'Conference Session'
    _order = 'date, name'

    name = fields.Char(string='Title', required=True)
    duration = fields.Float(string='Duration (hours)')
    presenter = fields.Many2one('res.partner', string='Presenter')
    room = fields.Char(string='Room')
    notes = fields.Text(string='Notes')
    date = fields.Date(string='Date')

    room_session_count = fields.Integer(
        string='Sessions in room',
        compute='_compute_room_session_count',
    )

    @api.depends('room')
    def _compute_room_session_count(self):
        counts = dict(self._read_group(
            [('room', 'in', self.mapped('room'))],
            groupby=['room'],
            aggregates=['__count'],
        ))
        for session in self:
            session.room_session_count = counts.get(session.room, 0)

    # ── populate (odoo-bin populate --size=medium --models=conference.session) ──

    _populate_sizes = {
        'small': 500,
        'medium': 10_000,
        'large': 65_000,
    }

    @classmethod
    def _populate_factories(cls):
        return [
            ('name', populate.randomize(
                [f'Session {i:05d}' for i in range(100_000)]
            )),
            ('presenter', populate.randomize(
                cls.env['res.partner'].search([]).ids or [False]
            )),
            ('duration', populate.randomize([0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])),
            ('room', populate.randomize(
                ['Hall A', 'Hall B', 'Hall C', 'Hall D', 'Hall E']
            )),
            ('date', populate.randomize(
                ['2026-09-22', '2026-09-23', '2026-09-24', '2026-09-25']
            )),
        ]
