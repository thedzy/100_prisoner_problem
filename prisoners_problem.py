#!/usr/bin/env python3

__author__ = 'thedzy'
__copyright__ = 'Copyright 2024, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Development'
__date__ = '2025-02-10'
__description__ = \
    """
    prisoners_problem.py: 
    The 100 prisoners problem
    
    The director of a prison offers 100 death row prisoners, who are numbered from 1 to 100, a last chance. 
    A room contains a cupboard with 100 drawers. The director randomly puts one prisoner's number in each 
    closed drawer. The prisoners enter the room, one after another. Each prisoner may open and look into 50 
    drawers in any order. The drawers are closed again afterwards. If, during this search, every prisoner 
    finds their number in one of the drawers, all prisoners are pardoned. If even one prisoner does not 
    find their number, all prisoners die. Before the first prisoner enters the room, the prisoners may 
    discuss strategy — but may not communicate once the first prisoner enters to look in the drawers. What 
    is the prisoners' best strategy?

    https://en.wikipedia.org/wiki/100_prisoners_problem
    """

import argparse
import logging.config
import pprint
import random
from pathlib import Path


class ColourFormat(logging.Formatter):
    """
    Add colour to logging events
    """

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = '%', levels={}) -> None:
        """
        Initialise the formatter
        ft: (str) Format String
        datefmt: (str) Date format
        style: (str) Format style
        levels: tuple, tuple (level number start, colour, attribute
        """
        self.levels = {}
        set_levels = {10: 90, 20: 92, 30: 93, 40: 91, 50: (41, 97)}
        set_levels.update(levels)

        for key in sorted(set_levels.keys()):
            value = set_levels[key]
            colour = str(value) if isinstance(value, (str, int)) else ';'.join(map(str, value))

            self.levels[key] = f'\x1b[5;{colour};m'

        super().__init__(fmt, datefmt, style)

    def formatMessage(self, record: logging.LogRecord, **kwargs: dict) -> str:
        """
        Override the formatMessage method to add colour
        """
        no_colour = u'\x1b[0m'
        for level in self.levels:
            colour = self.levels[level] if record.levelno >= level else colour

        return f'{colour}{super().formatMessage(record, **kwargs)}{no_colour}'


def main() -> None:
    logger.info('Start')

    total_prisoners = options.total_prisoners
    total_runs = options.total_runs
    successes = 0

    logger.info(f'{"Runs":20}: {total_runs:5d}')
    logger.info(f'{"Prisoners":20}: {total_prisoners:5d}')

    for run_number in range(0, total_runs):
        logger.debug3(f'------------- Run: {run_number} -------------')
        counts = []
        first_50 = 0  # How many find it in the first 50% of boxes

        # Setup the room first
        boxes = {box: 0 for box in range(0, total_prisoners)}
        prisoner_boxes = list(range(0, total_prisoners))

        # Assign numbers to the boxes randomly
        for box in boxes:
            prisoner = random.choice(prisoner_boxes)
            prisoner_boxes.remove(prisoner)
            boxes[box] = prisoner

        # Send the prisoners in to pick their boxes in the set order
        prisoners = list(range(0, total_prisoners))
        random.shuffle(prisoners)
        for prisoner in prisoners:
            logger.debug2(f'Prisoner: {prisoner}')

            count = 1
            box = prisoner
            while True:
                new_box = boxes[box]
                if new_box == prisoner:
                    logger.debug(f'{prisoner:5d}: Try #{count} Box #{box}={new_box}')
                    break
                else:
                    logger.debug(f'{prisoner:5d}: Try #{count} Box #{box}={new_box}')
                    count += 1
                    box = new_box

            counts.append(count)
            logger.debug(f'Tries: {count}')
            if count <= total_prisoners / 2:
                first_50 += 1

        logger.debug3(f'{"Average":20}: {sum(counts) / total_prisoners:5.0f}')
        logger.debug3(f'{"First half":20}: {first_50:5d}')

        if first_50 == total_prisoners:
            successes += 1

    logger.info(f'{"Successes":20}: {successes:5d}')
    logger.info(f'{"Percentage":20}: {(successes / total_runs) * 100:7.1f}%')

    logger.info('Done')


def create_logger(name: str = __file__, levels: dict = {}) -> logging.Logger:
    """
    Create logging with custom levels
    :param name: (str) Logger name
    :param levels: (dict) levelname=level
    :return: (logging.Logger) Logging instance
    """

    # Create log level
    def make_log_level(level_name: str, level_int: int) -> None:
        logging.addLevelName(level_int, level_name.upper())
        setattr(new_logger, level_name, lambda *args: new_logger.log(level_int, *args))

    new_logger = logging.getLogger(name)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stderr': {
                '()': ColourFormat,
                'style': '{', 'format': '{message}',
            },
            'file': {
                'style': '{', 'format': '[{asctime}] [{levelname:8}] {message}'
            }
        },
        'handlers': {
            'stderr': {
                'class': 'logging.StreamHandler',
                'formatter': 'stderr',
                'stream': 'ext://sys.stderr',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'file',
                'filename': options.log_file if options.log_file else '/dev/null',
                'maxBytes': 1024 * 5
                ,
                'backupCount': 0
            }
        },
        'loggers': {
            'root': {
                'handlers': [
                    'stderr'
                ]
            },
            name: {
                'level': options.log_level,
                'handlers': [
                    'stderr'
                ]
            }
        }
    }

    if options.log_file is not None:
        logging_config['loggers'][name]['handlers'].append('file')

    logging.config.dictConfig(logging_config)

    # Create custom levels
    for level in levels.items():
        make_log_level(*level)

    return new_logger


if __name__ == '__main__':
    def valid_path(path):
        parent = Path(path).parent
        if not parent.is_dir():
            print(f'{parent} is not a directory, make it?', end=' ')
            if input('y/n: ').lower()[0] == 'y':
                parent.mkdir(parents=True, exist_ok=True)
                return Path(path)
            raise argparse.ArgumentTypeError(f'{path} is an invalid path')
        return Path(path)


    # Create argument parser
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-r', '--runs', type=int, default=1000,
                        action='store', dest='total_runs',
                        help='how many times to run the scenario')

    parser.add_argument('-p', '--prisoners', type=int, default=100,
                        action='store', dest='total_prisoners',
                        help='how many prisoners in the scenario')

    # Debug/verbosity option
    parser.add_argument('--debug', type=int, default=20, const=12, nargs='?',
                        action='store', dest='log_level',
                        help=argparse.SUPPRESS)

    # Output
    parser.add_argument('--log', type=valid_path,
                        default=None,
                        action='store', dest='log_file',
                        help='output log')

    options = parser.parse_args()

    logger = create_logger(levels={'debug2': 11, 'debug3': 12})
    logger.debug('Debug ON')
    logger.debug(pprint.pformat(options))

    main()
