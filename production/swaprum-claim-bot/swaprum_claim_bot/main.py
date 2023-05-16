import argparse
import csv
import logging
import traceback
from pathlib import Path
from typing import List

import requests

from .version import __version__

def parse_csv(csv_p: Path) -> List[str]:
    """
    Parse csv and get list of wallet addresses.

    Addresses expected to be in the second column.
    """
    with csv_p.open('r') as f:
        reader = csv.reader(f, delimiter=';', lineterminator=';;;')
        wallets = [row[1] for row in reader]
        return wallets


def log_exception(e: Exception):
    traceback.print_exception(e)
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--csv-wallets', type=Path, required=True,
                        help='.csv file where stored wallet addresses '
                             'in the second column')
    return parser.parse_args()


def main():
    args = parse_args()
    wallets = parse_csv(args.csv_wallets)
    while True:
        for wallet in wallets:
            url = f'https://swaprum.finance/server/claim-free?address={wallet}'
            print(f'GET request to {url}')
            try:
                res = requests.get(f'https://swaprum.finance/server/claim-free?address={wallet}')
                print(f'Response: {res.text}')
            except Exception as e:
                log_exception(e)


if __name__ == '__main__':
    main()
