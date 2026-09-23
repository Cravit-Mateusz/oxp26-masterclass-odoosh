-- Wipe the custom System Parameter secret copied from production
UPDATE ir_config_parameter
SET value = 'neutralized'
WHERE key = 'secret';
