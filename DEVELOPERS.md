YT‑DLP GUI — Developer Notes

Overview

- UI framework: CustomTkinter (CTk)
- Entry point: main_app.py
- Theme system: theme_manager_fixed.py generates JSON for custom themes on first run
- i18n: language_manager.py (simple map of keys per language)
- yt-dlp lifecycle: yt_dlp_manager.py (downloads/updates/executes yt-dlp.exe)

Key Modules

- main_app.py: Application window, tabs, widgets, and all event wiring.
  - CollapsibleFrame: expands the supported sites list and adjusts the main block padding to avoid overlap (see _check_and_adjust_layout).
  - _rebuild_ui(go_home=False): safe rebuild for theme/language switch. In theme switch we call it with go_home=True to avoid tab glitches.
  - resource_path(): PyInstaller-friendly resource resolver for icon/logo.

- theme_manager_fixed.py: Holds theme definitions and writes custom theme JSON files to ./themes on startup.
  - Add new theme in self.themes; JSON is generated automatically.

- language_manager.py: Keeps translations in-memory; get(key, **kwargs) formats strings for current language.

- yt_dlp_manager.py: Handles downloading/updating/launching yt-dlp.exe using urllib + subprocess (no heavy deps).
  - check_and_update(force=True) is a generator yielding: checking | downloading | success | latest | error

Packaging (Windows, single EXE)

Install deps in a clean venv:

  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install pyinstaller customtkinter pillow

Build one-file EXE (no console):

  pyinstaller -F -w -i icon.ico ^
    --name "YT-DLP GUI" ^
    --add-data "logo_bg.png;." ^
    --add-data "icon.ico;." ^
    main_app.py

Optional: if you want to ship ffmpeg.exe alongside the EXE (not required — the app also respects system PATH):

  pyinstaller -F -w -i icon.ico ^
    --name "YT-DLP GUI" ^
    --add-data "logo_bg.png;." ^
    --add-data "icon.ico;." ^
    --add-binary "ffmpeg.exe;." ^
    main_app.py

After build, distribute the single EXE from the dist/ folder.

Runtime Notes

- On first run, yt_dlp_manager downloads yt-dlp.exe into ./bin.
- Logs are stored under ./logs with rotation (see main_app.setup_file_logger).
- To clear logs safely, use the UI button (“Обслуживание”).

