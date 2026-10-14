import configparser
import logging
import os

# Map BIBLIONX_* environment variables to standard names if set
_ALIASES = {
    "AMQP_HOST": "BIBLIONX_AMQP_HOST",
    "AMQP_PORT": "BIBLIONX_AMQP_PORT",
    "AMQP_USER": "BIBLIONX_AMQP_USER",
    "AMQP_PASS": "BIBLIONX_AMQP_PASS",
    "AMQP_PREFETCH_COUNT": "BIBLIONX_AMQP_PREFETCH_COUNT",
    "RECEIVE_QUEUE": "BIBLIONX_RECEIVE_QUEUE",
}
for std_var, bib_var in _ALIASES.items():
    if std_var not in os.environ and bib_var in os.environ:
        os.environ[std_var] = os.environ[bib_var]

_CONFIG_FILE = os.environ.get("CORE_CONFIG_FILE", "")
_CONFIG = configparser.ConfigParser(os.environ)


def load_configs(section):
    logger = logging.getLogger(__name__)
    logger.debug("Loading {} configs.".format(section))

    try:
        logger.debug("Opening {}.".format(_CONFIG_FILE))
        with open(_CONFIG_FILE) as c_file:
            _CONFIG.read_file(c_file)

    except FileNotFoundError:
        logger.exception("Failed to open {}.".format(_CONFIG_FILE))
        return {}

    if section in _CONFIG:
        logger.debug("Section '{}' loaded successfully.".format(section))
        return _CONFIG[section]

    else:
        logger.error("Failed to load section '{}'.".format(section))
        return {}
