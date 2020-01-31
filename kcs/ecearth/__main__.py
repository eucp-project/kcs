"""Module to extract data from EC-EARTH NetCDF data files.

This module wraps the area extraction funcionality from
`kcs.utils.coord`. It can run multiple processes in
parallel. Extracted datasets can be saved (by default) to disk, in
subdirectoriees named after the variable and area (given by a template
that follows Python formatted strings with variable names; the default
is given in the `TEMPLATE` constant).

The module can also be used as a executable module, with the `-m
kcs.ecearth` option to the `python` executable.

"""

import sys
import glob
import argparse
import itertools
import logging
import kcs.config
import kcs.extraction


# Allowed template substitution variable names: var, area, filename
# (filename refers to the filename part of the input file, not the full path)
TEMPLATE = "ecearth/{var}-{area}-averaged/{filename}"

logger = logging.getLogger(__name__)


def parse_args():
    """Parse the command line arguments"""

    areas = list(kcs.config.AREAS.keys())

    class ListAreas(argparse.Action):
        """Helper class for argparse to list available areas and exit"""
        def __call__(self, parser, namespace, values, option_string):
            print("\n".join(areas))
            parser.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help="Input files. "
                        "Globbing patterns (including recursive globbing with '**') allowed.")
    parser.add_argument('--area', action='append', required=True,
                        choices=areas, help="One or more area names")
    parser.add_argument('--template', default=TEMPLATE,
                        help="Output path template, including subdirectory")
    parser.add_argument('-v', '--verbosity', action='count',
                        default=0, help="Verbosity level")
    parser.add_argument('-P', '--nproc', type=int, default=1,
                        help="Number of simultaneous processes")
    parser.add_argument('--list-areas', action=ListAreas, nargs=0,
                        help="List availabe areas and quit")
    parser.add_argument('--regrid', action='store_true',
                        help="Regrid the data (to a 1x1 deg. grid)")
    parser.add_argument('--no-save-results', action='store_true',
                        help="Store the resulting extracted datasets on disk")
    parser.add_argument('--no-average-area', action='store_true',
                        help="Don't average the extracted areas")
    parser.add_argument('--tempdir')
    args = parser.parse_args()
    # Expand any glob patterns in args.files
    args.files = list(itertools.chain.from_iterable(glob.glob(pattern) for pattern in args.files))
    args.save_result = not args.no_save_results
    args.average_area = not args.no_average_area
    args.area = {name: kcs.config.AREAS[name] for name in args.area}
    return args


def setup_logging(verbosity=0):
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[max(0, min(verbosity, len(levels)))]
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt="%Y-%m-%dT%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    kcs_logger = logging.getLogger('kcs')
    kcs_logger.setLevel(level)
    kcs_logger.addHandler(handler)


def main():
    args = parse_args()
    setup_logging(args.verbosity)
    logger.debug("%s", " ".join(sys.argv))
    logger.debug("Args: %s", args)
    kcs.extraction.run(args.files, args.area, regrid=args.regrid,
                       save_result=args.save_result, average_area=args.average_area,
                       nproc=args.nproc, template=args.template,
                       tempdir=args.tempdir)
    logger.debug("%s finished", sys.argv[0])


if __name__ == "__main__":
    main()
