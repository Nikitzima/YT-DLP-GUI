# Р¤Р°Р№Р»: main_app.py
# РР·РјРµРЅРµРЅРёСЏ:
# - РСЃРїСЂР°РІР»РµРЅР° Р»РѕРіРёРєР° РёРЅРёС†РёР°Р»РёР·Р°С†РёРё СЏР·С‹РєР° РґР»СЏ РєРѕСЂСЂРµРєС‚РЅРѕРіРѕ РѕС‚РѕР±СЂР°Р¶РµРЅРёСЏ РїСЂРё РїРµСЂРІРѕРј Р·Р°РїСѓСЃРєРµ.
# - РЇР·С‹Рє РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ РїСЂРё СЃРѕР·РґР°РЅРёРё РєРѕРЅС„РёРіСѓСЂР°С†РёРё РёР·РјРµРЅРµРЅ РЅР° "English".
# - Р”РѕР±Р°РІР»РµРЅР° С„СѓРЅРєС†РёСЏ Рё РєРЅРѕРїРєР° РґР»СЏ РїСЂРёРЅСѓРґРёС‚РµР»СЊРЅРѕР№ РѕС‡РёСЃС‚РєРё РІСЃРµС… С„Р°Р№Р»РѕРІ Р»РѕРіРѕРІ.

"""
Главное приложение YT-DLP GUI.

Замечания для разработчиков:
- Код организован по секциям: утилиты, логи/FFmpeg, UI‑виджеты, основное приложение;
- UI строится заново при смене темы/языка через `_rebuild_ui`, чтобы избежать глитчей;
- Секция `CollapsibleFrame` содержит логику смещения центрального блока при показе списка сайтов
  (метод `_check_and_adjust_layout`).

Файлы ресурсов (icon.ico, logo_bg.png) подтягиваются через `resource_path`, совместимо с PyInstaller.
"""

import customtkinter as ctk
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys 
import re
import json
import webbrowser
from PIL import Image
import shutil
import logging
from logging.handlers import RotatingFileHandler
import platform
import subprocess

# РРјРїРѕСЂС‚РёСЂСѓРµРј РѕР±РЅРѕРІР»РµРЅРЅС‹Рµ РјРµРЅРµРґР¶РµСЂС‹ Рё РЅРѕРІС‹Р№ РјРµРЅРµРґР¶РµСЂ yt-dlp
from theme_manager_fixed import ThemeManager
from language_manager import LanguageManager
from yt_dlp_manager import YTDLPManager

APP_NAME = "YT-DLP GUI"
WIDTH = 900
HEIGHT = 700

def load_app_version():
    try:
        p = resource_path("app_version.txt")
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                v = f.read().strip()
                if v:
                    return v
    except Exception:
        pass
    return "dev"

# --- Р¤РЈРќРљР¦РРЇ Р”Р›РЇ РџРћР›РЈР§Р•РќРРЇ РџР РђР’РР›Р¬РќРћР“Рћ РџРЈРўР Рљ Р Р•РЎРЈР РЎРђРњ ---
def resource_path(relative_path):
    """ РџРѕР»СѓС‡Р°РµС‚ Р°Р±СЃРѕР»СЋС‚РЅС‹Р№ РїСѓС‚СЊ Рє СЂРµСЃСѓСЂСЃСѓ, СЂР°Р±РѕС‚Р°РµС‚ РєР°Рє РґР»СЏ СЃРєСЂРёРїС‚Р°, С‚Р°Рє Рё РґР»СЏ PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# =============================================================================
# РЈРњРќРђРЇ РџР РћР’Р•Р РљРђ РќРђР›РР§РРЇ FFMPEG
# =============================================================================
def get_ffmpeg_path():
    """ РќР°С…РѕРґРёС‚ РїСѓС‚СЊ Рє ffmpeg.exe, СЃРЅР°С‡Р°Р»Р° Р»РѕРєР°Р»СЊРЅРѕ, РїРѕС‚РѕРј РІ PATH. """
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    local_ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg_path):
        return local_ffmpeg_path
    return "ffmpeg"

def ffmpeg_available():
    """ РџСЂРѕРІРµСЂСЏРµС‚, РґРѕСЃС‚СѓРїРµРЅ Р»Рё FFmpeg РІ СЃРёСЃС‚РµРјРµ. """
    path = get_ffmpeg_path()
    return shutil.which(path) is not None

# --- Override with robust variants (support PyInstaller one-file) ---
def get_ffmpeg_path():
    """Return path to ffmpeg.exe bundled with the app or available in PATH.

    - If running under PyInstaller, files added via spec (sys._MEIPASS) are
      accessible through resource_path(). Prefer that if present.
    - Otherwise, look for ffmpeg.exe next to the executable/script.
    - Finally, fall back to just "ffmpeg" (expecting it in PATH).
    """
    # 1) Check bundled resource path (works for both dev and PyInstaller one-file)
    bundled = resource_path("ffmpeg.exe")
    if os.path.isabs(bundled) and os.path.exists(bundled):
        return bundled

    # 2) Check side-by-side with the executable/script
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    local_ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg_path):
        return local_ffmpeg_path

    # 3) Fallback: rely on PATH
    return "ffmpeg"

def ffmpeg_available():
    """Check that FFmpeg is available either bundled or in PATH."""
    path = get_ffmpeg_path()
    # If we have an absolute path, just confirm the file exists
    if os.path.isabs(path):
        return os.path.exists(path)
    # Otherwise, search in PATH
    return shutil.which(path) is not None

# =============================================================================
# Р›РћР“РР РћР’РђРќРР•
# =============================================================================
def get_logs_dir():
    base = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    path = os.path.join(base, "logs")
    os.makedirs(path, exist_ok=True)
    return path

def setup_file_logger():
    """РЎРѕР·РґР°РµС‚ Р»РѕРіРіРµСЂ СЃ СЂРѕС‚Р°С†РёРµР№ С„Р°Р№Р»РѕРІ."""
    logs_dir = get_logs_dir()
    log_path = os.path.join(logs_dir, "yt-dlp-gui.log")
    logger = logging.getLogger("yt_dlp_gui")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.propagate = False
    return logger, log_path

def clear_all_logs():
    """Р—Р°РєСЂС‹РІР°РµС‚ РѕР±СЂР°Р±РѕС‚С‡РёРєРё Р»РѕРіРѕРІ Рё СѓРґР°Р»СЏРµС‚ РІСЃРµ С„Р°Р№Р»С‹ Р»РѕРіРѕРІ."""
    logger = logging.getLogger("yt_dlp_gui")
    if not logger.handlers: return

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    logs_dir = get_logs_dir()
    for filename in os.listdir(logs_dir):
        if filename.startswith("yt-dlp-gui.log"):
            try:
                os.remove(os.path.join(logs_dir, filename))
            except OSError as e:
                print(f"РћС€РёР±РєР° СѓРґР°Р»РµРЅРёСЏ С„Р°Р№Р»Р° Р»РѕРіР° {filename}: {e}")
    
    setup_file_logger()

# --- РљРћРќР¤РР“РЈР РђР¦РРЇ ---
def get_config_path():
    """ РџРѕР»СѓС‡Р°РµС‚ РїСѓС‚СЊ Рє С„Р°Р№Р»Сѓ config.json """
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    return os.path.join(base_path, "config.json")

def load_or_create_config():
    """Р—Р°РіСЂСѓР¶Р°РµС‚ config.json РёР»Рё СЃРѕР·РґР°РµС‚ РµРіРѕ СЃ РЅР°СЃС‚СЂРѕР№РєР°РјРё РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ."""
    config_file_path = get_config_path()
    try:
        with open(config_file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # РР—РњР•РќР•РќРР•: РЇР·С‹Рє РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ С‚РµРїРµСЂСЊ РђРЅРіР»РёР№СЃРєРёР№
        return {
            "download_path": os.path.join(os.path.expanduser('~'), 'Downloads'),
            "theme": "Classic", "language": "English", "show_details": False,
            "video_quality": "1080p", "video_codec": "auto",
            "file_container": "mp4", "audio_format": "auto", "audio_bitrate": "192k",
            "network_mode": "Auto", "downloader": "builtin",
        }

# =============================================================================
# Р’РР”Р–Р•РўР« GUI (Р±РµР· РёР·РјРµРЅРµРЅРёР№)
# =============================================================================
class DownloadQueueItem(ctk.CTkFrame):
    def __init__(self, master, lang_manager, initial_title="..."):
        super().__init__(master, corner_radius=12)
        self.lang = lang_manager
        self.grid_columnconfigure(1, weight=1)
        self.icon_label = ctk.CTkLabel(self, text="рџ”„", font=ctk.CTkFont(size=22))
        self.icon_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")
        # Ensure valid icon glyph using emoji font or fallback
        try:
            self.icon_label.configure(text="🔁", font=ctk.CTkFont(family="Segoe UI Emoji", size=18))
        except Exception:
            self.icon_label.configure(text="↻")
        self.title_label = ctk.CTkLabel(self, text=initial_title, anchor="w", font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(self, height=8, corner_radius=100, border_width=0, bg_color=self.cget("fg_color")); self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=1, padx=(0, 10), pady=4, sticky="ew")
        self.status_label = ctk.CTkLabel(self, text="...", anchor="w", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")
        self.status_label.configure(text=self.lang.get("download_info_getting"))

    def set_title(self, title):
        max_len = 50
        display_title = (title[:max_len] + '...') if len(title) > max_len else title
        self.title_label.configure(text=display_title)

    def update_progress(self, percentage, status_text):
        pct = max(0.0, min(100.0, float(percentage)))
        self.progress_bar.set(pct / 100)
        self.status_label.configure(text=status_text)

    def set_complete(self, final_text=""):
        self.progress_bar.set(1)
        self.status_label.configure(text=final_text or self.lang.get("download_complete"), text_color=("#1f9340", "#32a852"))
        try:
            self.icon_label.configure(text="✅")
        except Exception:
            self.icon_label.configure(text="✔")
        self.icon_label.configure(text="вњ…")

    def set_error(self, text=""):
        self.status_label.configure(text=text or self.lang.get("download_error"), text_color=("#d94848", "#e85151"))
        try:
            self.icon_label.configure(text="❌")
        except Exception:
            self.icon_label.configure(text="✖")
        self.icon_label.configure(text="вќЊ")

    def set_cancelled(self):
        self.status_label.configure(text=self.lang.get("download_cancelled"), text_color="gray")
        try:
            self.icon_label.configure(text="🚫")
        except Exception:
            self.icon_label.configure(text="×")
        self.icon_label.configure(text="рџљ«")

class SiteListFrame(ctk.CTkFrame):
    def __init__(self, master, lang_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.lang = lang_manager
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        self.all_sites = []
        self.is_populated = False
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(controls_frame)
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search)
        self.sort_az_button = ctk.CTkButton(controls_frame, text="A-Z", width=60, command=self._sort_az)
        self.sort_az_button.grid(row=0, column=1, padx=(0, 5))
        self.sort_za_button = ctk.CTkButton(controls_frame, text="Z-A", width=60, command=self._sort_za)
        self.sort_za_button.grid(row=0, column=2)
        self.textbox = ctk.CTkTextbox(self, wrap="none", height=250, font=ctk.CTkFont(family="Consolas", size=13))
        self.textbox.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")
        self.textbox.configure(state="disabled")

    def populate_sites(self, site_list):
        self.all_sites = sorted(site_list); self.is_populated = True
        self.update_texts(); self._update_display(self.all_sites)

    def update_texts(self):
        if self.is_populated: self.search_entry.configure(placeholder_text=self.lang.get("search_sites_placeholder", count=len(self.all_sites)))

    def _update_display(self, sites_to_display):
        max_len = max(len(s) for s in sites_to_display) if sites_to_display else 0
        col_width = max(max_len + 4, 25)
        self.after(50, lambda: self._format_columns(sites_to_display, col_width))

    def _format_columns(self, sites_to_display, col_width):
        if not self.winfo_exists(): return
        try:
            font = ctk.CTkFont(family="Consolas", size=13); char_width = font.measure("W")
            num_cols = max(1, self.textbox.winfo_width() // char_width // col_width)
        except: num_cols = max(1, self.textbox.winfo_width() // 8 // col_width)
        num_rows = (len(sites_to_display) + num_cols - 1) // num_cols
        output_lines = ["".join(sites_to_display[i + j * num_rows].ljust(col_width) for j in range(num_cols) if i + j * num_rows < len(sites_to_display)) for i in range(num_rows)]
        self.textbox.configure(state="normal"); self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", "\n".join(output_lines)); self.textbox.configure(state="disabled")

    def _on_search(self, event=None):
        if not self.is_populated: return
        search_term = self.search_entry.get().lower()
        self._update_display([site for site in self.all_sites if search_term in site.lower()])

    def _sort_az(self): self.all_sites.sort(); self._on_search()
    def _sort_za(self): self.all_sites.sort(reverse=True); self._on_search()

class CollapsibleFrame(ctk.CTkFrame):
    def __init__(self, master, lang_manager, main_content_widget=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.lang = lang_manager; self.grid_columnconfigure(0, weight=1)
        self.is_collapsed = True; self.content_is_populated = False
        self.load_function = None; self.content_widget = None
        self.main_content_widget = main_content_widget
        self.button = ctk.CTkButton(self, command=self.toggle)
        self.button.grid(row=0, column=0, sticky="ew")
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.update_button_text()

    def update_button_text(self):
        arrow = "▼" if self.is_collapsed else "▲"
        text = f"{arrow}  {self.lang.get('show_sites_button')}" if self.is_collapsed else f"{arrow}  {self.lang.get('hide_sites_button')}"
        self.button.configure(text=text)
        # Ensure proper arrow glyphs regardless of encoding glitches
        try:
            arrow2 = "▼" if self.is_collapsed else "▲"
            fixed_text = f"{arrow2}  {self.lang.get('show_sites_button')}" if self.is_collapsed else f"{arrow2}  {self.lang.get('hide_sites_button')}"
            self.button.configure(text=fixed_text)
        except Exception:
            pass

    def set_load_function(self, func): self.load_function = func
    def toggle(self):
        self.is_collapsed = not self.is_collapsed
        self.update_button_text()
        if self.is_collapsed: self._collapse()
        else:
            if not self.content_is_populated and self.load_function: self.load_function(self)
            else: self._expand()

    def populate(self, sites_data):
        if self.content_widget: self.content_widget.destroy()
        self.content_widget = SiteListFrame(self.content_container, lang_manager=self.lang)
        self.content_widget.populate_sites(sites_data)
        self.content_widget.pack(fill="both", expand=True)
        self.content_is_populated = True
        self._expand()

    def _expand(self):
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=5)
        try:
            self.update_idletasks()
            self._check_and_adjust_layout()
        except Exception:
            pass

    def _collapse(self):
        self.content_container.grid_forget()
        if self.main_content_widget:
            try:
                self.main_content_widget.grid_configure(pady=0)
            except Exception:
                pass

    def _check_and_adjust_layout(self):
        if not self.main_content_widget:
            return
        self.main_content_widget.update_idletasks()
        self.winfo_toplevel().update_idletasks()
        try:
            main_bottom_y = self.main_content_widget.winfo_y() + self.main_content_widget.winfo_height()
            list_top_y = self.master.winfo_y()
            overlap = main_bottom_y - list_top_y
            if overlap > 0:
                self.main_content_widget.grid_configure(pady=(0, overlap + 130))
            else:
                self.main_content_widget.grid_configure(pady=0)
        except Exception:
            pass
    
# =============================================================================
# Р“Р›РђР’РќР«Р™ РљР›РђРЎРЎ РџР РР›РћР–Р•РќРРЇ
# =============================================================================
class App(ctk.CTk):
    SETTINGS_VIDEO = "settings_video"; SETTINGS_AUDIO = "settings_audio"
    SETTINGS_APPEARANCE = "settings_appearance"; SETTINGS_ADVANCED = "settings_advanced"
    INFO_WHAT_IS_THIS = "info_what_is_this"; INFO_COMMUNITY = "info_community"
    INFO_PRIVACY = "info_privacy"; INFO_ETHICS = "info_ethics"; INFO_LICENSES = "info_licenses"

    def __init__(self, initial_settings: dict):
        super().__init__()
        # Set dynamic title with version (from app_version.txt when built by CI)
        try:
            self.title(f"{APP_NAME} {load_app_version()}")
        except Exception:
            pass
        self.logger, self.log_file_path = setup_file_logger()
        self.logger.info(f"App start: {APP_NAME}")
        self.logger.info(f"Python={sys.version.split()[0]} | OS={platform.system()} {platform.release()}")
        
        self.lang = LanguageManager()
        self.theme_manager = ThemeManager()
        self.ytdlp_manager = YTDLPManager(logger_callback=self.logger.info)

        self.is_running = True
        self.download_thread = None
        self.download_process = None
        self.download_cancelled = threading.Event()
        self.download_widget = None
        self.quick_override = None
        self.last_error_line = ""
        # Queue and history
        self.current_output_file = None
        self.pending_queue = []  # list of URLs
        self.download_history = []  # list of dicts: {title,path,status,error?}
        self.queue_overlay = None
        self.queue_add_button = None
        self.active_settings_frame = self.SETTINGS_VIDEO
        self.active_info_frame = self.INFO_WHAT_IS_THIS
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        try: self.iconbitmap(resource_path("icon.ico"))
        except Exception as e: self.logger.error(f"Icon loading error: {e}")
        
        self.logo_image = None
        try: self.logo_image = ctk.CTkImage(Image.open(resource_path("logo_bg.png")), size=(128, 128))
        except Exception as e: self.logger.error(f"Logo loading error: {e}")

        self.bitrate_map = {"Р›СѓС‡С€РёР№": "0", "Best": "0", "320k": "320", "192k": "192", "128k": "128", "96k": "96"}
        
        self.theme_var = ctk.StringVar(); self.language_var = ctk.StringVar()
        self.show_details_var = ctk.BooleanVar()
        self.download_mode_var = ctk.StringVar()
        self.video_quality_var = ctk.StringVar(); self.video_codec_var = ctk.StringVar()
        self.container_var = ctk.StringVar()
        self.audio_format_var = ctk.StringVar(); self.audio_bitrate_var = ctk.StringVar()
        self.network_mode_var = ctk.StringVar(); self.downloader_var = ctk.StringVar()

        self.load_settings(initial_settings)
        
        # РР—РњР•РќР•РќРР•: РЈСЃС‚Р°РЅР°РІР»РёРІР°РµРј СЏР·С‹Рє РґРѕ РїРѕСЃС‚СЂРѕРµРЅРёСЏ РёРЅС‚РµСЂС„РµР№СЃР°
        self.lang.set_language(self.language_var.get())

        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)
        
        self.build_ui()
        self.update_all_texts() # РџСЂРёРјРµРЅСЏРµРј С‚РµРєСЃС‚С‹ РєРѕ РІСЃРµРј РІРёРґР¶РµС‚Р°Рј

        threading.Thread(target=self.initial_ytdlp_check, daemon=True).start()

    def initial_ytdlp_check(self):
        """РџСЂРѕРІРµСЂСЏРµС‚ РЅР°Р»РёС‡РёРµ yt-dlp.exe РїСЂРё Р·Р°РїСѓСЃРєРµ Рё СЃРєР°С‡РёРІР°РµС‚, РµСЃР»Рё РµРіРѕ РЅРµС‚."""
        if not os.path.exists(self.ytdlp_manager.executable_path):
            self.logger.info("yt-dlp.exe not found, starting initial download.")
            self.update_status(self.lang.get("update_status_downloading"))
            update_generator = self.ytdlp_manager.check_and_update(force=True)
            for status in update_generator:
                if status == "downloading":
                    self.after(0, self.update_status, self.lang.get("update_status_downloading"))
            self.after(0, self.update_status, self.lang.get("ready_status"))

    def load_settings(self, settings: dict):
        self.download_path = settings.get("download_path", os.path.join(os.path.expanduser('~'), 'Downloads'))
        if not os.path.exists(self.download_path): os.makedirs(self.download_path, exist_ok=True)
        self.theme_var.set(settings.get("theme", "Classic"))
        self.language_var.set(settings.get("language", "English")) # РџРѕ СѓРјРѕР»С‡Р°РЅРёСЋ Р°РЅРіР»РёР№СЃРєРёР№
        self.show_details_var.set(settings.get("show_details", False))
        self.video_quality_var.set(settings.get("video_quality", "1080p"))
        self.video_codec_var.set(settings.get("video_codec", "auto"))
        self.container_var.set(settings.get("file_container", "mp4"))
        self.audio_format_var.set(settings.get("audio_format", "auto"))
        self.audio_bitrate_var.set(settings.get("audio_bitrate", "192k"))
        self.network_mode_var.set(settings.get("network_mode", "Auto"))
        self.downloader_var.set(settings.get("downloader", "builtin"))

    def on_closing(self):
        self.save_settings(); self.is_running = False
        self.cancel_download(); self.destroy()

    def save_settings(self):
        config_file_path = get_config_path()
        dl_val = str(self.downloader_var.get())
        dl_code = "aria2c" if dl_val == self.lang.get("downloader_aria2c") or dl_val.lower() == "aria2c" else "builtin"
        settings = {
            "download_path": self.download_path, "theme": self.theme_var.get(),
            "language": self.language_var.get(), "show_details": self.show_details_var.get(),
            "video_quality": self.video_quality_var.get(), "video_codec": self.video_codec_var.get(),
            "file_container": self.container_var.get(), "audio_format": self.audio_format_var.get(),
            "audio_bitrate": self.audio_bitrate_var.get(),
            "network_mode": self.network_mode_var.get(),
            "downloader": dl_code,
        }
        try:
            with open(config_file_path, "w", encoding='utf-8') as f: json.dump(settings, f, indent=4)
        except Exception as e: self.logger.error(f"Failed to save settings: {e}")

    def _rebuild_ui(self, go_home: bool = False):
        """РџРµСЂРµСЃС‚СЂР°РёРІР°РµС‚ РІРµСЃСЊ РёРЅС‚РµСЂС„РµР№СЃ, РІСЃРµРіРґР° РІРѕР·РІСЂР°С‰Р°СЏСЃСЊ РЅР° РіР»Р°РІРЅСѓСЋ РІРєР»Р°РґРєСѓ."""
        try:
            current_tab = self.lang.get("home_tab") if go_home else self.tab_view.get()
        except Exception:
            current_tab = self.lang.get("home_tab")
        for widget in self.winfo_children():
            widget.destroy()
        self.build_ui()
        self.update_all_texts()
        try:
            self.tab_view.set(current_tab)
        except Exception:
            self.tab_view.set(self.lang.get("home_tab"))
        
    def apply_theme(self, theme_name: str):
        theme_data = self.theme_manager.get_theme_data(theme_name)
        if not theme_data: return
        ctk.set_appearance_mode(theme_data["appearance"])
        if theme_data["type"] == "built-in": ctk.set_default_color_theme(theme_data["name"])
        else: ctk.set_default_color_theme(theme_data["path"])
        self.after(50, self._rebuild_ui, True)
        
    def change_language(self, lang_name: str):
        if self.lang.set_language(lang_name):
            self.language_var.set(lang_name)
            self.after(50, self._rebuild_ui, True)

    def build_ui(self):
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.home_tab = self.tab_view.add(self.lang.get("home_tab"))
        self.settings_tab = self.tab_view.add(self.lang.get("settings_tab"))
        self.maintenance_tab = self.tab_view.add(self.lang.get("maintenance_tab"))
        self.info_tab = self.tab_view.add(self.lang.get("info_tab"))
        self.status_frame = ctk.CTkFrame(self, corner_radius=0, height=30)
        self.status_label = ctk.CTkLabel(self.status_frame, text="")
        self.status_label.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="w")
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.configure_main_tab(); self.configure_settings_tab(); self.configure_maintenance_tab(); self.configure_info_tab()
        self.toggle_details_bar()
        self.tab_view.set(self.lang.get("home_tab"))

    def configure_main_tab(self):
        main_tab = self.home_tab
        main_tab.grid_columnconfigure(0, weight=1); main_tab.grid_rowconfigure(0, weight=1)
        main_container = ctk.CTkFrame(main_tab, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1); main_container.grid_rowconfigure(0, weight=1)
        main_block = ctk.CTkFrame(main_container)
        main_block.grid(row=0, column=0)
        if self.logo_image:
            ctk.CTkLabel(main_block, image=self.logo_image, text="").pack(pady=(20, 10))
        self.app_title_label = ctk.CTkLabel(main_block, text=APP_NAME, font=ctk.CTkFont(size=36, weight="bold"))
        self.app_title_label.pack(pady=(0, 20))
        url_frame = ctk.CTkFrame(main_block)
        url_frame.pack(pady=10, fill="x")
        url_frame.grid_columnconfigure(1, weight=1)
        self.url_entry = ctk.CTkEntry(url_frame, height=50, font=ctk.CTkFont(size=14))
        self.url_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.paste_button = ctk.CTkButton(url_frame, height=40, command=self.paste_from_clipboard, font=ctk.CTkFont(size=14, weight="bold"))
        self.paste_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        path_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        path_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        path_frame.grid_columnconfigure(1, weight=1)
        self.path_button = ctk.CTkButton(path_frame, height=40, command=self.select_folder, font=ctk.CTkFont(size=14, weight="bold"))
        self.path_button.grid(row=0, column=0, padx=(0, 10))
        self.path_label = ctk.CTkLabel(path_frame, text=self.download_path, text_color="gray", anchor="w", justify="left", font=ctk.CTkFont(size=14))
        self.path_label.grid(row=0, column=1, sticky="ew")
        self.download_button = ctk.CTkButton(url_frame, height=40, command=self.start_download_thread, font=ctk.CTkFont(size=14, weight="bold"))
        self.download_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        # Shown only during active download to enqueue next URLs
        self.queue_add_button = ctk.CTkButton(url_frame, height=40, text="+ Queue", command=self.add_to_queue, font=ctk.CTkFont(size=14))
        self.queue_add_button.grid(row=1, column=3, padx=(10, 0), pady=10)
        self.queue_add_button.grid_remove()
        self.mode_segmented_button = ctk.CTkSegmentedButton(main_block, variable=self.download_mode_var, height=45, font=ctk.CTkFont(size=14))
        self.mode_segmented_button.pack(pady=10, fill="x")
        quick_row = ctk.CTkFrame(main_block, fg_color="transparent")
        quick_row.pack(pady=(0, 5), fill="x")
        quick_inner = ctk.CTkFrame(quick_row, fg_color="transparent")
        quick_inner.pack(anchor="center")
        self.quick_best_btn = ctk.CTkButton(quick_inner, height=36, command=lambda: self.quick_download("best"))
        self.quick_best_btn.grid(row=0, column=0, padx=(0, 10))
        self.quick_compat_btn = ctk.CTkButton(quick_inner, height=36, command=lambda: self.quick_download("compat"))
        self.quick_compat_btn.grid(row=0, column=1)
        sites_container = ctk.CTkFrame(main_tab, fg_color="transparent", width=800)
        sites_container.place(relx=0.5, rely=1.0, anchor="s", y=-10)
        self.sites_widget = CollapsibleFrame(sites_container, lang_manager=self.lang, main_content_widget=main_block)
        self.sites_widget.pack(fill="x", expand=True)
        self.sites_widget.set_load_function(self.load_supported_sites_in_thread)

    def configure_settings_tab(self):
        settings_tab = self.settings_tab
        settings_tab.grid_columnconfigure(1, weight=1); settings_tab.grid_rowconfigure(0, weight=1)
        nav_frame = ctk.CTkFrame(settings_tab, width=200, corner_radius=0)
        nav_frame.grid(row=0, column=0, sticky="nsw"); nav_frame.grid_rowconfigure(4, weight=1)
        self.settings_content_frame = ctk.CTkFrame(settings_tab, fg_color="transparent")
        self.settings_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.settings_frames = {
            self.SETTINGS_VIDEO: self.create_video_settings_frame(self.settings_content_frame),
            self.SETTINGS_AUDIO: self.create_audio_settings_frame(self.settings_content_frame),
            self.SETTINGS_APPEARANCE: self.create_appearance_settings_frame(self.settings_content_frame),
            self.SETTINGS_ADVANCED: self.create_advanced_settings_frame(self.settings_content_frame)
        }
        button_font = ctk.CTkFont(size=16, weight="bold")
        self.settings_video_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_settings_frame(self.SETTINGS_VIDEO))
        self.settings_video_button.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.settings_audio_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_settings_frame(self.SETTINGS_AUDIO))
        self.settings_audio_button.grid(row=1, column=0, padx=15, pady=15, sticky="ew")
        self.settings_appearance_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_settings_frame(self.SETTINGS_APPEARANCE))
        self.settings_appearance_button.grid(row=2, column=0, padx=15, pady=15, sticky="ew")
        self.settings_advanced_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_settings_frame(self.SETTINGS_ADVANCED))
        self.settings_advanced_button.grid(row=3, column=0, padx=15, pady=15, sticky="ew")
        self.show_settings_frame(self.active_settings_frame)

    def configure_maintenance_tab(self):
        maintenance_tab = self.maintenance_tab
        maintenance_tab.grid_columnconfigure(0, weight=1); maintenance_tab.grid_rowconfigure(2, weight=1)
        main_frame = ctk.CTkFrame(maintenance_tab, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")
        main_frame.grid_columnconfigure(0, weight=1)
        self.maintenance_title_label = ctk.CTkLabel(main_frame, font=ctk.CTkFont(size=22, weight="bold"))
        self.maintenance_title_label.pack(pady=(5, 25), padx=10, anchor="w")
        update_frame = ctk.CTkFrame(main_frame, width=450)
        update_frame.pack(pady=10, anchor="w", fill="x")
        maintenance_btn_font = ctk.CTkFont(size=16, weight="bold")
        self.update_button = ctk.CTkButton(update_frame, height=50, width=220, font=maintenance_btn_font, command=self.update_ytdlp_in_thread)
        self.update_button.pack(side="left", padx=15, pady=12)
        self.update_label = ctk.CTkLabel(update_frame, justify="left", font=ctk.CTkFont(size=16))
        self.update_label.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        logs_frame = ctk.CTkFrame(main_frame, width=450)
        logs_frame.pack(pady=10, anchor="w", fill="x")
        self.logs_button = ctk.CTkButton(logs_frame, height=50, width=220, font=maintenance_btn_font, command=self.open_logs_folder)
        self.logs_button.pack(side="left", padx=15, pady=12)
        self.logs_label = ctk.CTkLabel(logs_frame, justify="left", font=ctk.CTkFont(size=16))
        self.logs_label.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        # РќРћР’Р«Р™ Р’РР”Р–Р•Рў: РћС‡РёСЃС‚РєР° Р»РѕРіРѕРІ
        clear_logs_frame = ctk.CTkFrame(main_frame, width=450)
        clear_logs_frame.pack(pady=10, anchor="w", fill="x")
        self.clear_logs_button = ctk.CTkButton(clear_logs_frame, height=50, width=220, font=maintenance_btn_font, command=self.confirm_clear_logs)
        self.clear_logs_button.pack(side="left", padx=15, pady=12)
        self.clear_logs_label = ctk.CTkLabel(clear_logs_frame, justify="left", font=ctk.CTkFont(size=16))
        self.clear_logs_label.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        # Bind dynamic wraplength to fit container width nicely
        self._bind_dynamic_wraplength(self.update_label, update_frame, self.update_button)
        self._bind_dynamic_wraplength(self.logs_label, logs_frame, self.logs_button)
        self._bind_dynamic_wraplength(self.clear_logs_label, clear_logs_frame, self.clear_logs_button)

    def configure_info_tab(self):
        info_tab = self.info_tab
        info_tab.grid_columnconfigure(1, weight=1); info_tab.grid_rowconfigure(0, weight=1)
        nav_frame = ctk.CTkFrame(info_tab, width=200, corner_radius=0)
        nav_frame.grid(row=0, column=0, sticky="nsw"); nav_frame.grid_rowconfigure(5, weight=1)
        self.info_content_textbox = ctk.CTkTextbox(info_tab, wrap="word", fg_color="transparent", font=ctk.CTkFont(size=14))
        self.info_content_textbox.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.info_content_textbox.tag_config("hyperlink", foreground="#58a6ff", underline=True)
        self.info_content_textbox.tag_bind("hyperlink", "<Enter>", self._on_link_enter)
        self.info_content_textbox.tag_bind("hyperlink", "<Leave>", self._on_link_leave)
        self.info_content_textbox.tag_bind("hyperlink", "<Button-1>", self._open_link)
        self.info_content_textbox.configure(state="disabled")
        button_font = ctk.CTkFont(size=16, weight="bold")
        self.info_what_is_this_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_info_frame(self.INFO_WHAT_IS_THIS))
        self.info_what_is_this_button.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.info_community_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_info_frame(self.INFO_COMMUNITY))
        self.info_community_button.grid(row=1, column=0, padx=15, pady=15, sticky="ew")
        self.info_privacy_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_info_frame(self.INFO_PRIVACY))
        self.info_privacy_button.grid(row=2, column=0, padx=15, pady=15, sticky="ew")
        self.info_ethics_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_info_frame(self.INFO_ETHICS))
        self.info_ethics_button.grid(row=3, column=0, padx=15, pady=15, sticky="ew")
        self.info_licenses_button = ctk.CTkButton(nav_frame, height=50, font=button_font, command=lambda: self.show_info_frame(self.INFO_LICENSES))
        self.info_licenses_button.grid(row=4, column=0, padx=15, pady=15, sticky="ew")
        self.show_info_frame(self.active_info_frame)

    def show_info_frame(self, frame_name):
        self.active_info_frame = frame_name
        content = self.lang.get(frame_name.replace("info_", "info_content_"))
        self.info_content_textbox.configure(state="normal")
        self.info_content_textbox.delete("1.0", "end")
        self.info_content_textbox.insert("1.0", content)
        self._highlight_links(content)
        self.info_content_textbox.configure(state="disabled")

    def _highlight_links(self, text):
        for match in re.finditer(r"https?://[^\s\[\]\(\)]+", text):
            self.info_content_textbox.tag_add("hyperlink", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    def _bind_dynamic_wraplength(self, label_widget, container_widget, left_widget=None, padding: int = 30, min_width: int = 320):
        """Dynamically adjust a label's wraplength to container width minus left-side widget width.
        Keeps long maintenance descriptions readable across window resizes.
        """
        def _update(event=None):
            try:
                cont_w = max(container_widget.winfo_width(), 0)
                left_w = max(left_widget.winfo_width(), 0) if left_widget else 0
                wrap = max(min_width, cont_w - left_w - padding)
                label_widget.configure(wraplength=wrap)
            except Exception:
                pass
        container_widget.bind("<Configure>", _update)
        if left_widget:
            left_widget.bind("<Configure>", _update)
        self.after(100, _update)

    def _on_link_enter(self, event): self.info_content_textbox.configure(cursor="hand2")
    def _on_link_leave(self, event): self.info_content_textbox.configure(cursor="")
    def _open_link(self, event):
        index = self.info_content_textbox.index(f"@{event.x},{event.y}")
        if "hyperlink" in self.info_content_textbox.tag_names(index):
            tag_range = self.info_content_textbox.tag_ranges("hyperlink")
            for i in range(0, len(tag_range), 2):
                start, end = tag_range[i], tag_range[i+1]
                if self.info_content_textbox.compare(index, ">=", start) and self.info_content_textbox.compare(index, "<", end):
                    webbrowser.open_new_tab(self.info_content_textbox.get(start, end)); break

    def update_all_texts(self):
        self.title(self.lang.get("app_title"))
        self.status_label.configure(text=self.lang.get("ready_status"))
        self.url_entry.configure(placeholder_text=self.lang.get("paste_placeholder"))
        self.paste_button.configure(text=self.lang.get("paste_button"))
        self.path_button.configure(text=self.lang.get("select_folder_button"))
        self.download_button.configure(text=self.lang.get("download_button"))
        mode_options = [self.lang.get(m) for m in ["mode_auto", "mode_video", "mode_audio", "mode_video_only"]]
        self.mode_segmented_button.configure(values=mode_options)
        if self.download_mode_var.get() not in mode_options: self.download_mode_var.set(mode_options[0])
        self.quick_best_btn.configure(text=self.lang.get("quick_best_button"))
        self.quick_compat_btn.configure(text=self.lang.get("quick_compat_button"))
        self.sites_widget.update_button_text()
        if self.sites_widget.content_widget: self.sites_widget.content_widget.update_texts()
        self.settings_video_button.configure(text=self.lang.get("settings_video"))
        self.settings_audio_button.configure(text=self.lang.get("settings_audio"))
        self.settings_appearance_button.configure(text=self.lang.get("settings_appearance"))
        self.settings_advanced_button.configure(text=self.lang.get("settings_advanced"))
        self.video_settings_title_label.configure(text=self.lang.get("video_settings_title"))
        self.video_quality_label.configure(text=self.lang.get("video_quality"))
        self.video_quality_seg_button.configure(values=[self.lang.get("quality_best"), "8k", "4k", "1440p", "1080p", "720p", "480p", "360p"])
        self.video_codec_label.configure(text=self.lang.get("video_codec"))
        self.video_codec_seg_button.configure(values=["auto", self.lang.get("codec_h264"), "vp9", self.lang.get("codec_av1")])
        self.container_label.configure(text=self.lang.get("file_container"))
        self.audio_settings_title_label.configure(text=self.lang.get("audio_settings_title"))
        self.audio_format_label.configure(text=self.lang.get("audio_format"))
        self.audio_bitrate_label.configure(text=self.lang.get("audio_bitrate"))
        self.audio_bitrate_seg_button.configure(values=[self.lang.get("quality_best"), "320k", "192k", "128k", "96k"])
        self.appearance_title_label.configure(text=self.lang.get("appearance_settings_title"))
        self.theme_label.configure(text=self.lang.get("theme_label"))
        self.language_label.configure(text=self.lang.get("language_label"))
        self.language_option_menu.configure(values=list(self.lang.language_map.keys()))
        self.advanced_title_label.configure(text=self.lang.get("advanced_settings_title"))
        self.show_details_label.configure(text=self.lang.get("show_details_switch"))
        self.network_mode_label.configure(text=self.lang.get("network_mode"))
        self.network_mode_seg.configure(values=[self.lang.get(n) for n in ["network_auto", "network_ipv4", "network_ipv6"]])
        # Normalize network segmented value to current language
        network_options = [self.lang.get(n) for n in ["network_auto", "network_ipv4", "network_ipv6"]]
        if self.network_mode_var.get() not in network_options:
            cur = str(self.network_mode_var.get())
            if cur.lower() in ("auto",):
                self.network_mode_var.set(self.lang.get("network_auto"))
            elif cur.lower() in ("ipv4", "force ipv4"):
                self.network_mode_var.set(self.lang.get("network_ipv4"))
            elif cur.lower() in ("ipv6", "force ipv6"):
                self.network_mode_var.set(self.lang.get("network_ipv6"))
            else:
                self.network_mode_var.set(network_options[0])
        self.downloader_label.configure(text=self.lang.get("downloader_engine"))
        self.downloader_seg.configure(values=[self.lang.get(d) for d in ["downloader_builtin", "downloader_aria2c"]])
        # Normalize downloader segmented value to current language
        downloader_options = [self.lang.get(d) for d in ["downloader_builtin", "downloader_aria2c"]]
        if self.downloader_var.get() not in downloader_options:
            cur = str(self.downloader_var.get())
            if cur.lower() in ("builtin", "built-in", "built in"):
                self.downloader_var.set(self.lang.get("downloader_builtin"))
            elif cur.lower() == "aria2c":
                self.downloader_var.set(self.lang.get("downloader_aria2c"))
            else:
                self.downloader_var.set(downloader_options[0])
        self.maintenance_title_label.configure(text=self.lang.get("maintenance_title"))
        self.update_button.configure(text=self.lang.get("update_button"))
        self.update_label.configure(text=self.lang.get("update_label"))
        self.logs_button.configure(text=self.lang.get("logs_button"))
        self.logs_label.configure(text=self.lang.get("logs_label"))
        self.clear_logs_button.configure(text=self.lang.get("clear_logs_button"))
        self.clear_logs_label.configure(text=self.lang.get("clear_logs_label"))
        self.info_what_is_this_button.configure(text=self.lang.get("info_nav_what_is_this"))
        self.info_community_button.configure(text=self.lang.get("info_nav_community"))
        self.info_privacy_button.configure(text=self.lang.get("info_nav_privacy"))
        self.info_ethics_button.configure(text=self.lang.get("info_nav_ethics"))
        self.info_licenses_button.configure(text=self.lang.get("info_nav_licenses"))
        self.show_info_frame(self.active_info_frame)

    def show_settings_frame(self, frame_name):
        for frame in self.settings_frames.values(): frame.grid_forget()
        self.settings_frames[frame_name].grid(row=0, column=0, sticky="nw")
        self.active_settings_frame = frame_name

    def create_video_settings_frame(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        self.video_settings_title_label = ctk.CTkLabel(frame, font=ctk.CTkFont(size=22, weight="bold"))
        self.video_settings_title_label.pack(pady=(5, 25), padx=10, anchor="w")
        quality_frame = ctk.CTkFrame(frame, width=450); quality_frame.pack(pady=10, anchor="w")
        self.video_quality_label = ctk.CTkLabel(quality_frame, font=ctk.CTkFont(size=16))
        self.video_quality_label.pack(pady=10, padx=15, anchor="w")
        self.video_quality_seg_button = ctk.CTkSegmentedButton(quality_frame, variable=self.video_quality_var, height=40, font=ctk.CTkFont(size=14))
        self.video_quality_seg_button.pack(pady=(5, 15), padx=15)
        codec_frame = ctk.CTkFrame(frame, width=450); codec_frame.pack(pady=10, anchor="w")
        self.video_codec_label = ctk.CTkLabel(codec_frame, font=ctk.CTkFont(size=16))
        self.video_codec_label.pack(pady=10, padx=15, anchor="w")
        self.video_codec_seg_button = ctk.CTkSegmentedButton(codec_frame, variable=self.video_codec_var, height=40, font=ctk.CTkFont(size=14))
        self.video_codec_seg_button.pack(pady=(5, 15), padx=15)
        container_frame = ctk.CTkFrame(frame, width=450); container_frame.pack(pady=10, anchor="w")
        self.container_label = ctk.CTkLabel(container_frame, font=ctk.CTkFont(size=16))
        self.container_label.pack(pady=10, padx=15, anchor="w")
        self.container_seg_button = ctk.CTkSegmentedButton(container_frame, values=["auto", "mp4", "mkv", "webm"], variable=self.container_var, height=40, font=ctk.CTkFont(size=16))
        self.container_seg_button.pack(pady=(5, 15), padx=15, anchor="w")
        return frame

    def create_audio_settings_frame(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        self.audio_settings_title_label = ctk.CTkLabel(frame, font=ctk.CTkFont(size=22, weight="bold")); self.audio_settings_title_label.pack(pady=(5, 25), padx=10, anchor="w")
        audio_format_frame = ctk.CTkFrame(frame, width=450); audio_format_frame.pack(pady=10, anchor="w")
        self.audio_format_label = ctk.CTkLabel(audio_format_frame, font=ctk.CTkFont(size=16)); self.audio_format_label.pack(pady=10, padx=15, anchor="w")
        self.audio_format_seg_button = ctk.CTkSegmentedButton(audio_format_frame, values=["auto", "mp3", "opus", "wav", "m4a"], variable=self.audio_format_var, height=40, font=ctk.CTkFont(size=14)); self.audio_format_seg_button.pack(pady=(5,15), padx=15)
        bitrate_frame = ctk.CTkFrame(frame, width=450); bitrate_frame.pack(pady=10, anchor="w")
        self.audio_bitrate_label = ctk.CTkLabel(bitrate_frame, font=ctk.CTkFont(size=16)); self.audio_bitrate_label.pack(pady=10, padx=15, anchor="w")
        self.audio_bitrate_seg_button = ctk.CTkSegmentedButton(bitrate_frame, variable=self.audio_bitrate_var, height=40, font=ctk.CTkFont(size=14)); self.audio_bitrate_seg_button.pack(pady=(5,15), padx=15)
        return frame

    def create_appearance_settings_frame(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        self.appearance_title_label = ctk.CTkLabel(frame, font=ctk.CTkFont(size=22, weight="bold")); self.appearance_title_label.pack(pady=(5, 25), padx=10, anchor="w")
        theme_frame = ctk.CTkFrame(frame, width=450); theme_frame.pack(pady=10, anchor="w", fill="x")
        self.theme_label = ctk.CTkLabel(theme_frame, font=ctk.CTkFont(size=16)); self.theme_label.pack(pady=10, padx=15, anchor="w")
        self.theme_option_menu = ctk.CTkOptionMenu(theme_frame, values=list(self.theme_manager.themes.keys()), command=self.apply_theme, variable=self.theme_var, height=40, font=ctk.CTkFont(size=14)); self.theme_option_menu.pack(pady=(5,15), padx=15, fill="x")
        lang_frame = ctk.CTkFrame(frame, width=450); lang_frame.pack(pady=10, anchor="w", fill="x")
        self.language_label = ctk.CTkLabel(lang_frame, font=ctk.CTkFont(size=16)); self.language_label.pack(pady=10, padx=15, anchor="w")
        self.language_option_menu = ctk.CTkOptionMenu(lang_frame, values=list(self.lang.language_map.keys()), command=self.change_language, variable=self.language_var, height=40, font=ctk.CTkFont(size=14)); self.language_option_menu.pack(pady=(5,15), padx=15, fill="x")
        return frame

    def create_advanced_settings_frame(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        self.advanced_title_label = ctk.CTkLabel(frame, font=ctk.CTkFont(size=22, weight="bold")); self.advanced_title_label.pack(pady=(5, 25), padx=10, anchor="w")
        details_frame = ctk.CTkFrame(frame, width=450); details_frame.pack(pady=10, anchor="w")
        details_frame.grid_columnconfigure(1, weight=1)
        self.show_details_label = ctk.CTkLabel(details_frame, font=ctk.CTkFont(size=16)); self.show_details_label.grid(row=0, column=0, pady=15, padx=15, sticky="w")
        ctk.CTkSwitch(details_frame, text="", variable=self.show_details_var, command=self.toggle_details_bar).grid(row=0, column=1, pady=15, padx=15, sticky="e")
        net_frame = ctk.CTkFrame(frame, width=450); net_frame.pack(pady=10, anchor="w")
        self.network_mode_label = ctk.CTkLabel(net_frame, font=ctk.CTkFont(size=16)); self.network_mode_label.pack(pady=10, padx=15, anchor="w")
        self.network_mode_seg = ctk.CTkSegmentedButton(net_frame, variable=self.network_mode_var, height=40, font=ctk.CTkFont(size=14))
        self.network_mode_seg.pack(pady=(5,15), padx=15, anchor="w")
        dl_frame = ctk.CTkFrame(frame, width=450); dl_frame.pack(pady=10, anchor="w")
        self.downloader_label = ctk.CTkLabel(dl_frame, font=ctk.CTkFont(size=16)); self.downloader_label.pack(pady=10, padx=15, anchor="w")
        self.downloader_seg = ctk.CTkSegmentedButton(dl_frame, variable=self.downloader_var, height=40, font=ctk.CTkFont(size=14))
        self.downloader_seg.pack(pady=(5,15), padx=15, anchor="w")
        return frame

    def toggle_details_bar(self):
        if self.show_details_var.get(): self.status_frame.grid(row=1, column=0, sticky="ew")
        else: self.status_frame.grid_remove()

    def paste_from_clipboard(self):
        try:
            self.url_entry.delete(0, 'end'); self.url_entry.insert(0, self.clipboard_get())
        except tk.TclError: self.update_status(self.lang.get("clipboard_empty"))

    def select_folder(self):
        directory = filedialog.askdirectory(title=self.lang.get("select_folder_button"))
        if directory:
            self.download_path = directory
            if self.is_running: self.path_label.configure(text=self.download_path)
    
    def load_supported_sites_in_thread(self, collapsible_frame):
        for widget in collapsible_frame.content_container.winfo_children(): widget.destroy()
        loading_label = ctk.CTkLabel(collapsible_frame.content_container, text=self.lang.get("loading_sites"))
        loading_label.pack(pady=20)
        # Show container immediately to adjust layout while loading
        try:
            collapsible_frame._expand()
        except Exception:
            pass
        threading.Thread(target=self._fetch_sites_worker, args=(collapsible_frame, loading_label), daemon=True).start()

    def _fetch_sites_worker(self, collapsible_frame, loading_label):
        try:
            sites = self.ytdlp_manager.get_extractors()
            if not sites:
                 raise Exception("yt-dlp.exe not found or failed to execute.")
            self.after(0, self._populate_sites_frame, collapsible_frame, loading_label, sites)
        except Exception as e:
            self.logger.error(f"Site list fetch error: {e}")
            self.after(0, self._handle_fetch_error, collapsible_frame, loading_label)

    def _populate_sites_frame(self, collapsible_frame, loading_label, sites):
        if not self.is_running: return
        loading_label.destroy(); collapsible_frame.populate(sites)

    def _handle_fetch_error(self, collapsible_frame, loading_label):
        if not self.is_running: return
        loading_label.configure(text=self.lang.get("fetch_error_label"), text_color=("#d94848", "#e85151"))

    def start_download_thread(self):
        if self.download_thread and self.download_thread.is_alive():
            self.cancel_download(); return
        url = self.url_entry.get()
        if not url:
            messagebox.showerror(self.lang.get("error_title"), self.lang.get("link_error")); return
        self.logger.info(f"Start download | mode={self.download_mode_var.get()} | quick={self.quick_override} | url={url}")
        self.download_cancelled.clear()
        self.last_error_line = ""
        self.download_thread = threading.Thread(target=self.download_video_worker, args=(url,), daemon=True)
        self.download_thread.start()

    def quick_download(self, kind: str):
        self.quick_override = kind; self.start_download_thread()

    def cancel_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.download_cancelled.set()
            if self.download_process and self.download_process.poll() is None:
                self.download_process.terminate()
                self.logger.info("Download process terminated.")

    def _process_download_output(self, line, stream_type):
        if not self.is_running: return
        line = line.strip()
        if not line: return
        if stream_type == 'stderr':
            self.logger.error(f"[yt-dlp-stderr] {line}")
            self.last_error_line = line
            return
        # Track output file path from yt-dlp logs
        m_dest = re.search(r"\[download\] Destination: (.+)", line)
        if m_dest:
            self.current_output_file = m_dest.group(1).strip().strip('"')
        m_merge = re.search(r"\[Merger\] Merging formats into \"(.+)\"", line)
        if m_merge:
            self.current_output_file = m_merge.group(1).strip().strip('"')
        match = re.search(r"\[download\]\s+(?P<percent>[\d\.]+)%\s+of\s+\~?\s*(?P<size>[\d\.]+\w+)(?:\s+at\s+(?P<speed>[\d\.]+\w+/s))?(?:\s+ETA\s+(?P<eta>[\d\:]+))?", line)
        if match:
            data = match.groupdict()
            pct = float(data['percent'])
            status_text = self.lang.get("download_status_progress", percentage=round(pct, 1), size=data.get('size',''), speed=data.get('speed',''))
            if self.download_widget: self.after(0, self.download_widget.update_progress, pct, status_text)
        elif "[ExtractAudio]" in line or "[Merger]" in line or "[ffmpeg]" in line:
            if self.download_widget: self.after(0, self.download_widget.update_progress, 100, self.lang.get('download_processing'))
        else:
            self.logger.info(f"[yt-dlp-stdout] {line}")
            self.update_status(line)

    def _build_ydl_args(self, url):
        output_template = os.path.join(self.download_path, '%(title)s.%(ext)s')
        args = ['--no-playlist', '--color', 'never', '--retries', '10', '--fragment-retries', '10', '-o', output_template]
        if ffmpeg_available(): args.extend(['--ffmpeg-location', get_ffmpeg_path()])
        net_map = {"Auto": None, self.lang.get("network_ipv4"): "0.0.0.0", self.lang.get("network_ipv6"): "::"}
        source_addr = net_map.get(self.network_mode_var.get())
        if source_addr: args.extend(['--source-address', source_addr])
        dl_cur = str(self.downloader_var.get())
        if (dl_cur == self.lang.get("downloader_aria2c") or dl_cur.lower() == "aria2c") and shutil.which('aria2c'):
             args.extend(['--downloader', 'aria2c', '--downloader-args', 'aria2c:"-x16 -s16 -k1M"'])
        mode_map = { self.lang.get(k): v for k, v in {"mode_auto": "video_best", "mode_video": "video_best", "mode_video_only": "video_only", "mode_audio": "audio_only"}.items() }
        mode_key = mode_map.get(self.download_mode_var.get(), "video_best")
        quick = self.quick_override
        format_selector = ""
        if mode_key in ["video_best", "video_only"]:
            audio = "+bestaudio" if mode_key == "video_best" else ""
            fallback = f"/best{audio}"
            if quick == "best": format_selector = f"bestvideo{audio}{fallback}"
            elif quick == "compat": format_selector = f"bestvideo[ext=mp4][vcodec^=avc1]{audio}/best[ext=mp4]{audio}"
            else:
                q = self.video_quality_var.get()
                h = {"8k":"4320","4k":"2160","1440p":"1440","1080p":"1080","720p":"720","480p":"480","360p":"360"}.get(q)
                h_filter = f"[height<={h}]" if h else ""
                c = self.video_codec_var.get()
                c_id = {self.lang.get("codec_h264"):"avc", "vp9":"vp9", self.lang.get("codec_av1"):"av01"}.get(c)
                c_filter = f"[vcodec^={c_id}]" if c_id else ""
                format_selector = f"bestvideo{h_filter}{c_filter}{audio}{fallback}"
            container = self.container_var.get()
            if ffmpeg_available() and container != "auto": args.extend(['--merge-output-format', container])
        elif mode_key == "audio_only":
            audio_format = self.audio_format_var.get()
            if ffmpeg_available() and audio_format != "auto":
                format_selector = 'bestaudio/best'
                args.extend(['-x', '--audio-format', audio_format, '--audio-quality', self.bitrate_map.get(self.audio_bitrate_var.get(), "0")])
            else: format_selector = 'bestaudio[ext=m4a]/bestaudio'
        if format_selector: args.extend(['-f', format_selector])
        args.append(url)
        return args

    def download_video_worker(self, url):
        self.after(0, self.set_ui_to_download_mode)
        try:
            info = self.ytdlp_manager.get_info(url)
            self.after(0, self.download_widget.set_title, info.get('title', '...'))
            args = self._build_ydl_args(url)
            self.logger.debug(f"Running yt-dlp with args: {args}")
            self.download_process = self.ytdlp_manager._create_process(args)
            for line in iter(self.download_process.stdout.readline, ''):
                if self.download_cancelled.is_set(): break
                self._process_download_output(line, 'stdout')
            self.download_process.wait()
            stderr_output = self.download_process.stderr.read()
            if stderr_output: self._process_download_output(stderr_output, 'stderr')
            if self.download_cancelled.is_set():
                self.after(0, lambda: self.download_widget and self.download_widget.set_cancelled())
                self.after(0, lambda: self.download_widget and hasattr(self.download_widget, 'icon_label') and self.download_widget.icon_label.configure(text="⏹"))
                self.after(1500, self.set_ui_to_idle_mode)
                return
            if self.download_process.returncode == 0:
                self.after(0, lambda: self.download_widget and self.download_widget.set_complete())
                self.after(0, lambda: self.download_widget and hasattr(self.download_widget, 'icon_label') and self.download_widget.icon_label.configure(text="✓"))
                self.after(1500, self.set_ui_to_idle_mode)
            else: raise Exception(self.last_error_line or "Unknown download error")
        except FileNotFoundError:
            self.logger.error("yt-dlp.exe not found.")
            messagebox.showerror(self.lang.get("error_title"), self.lang.get("update_status_not_found"))
            self.after(0, self.set_ui_to_idle_mode)
        except Exception as e:
            if self.is_running:
                error_msg = str(e).split('ERROR: ')[-1].strip()
                self.logger.error(f"Download failed: {error_msg}")
                self.after(0, lambda: self.download_widget and self.download_widget.set_error(error_msg[:100]))
                self.after(0, lambda: self.download_widget and hasattr(self.download_widget, 'icon_label') and self.download_widget.icon_label.configure(text="✕"))
                self.after(4000, self.set_ui_to_idle_mode)
        finally:
            self.quick_override = None; self.download_process = None
            if self.download_cancelled.is_set(): self.after(0, self.set_ui_to_idle_mode)

    def set_ui_to_download_mode(self):
        self.download_button.configure(text=self.lang.get("cancel_button"))
        if self.download_widget: self.download_widget.destroy()
        # Create overlay on Home tab (auto-hidden on other tabs)
        try:
            parent = self.home_tab
        except Exception:
            parent = self
        if not getattr(self, 'queue_overlay', None) or not self.queue_overlay.winfo_exists():
            self.queue_overlay = ctk.CTkFrame(parent, fg_color="transparent")
            self.queue_overlay.place(relx=0.98, rely=0.03, anchor="ne")
        self.download_widget = DownloadQueueItem(self.queue_overlay, lang_manager=self.lang)
        self.download_widget.grid(row=0, column=0, sticky="ew")
        if self.queue_add_button:
            self.queue_add_button.grid()
        self._render_queue_controls()

    def set_ui_to_idle_mode(self):
        self.download_button.configure(text=self.lang.get("download_button"))
        self.update_status(self.lang.get("ready_status"))
        if self.download_widget: self.download_widget.destroy(); self.download_widget = None
        if self.queue_add_button: self.queue_add_button.grid_remove()
        self.download_thread = None
        # Start next item from queue if present
        if hasattr(self, 'pending_queue') and self.pending_queue:
            next_url = self.pending_queue.pop(0)
            try:
                self.url_entry.delete(0, 'end'); self.url_entry.insert(0, next_url)
            except Exception:
                pass
            self.start_download_thread()
        else:
            # Clear overlay controls
            if getattr(self, 'queue_overlay', None) and self.queue_overlay.winfo_exists():
                for child in self.queue_overlay.winfo_children():
                    child.destroy()

    def update_status(self, text):
        if self.is_running and self.show_details_var.get():
            cleaned = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text).strip()
            self.status_label.configure(text=cleaned)

    def add_to_queue(self):
        try:
            url = self.url_entry.get().strip()
        except Exception:
            url = ""
        if not url:
            return
        if not hasattr(self, 'pending_queue'):
            self.pending_queue = []
        self.pending_queue.append(url)
        try:
            self.url_entry.delete(0, 'end')
        except Exception:
            pass
        self._render_queue_controls()

    def _render_queue_controls(self):
        if not getattr(self, 'queue_overlay', None) or not self.queue_overlay.winfo_exists():
            return
        # Remove rows below main widget
        for child in list(self.queue_overlay.winfo_children()):
            gi = child.grid_info() if hasattr(child, 'grid_info') else {}
            if gi and gi.get('row', 0) >= 1:
                child.destroy()
        max_show = 2
        for idx, q in enumerate(self.pending_queue[:max_show], start=1):
            lbl = ctk.CTkLabel(self.queue_overlay, text=f"{idx}. {q[:50]}" + ("..." if len(q)>50 else ""), anchor="w")
            lbl.grid(row=idx, column=0, sticky="ew", padx=4, pady=2)
        if len(self.pending_queue) > max_show:
            more_btn = ctk.CTkButton(self.queue_overlay, text="More", height=28, command=self.open_downloads_window)
            more_btn.grid(row=max_show+1, column=0, sticky="e", padx=4, pady=(4,0))
        # History toggle button (down arrow)
        hist_btn = ctk.CTkButton(self.queue_overlay, width=32, height=28, text="↓", command=self.open_downloads_window)
        hist_btn.grid(row=0, column=1, padx=(6,0), pady=(6,0))

    def open_downloads_window(self):
        win = ctk.CTkToplevel(self)
        try:
            win.title("Downloads")
        except Exception:
            pass
        win.geometry("600x400")
        win.grid_columnconfigure(0, weight=1); win.grid_rowconfigure(0, weight=1)
        frame = ctk.CTkFrame(win)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text="History", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10,6))
        row = 1
        items = list(getattr(self, 'download_history', []))
        if not items:
            ctk.CTkLabel(frame, text="No downloads yet").grid(row=row, column=0, padx=10, pady=10, sticky="w")
            return
        for item in reversed(items[-200:]):
            status_color = ("#1f9340", "#32a852") if item.get('status') == 'success' else ("#d94848", "#e85151")
            ctk.CTkLabel(frame, text=("✓" if item.get('status')=='success' else "✕"), text_color=status_color).grid(row=row, column=0, padx=10, pady=4)
            ctk.CTkLabel(frame, text=item.get('title','...'), anchor="w").grid(row=row, column=1, sticky="ew", pady=4)
            p = item.get('path') or ''
            btn = ctk.CTkButton(frame, height=28, text="Open folder",
                                 command=(lambda path=p: os.startfile(os.path.dirname(path)) if path and os.path.exists(path) else None))
            btn.grid(row=row, column=2, padx=10, pady=4)
            row += 1

    def update_ytdlp_in_thread(self):
        self.update_button.configure(state="disabled")
        self.update_label.configure(text=self.lang.get("update_status_checking"))
        threading.Thread(target=self._update_ytdlp_worker, daemon=True).start()

    def _update_ytdlp_worker(self):
        final_status = "update_status_error"
        try:
            update_generator = self.ytdlp_manager.check_and_update(force=True)
            for status in update_generator:
                self.after(0, self.update_label.configure, {"text": self.lang.get(f"update_status_{status}")})
                final_status = f"update_status_{status}"
        except Exception as e:
            self.logger.error(f"Exception during yt-dlp update: {e}")
            final_status = "update_status_error"
        self.after(0, self._update_ui_after_update, self.lang.get(final_status))

    def _update_ui_after_update(self, message):
        messagebox.showinfo(self.lang.get("update_title"), message)
        self.update_label.configure(text=self.lang.get("update_label"))
        self.update_button.configure(state="normal")
    
    def open_logs_folder(self):
        try: os.startfile(get_logs_dir())
        except Exception as e: messagebox.showerror(self.lang.get("error_title"), f"{self.lang.get('logs_error_open')}\n{e}")

    def confirm_clear_logs(self):
        confirmed = messagebox.askyesno(self.lang.get("confirm_title"), self.lang.get("confirm_clear_logs_text"))
        if confirmed:
            try:
                clear_all_logs()
                self.logger.info("Logs have been cleared by the user.")
                messagebox.showinfo(self.lang.get("success_title"), self.lang.get("logs_cleared_success"))
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title"), f"{self.lang.get('logs_cleared_error')}\n{e}")
                self.logger.error(f"Failed to clear logs: {e}")

if __name__ == "__main__":
    settings = load_or_create_config()
    theme_manager = ThemeManager()
    theme_data = theme_manager.get_theme_data(settings["theme"])
    if theme_data:
        ctk.set_appearance_mode(theme_data["appearance"])
        if theme_data["type"] == "custom": ctk.set_default_color_theme(theme_data["path"])
        else: ctk.set_default_color_theme(theme_data["name"])
    app = App(initial_settings=settings)
    app.mainloop()
