import shutil
import time
from pathlib import Path
from enum import Enum, auto

import psutil
import pywinauto as pwa


class Telegram():
    class TelegramUser(Enum):
        User = auto()
        Bot = auto()
        Group = auto()

    proc_name: str = 'telegram_bot.exe'

    def __init__(self, base_tg_exe: Path, target_tg_dir:Path):
        self.tg_p = target_tg_dir / self.proc_name
        shutil.copyfile(base_tg_exe, target_tg_dir / self.proc_name)
        self.app = pwa.Application(backend='uia')
        self.app = self.app.start(str(self.tg_p))
        self.app.Dialog.wait('ready')
        self.app.Dialog.maximize()
        self.dlg = self.app.Dialog

    def search_user(self, text, user_type: TelegramUser):
        edit = self.dlg.Edit
        edit.set_focus()
        pwa.keyboard.send_keys(text + '{ENTER}')
        time.sleep(3)
        pwa.keyboard.send_keys('{ENTER}')
        time.sleep(1)
        pwa.keyboard.send_keys('{ENTER}{ENTER}{ENTER}')
        time.sleep(1)
        pwa.keyboard.send_keys('{TAB}')

        if user_type == Telegram.TelegramUser.Bot:
            time.sleep(3)
            pwa.keyboard.send_keys('{ENTER}')
        elif user_type == Telegram.TelegramUser.Group:
            # join group
            rect = self.dlg.rectangle()
            center_rect = ((rect.right - rect.left) // 2 + rect.left, rect.bottom - 2)
            pwa.mouse.click(coords=center_rect)


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
