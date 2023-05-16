import argparse
import csv
import time
import traceback
from pathlib import Path
from typing import List

import pywinauto as pwa
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from .types import MetaMask
from .telegram import Telegram


def parse_csv(csv_p: Path) -> List[MetaMask]:
    """
    Parse csv and get list of MetaMasks.

    A csv file expected to store recovery_phrase and wallet addresses in pairs.
    """
    with csv_p.open('r') as f:
        reader = csv.reader(f, delimiter=';', lineterminator=';;;')
        metamasks = [MetaMask(recovery_phrase=row[0], address=row[1])
                     for row in reader]
        return metamasks


def log_exception(e: Exception):
    traceback.print_exception(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chrome-webdriver', type=Path, required=True,
                        help='Path to chrome webdriver.')
    parser.add_argument('--csv-wallets', type=Path, required=True,
                        help='.csv file where stored recovery_phrase and wallet addresses '
                             'in pairs.')
    parser.add_argument('--telegram-dir', type=Path, required=True,
                        help='Folder where telegram.exe and tg_<i> folders')
    return parser.parse_args()


def setup_driver() -> webdriver.Chrome:
    options = Options()
    third_parties_path = Path(__file__).parent.parent.parent.parent
    third_parties_path = third_parties_path / 'third_parties'
    options.add_extension(str(third_parties_path / 'metamask.crx'))
    options.add_extension(str(third_parties_path / 'antizapret.crx'))
    driver = webdriver.Chrome(options=options)
    return driver

def main():
    args = parse_args()
    # metamasks = parse_csv(args.csv_wallets)

    # driver = setup_driver()

    tg = Telegram(args.telegram_dir / 'telegram.exe', args.telegram_dir / 'tg2')
    tg.search_user('@swaprum_arb_bot')
    tg.send_message('/active 21349e62fb')
    time.sleep(2)
    twitter = ''
    tg.send_message(twitter)

if __name__ == '__main__':
    main()
