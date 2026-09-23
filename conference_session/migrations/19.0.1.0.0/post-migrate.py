import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Map former speaker names onto presenter (res.partner) after the ORM created the column."""
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conference_session' AND column_name = 'speaker_migrated'
    """)
    if not cr.fetchone():
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    Partner = env['res.partner']

    cr.execute("""
        SELECT DISTINCT speaker_migrated
        FROM conference_session
        WHERE speaker_migrated IS NOT NULL
          AND TRIM(speaker_migrated) <> ''
    """)
    names = [row[0] for row in cr.fetchall()]

    for name in names:
        partner = Partner.search([('name', '=', name)], limit=1)
        if not partner:
            partner = Partner.create({'name': name})
        cr.execute(
            """
            UPDATE conference_session
               SET presenter = %s
             WHERE speaker_migrated = %s
            """,
            (partner.id, name),
        )

    cr.execute("ALTER TABLE conference_session DROP COLUMN speaker_migrated")
    _logger.info("Mapped %s speaker name(s) to presenter", len(names))
