import argparse
import csv
import sys
import time
import traceback
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from .twitter import Twitter
from .types import MetaMask, TwitterAccount, Email
from .version import __version__


def parse_metamasks(csv_p: Path) -> List[MetaMask]:
    """
    Parse csv and get list of MetaMasks.

    A csv file expected to store recovery_phrase and wallet addresses in pairs.
    """
    with csv_p.open('r') as f:
        reader = csv.reader(f, delimiter=',', lineterminator='\n')
        metamasks = [MetaMask(recovery_phrase=row[0])
                     for row in reader]
        return metamasks


def parse_twitters(csv_p: Path) -> List[TwitterAccount]:
    """
    Parse csv and get list of MetaMasks.

    A csv file expected to store recovery_phrase and wallet addresses in pairs.
    """
    with csv_p.open('r') as f:
        reader = csv.reader(f, delimiter=':', lineterminator='\n')
        twitters = [TwitterAccount(login=row[0], password=row[1],
                                   email=Email(login=row[2], password=row[3]))
                     for row in reader]
        return twitters


def log_exception(e: Exception):
    traceback.print_exception(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--chrome-webdriver', type=Path, required=True,
                        help='Path to chrome webdriver.')
    parser.add_argument('--csv-wallets', type=Path, required=True,
                        help='.csv file where stored recovery_phrase and wallet addresses '
                             'in pairs.')
    parser.add_argument('--csv-twitters', type=Path, required=True,
                        help='.csv file in format <login>:<password>:<email>:<email_password>. Newline="\\n"')
    parser.add_argument('--telegram-dir', type=Path, required=True,
                        help='Folder where telegram.exe and tg_<i> folders')
    return parser.parse_args()


def setup_driver() -> webdriver.Chrome:
    options = Options()
    third_parties_path = Path(__file__).parent.parent.parent.parent
    third_parties_path = third_parties_path / 'third_parties'
    options.add_extension(str(third_parties_path / 'metamask.crx'))
    options.add_extension(str(third_parties_path / 'antizapret.crx'))
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    time.sleep(3)
    return driver


def main():
    args = parse_args()
    # Заходим на сайт. Коннектимся к сайту
    # Берем /active с сайта для телеграма
    # Отправляем в телеграм /active
    # Отправляем в телеграм твиттер
    # Телеграм закрываем.

    metamasks = parse_metamasks(args.csv_wallets)
    twitters = parse_twitters(args.csv_twitters)
    if len(metamasks) != len(twitters):
        print('Number of metamasks and number of twitters must be the same')
        sys.exit()

    driver = setup_driver()

    for metamask, twitter in zip(metamasks, twitters):
        twitter = Twitter(twitter, driver)
        twitter.run()
        print('username: ' + twitter.username)
        break

    # tg = Telegram(args.telegram_dir / 'Telegram.exe', args.telegram_dir / 'tg3')
    # tg.search_user('https://t.me/nameslot', Telegram.TelegramUser.Group)
    # tg.send_message('/active 21349e62fb')

if __name__ == '__main__':
    main()
