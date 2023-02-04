import argparse
from typing import List, Tuple
import logging

from givenergy_client import GivEnergyClient

print('\n*************************modeset**************')
#------------------------------------------------------------------------------
def configure_logging(verbose: bool):
    """Define logging settings."""
    logging_level = logging.DEBUG if verbose else logging.INFO # todo maybe change
    logging.basicConfig(level=logging_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.root.setLevel(logging_level)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Set mode")
    parser.add_argument(
        "--mode",
        '-m',
        type=int,
        required=True,
        help="Mode to set",
    )
    parser.add_argument(
        "--verbose",
        '-v',
        action='store_true',
        help='Enable verbose logging',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(args.verbose)
    gc = GivEnergyClient()
    if args.mode not in [1,2,3,4]:
        raise RuntimeError("Mode must be 1,2,3,4")
    logging.info(f"before setting, mode is {gc.get_mode()}")
    logging.info(f"setting mode to {args.mode}")
    gc.set_mode(args.mode)
    logging.info(f"mode is now {gc.get_mode()}")


if __name__ == '__main__':
    main()

