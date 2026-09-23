from odoo.tests.common import TransactionCase


class TestConferenceSession(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Session = cls.env['conference.session']

    def test_duration_in_hours_half(self):
        """30 minutes → 0.5 hours."""
        session = self.Session.create({'name': 'Short Talk', 'duration': 30})
        self.assertAlmostEqual(session.duration_in_hours, 0.5)

    def test_duration_in_hours_one(self):
        """60 minutes → exactly 1.0 hour."""
        session = self.Session.create({'name': 'Standard Session', 'duration': 60})
        self.assertAlmostEqual(session.duration_in_hours, 1.0)

    def test_duration_in_hours_fractional(self):
        """90 minutes → 1.5 hours."""
        session = self.Session.create({'name': 'Long Session', 'duration': 90})
        self.assertAlmostEqual(session.duration_in_hours, 1.5)

    def test_duration_in_hours_zero(self):
        """No duration set → 0.0 hours."""
        session = self.Session.create({'name': 'TBD', 'duration': 0})
        self.assertAlmostEqual(session.duration_in_hours, 0.0)

    def test_duration_updates_when_changed(self):
        """Changing duration recomputes duration_in_hours."""
        session = self.Session.create({'name': 'Workshop', 'duration': 60})
        session.duration = 120
        self.assertAlmostEqual(session.duration_in_hours, 2.0)