import os
import logging
import logging.handlers
import sys
from datetime import datetime

## References:
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# Define the default logging message formats.
file_msg_format = '%(asctime)s %(levelname)-8s: %(message)s'
console_msg_format = '%(levelname)s: %(message)s'

# Define the log rotation criteria.
max_bytes = 1024 ** 2
backup_count = 10


def setup_logging(directory='logs', filename='debug.log', append_time=False):
    # Create the root logger.
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Validate the given directory.
    directory = os.path.normpath(directory)

    # Create a folder for the logfiles.
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the name of the logfile.
    filename = filename.rstrip('.log')
    if append_time:
        t = datetime.now()
        time_str = '{year:04d}{month:02d}{day:02d}-{hour:02d}{minute:02d}{second:02d}'. \
            format(year=t.year, month=t.month, day=t.day,
                   hour=t.hour, minute=t.minute, second=t.second)
        filename = filename + '-' + time_str + '.log'
    else:
        filename = filename + '.log'
    file_name = os.path.join(directory, filename)

    # Set up logging to the logfile.
    file_handler = logging.handlers.RotatingFileHandler(
        filename=file_name, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(file_msg_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Set up logging to the console.
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter(console_msg_format)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
