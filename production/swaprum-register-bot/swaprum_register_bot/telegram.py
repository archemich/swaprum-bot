import shutil
import time
from operator import attrgetter
from pathlib import Path

import psutil
import pywinauto as pwa


class Telegram():
    proc_name: str = 'telegram_bot.exe'

    def __init__(self, base_tg_exe: Path, target_tg_dir:Path):
        self.tg_p = target_tg_dir / self.proc_name
        shutil.copyfile(base_tg_exe, target_tg_dir / self.proc_name)
        # sp.Popen(self.tg_p)
        self.app = pwa.Application(backend='uia')
        self.app = self.app.start(str(self.tg_p))
        self.app.Dialog.wait('ready')
        self.app.Dialog.maximize()
        self.dlg = self.app.Dialog

    def search_user(self, text, is_user_bot: bool = True):
        edit = self.dlg.Edit
        edit.set_focus()
        pwa.keyboard.send_keys(text + '{ENTER}')
        time.sleep(3)
        pwa.keyboard.send_keys('{ENTER}')
        if is_user_bot:
            time.sleep(3)
            pwa.keyboard.send_keys('{ENTER}')

    def send_message(self, text: str):
        text=text.replace(' ', '{SPACE}')
        pwa.keyboard.send_keys(text + '{ENTER}')

    def stop(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == self.proc_name:
                proc.kill()

    def __del__(self):
        self.stop()
        if self.tg_p.exists():
            try:
                self.tg_p.unlink()
            except PermissionError:
                pass
