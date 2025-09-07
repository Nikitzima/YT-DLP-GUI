# Файл: yt_dlp_manager.py
# Описание: Этот модуль управляет загрузкой, обновлением и выполнением yt-dlp.exe.
# Он позволяет основному приложению оставаться независимым от версии yt-dlp.
# Изменение: Заменена библиотека 'requests' на встроенный модуль 'urllib' для устранения внешних зависимостей.

import os
import sys
import json
import urllib.request
import shutil
import subprocess
import re

def get_app_dir():
    """Получает базовый каталог приложения, работает как для скрипта, так и для замороженного exe."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_bin_dir():
    """Возвращает путь к каталогу 'bin', где будет храниться yt-dlp.exe."""
    path = os.path.join(get_app_dir(), "bin")
    os.makedirs(path, exist_ok=True)
    return path

class YTDLPManager:
    """
    Класс для управления исполняемым файлом yt-dlp.
    Отвечает за проверку обновлений, загрузку и выполнение команд.
    """
    def __init__(self, logger_callback=None):
        self.bin_dir = get_bin_dir()
        self.executable_path = os.path.join(self.bin_dir, "yt-dlp.exe")
        self.api_url = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
        # Используем переданный логгер или просто print для вывода
        self.log = logger_callback if logger_callback else lambda msg: print(f"[Manager] {msg}")

    def get_latest_version_info(self):
        """Получает данные о последнем релизе с GitHub API с помощью urllib."""
        try:
            # Устанавливаем заголовок User-Agent, так как GitHub API может требовать его
            req = urllib.request.Request(self.api_url, headers={'User-Agent': 'YT-DLP-GUI-Updater'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    self.log(f"Ошибка API запроса: Статус {response.status}")
                    return None
                data = response.read().decode('utf-8')
                return json.loads(data)
        except Exception as e:
            self.log(f"Ошибка API запроса: {e}")
            return None

    def download_executable(self, version_info):
        """Загружает yt-dlp.exe из данных о релизе с помощью urllib."""
        assets = version_info.get("assets", [])
        download_url = next((asset["browser_download_url"] for asset in assets if asset["name"] == "yt-dlp.exe"), None)
        
        if not download_url:
            self.log("Не удалось найти yt-dlp.exe в последнем релизе.")
            return False

        try:
            self.log(f"Загрузка с {download_url}...")
            req = urllib.request.Request(download_url, headers={'User-Agent': 'YT-DLP-GUI-Updater'})
            with urllib.request.urlopen(req, timeout=180) as response: # Увеличено время ожидания для загрузки
                with open(self.executable_path, 'wb') as f_out:
                    shutil.copyfileobj(response, f_out)
            self.log("Загрузка завершена.")
            return True
        except Exception as e:
            self.log(f"Ошибка загрузки: {e}")
            return False

    def check_and_update(self, force=False):
        """
        Проверяет наличие yt-dlp.exe и обновляет его при необходимости или принудительно.
        Возвращает строковый ключ статуса для GUI.
        """
        if not force and os.path.exists(self.executable_path):
            self.log("yt-dlp.exe уже существует. Используйте force=True для обновления.")
            return "already_exists"
        
        self.log("Проверка новой версии yt-dlp...")
        version_info = self.get_latest_version_info()
        if not version_info:
            return "api_error"

        self.log(f"Найдена последняя версия: {version_info['tag_name']}")
        
        # Возвращаем специальный статус для GUI, чтобы он показал "Загрузка..."
        yield "downloading" 
        
        success = self.download_executable(version_info)
        yield "success" if success else "download_error"

    def _create_process(self, args):
        """Создает подпроцесс для выполнения команды yt-dlp."""
        command = [self.executable_path] + args
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=creationflags
        )

    def get_extractors(self):
        """Получает список поддерживаемых экстракторов (сайтов)."""
        if not os.path.exists(self.executable_path):
            self.log("yt-dlp.exe не найден. Пожалуйста, сначала обновите.")
            return []
        
        process = self._create_process(["--list-extractors"])
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            self.log(f"Ошибка получения экстракторов: {stderr}")
            return []
        
        return sorted([line for line in stdout.splitlines() if not line.endswith(':generic')])

    def get_info(self, url):
        """Получает информацию о видео в формате JSON."""
        if not os.path.exists(self.executable_path):
            raise FileNotFoundError("yt-dlp.exe not found")
            
        process = self._create_process(["--dump-json", "--no-playlist", url])
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            error_line = stderr.strip().splitlines()[-1] if stderr.strip() else "Unknown error"
            raise RuntimeError(error_line)
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            self.log(f"Не удалось разобрать JSON: {stdout}")
            raise RuntimeError("Не удалось получить информацию о видео.")