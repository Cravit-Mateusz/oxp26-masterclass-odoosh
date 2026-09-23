import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _preserve_speaker_column(cr)
    _convert_duration_minutes_to_hours(cr)


def _preserve_speaker_column(cr):
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conference_session' AND column_name = 'speaker'
    """)
    if not cr.fetchone():
        return

    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conference_session' AND column_name = 'speaker_migrated'
    """)
    if cr.fetchone():
        return

    cr.execute(
        "ALTER TABLE conference_session RENAME COLUMN speaker TO speaker_migrated"
    )
    _logger.info("Renamed conference_session.speaker to speaker_migrated")


def _convert_duration_minutes_to_hours(cr):
    cr.execute("""
        SELECT data_type FROM information_schema.columns
        WHERE table_name = 'conference_session' AND column_name = 'duration'
    """)
    row = cr.fetchone()
    if not row:
        return
    if row[0] not in ('integer', 'smallint', 'bigint'):
        _logger.info("Skipped duration conversion (already %s)", row[0])
        return

    cr.execute("""
        ALTER TABLE conference_session
            ALTER COLUMN duration TYPE double precision
            USING (duration::double precision / 60.0)
    """)
    _logger.info("Converted conference.session duration from minutes to hours")
