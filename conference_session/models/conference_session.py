from odoo import api, fields, models
from odoo.tools import populate


class ConferenceSession(models.Model):
    _name = 'conference.session'
    _description = 'Conference Session'
    _order = 'date, name'

    name = fields.Char(string='Title', required=True)
    speaker = fields.Char(string='Speaker')           # ← will be renamed 'presenter' in v19
    duration = fields.Integer(string='Duration (min)')  # ← will become Float (hours) in v19
    room = fields.Char(string='Room')
    notes = fields.Text(string='Notes')
    date = fields.Date(string='Date')

    room_session_count = fields.Integer(
        string='Sessions in room',
        compute='_compute_room_session_count',
    )

    def _compute_room_session_count(self):
        for session in self:
            # deliberately slow: fires one SQL query per record
            session.room_session_count = self.search_count(
                [('room', '=', session.room)]
            )

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
            ('speaker', populate.randomize(
                [f'Speaker {i:02d}' for i in range(1, 21)]
            )),
            ('duration', populate.randomize([30, 45, 60, 75, 90, 105, 120])),
            ('room', populate.randomize(
                ['Hall A', 'Hall B', 'Hall C', 'Hall D', 'Hall E']
            )),
            ('date', populate.randomize(
                ['2026-09-22', '2026-09-23', '2026-09-24', '2026-09-25']
            )),
        ]
