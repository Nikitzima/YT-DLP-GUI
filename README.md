YT-DLP GUI — графический интерфейс для yt-dlp (Windows)

Удобное настольное приложение для загрузки видео и аудио с поддержкой очереди, профилей и тем. В комплекте — `yt-dlp` и `ffmpeg` для работы «из коробки».

— English blurb —
Simple, polished Windows GUI for `yt-dlp`. Ships with `yt-dlp` and `ffmpeg` so it works out of the box.

## Возможности
- Очередь загрузок и наглядный прогресс.
- Профили и сохранение настроек в `config.json`.
- Встроенные `yt-dlp.exe` и `ffmpeg.exe` (локально рядом с `.exe`).
- Гибкие форматы: видео/аудио, контейнеры, битрейт.
- Тёмная/светлая темы, поддержка CustomTkinter.

## Скачать
- Рекомендуемый способ: раздел Releases — последняя версия: https://github.com/Nikitzima/YT-DLP-GUI/releases/latest
- Альтернатива: архив в репозитории `release/` (portable-сборка с `.exe`).

Запуск: распакуйте архив в удобную папку (не в `Program Files`), запустите `YT-DLP GUI.exe`.

Требования: Windows 10/11 x64. Установка Python не требуется.

## Скриншот/иконка
Логотипы и иконка лежат в репозитории (`logo_bg.png`, `icon.ico`).

## Сборка из исходников
1) Установите зависимости:
```
python -m venv .venv
.venv\\Scripts\\pip install -r requirements.txt
```
2) Соберите exe (используется PyInstaller spec):
```
pyinstaller "YT-DLP GUI.spec"
```
Готовый `.exe` появится в `dist/`.

Полезно: в `bin/` находится `yt-dlp.exe`, который пакуется рядом с приложением. `ffmpeg.exe` также кладётся рядом с `.exe` (см. `main_app.py -> resource_path`).

## Структура
- `main_app.py` — основное приложение (CustomTkinter + логика).
- `theme_manager_fixed.py`, `language_manager.py`, `yt_dlp_manager.py` — модули тем, локализации и загрузчика.
- `bin/yt-dlp.exe` — бинарник yt-dlp для портативной поставки.
- `ffmpeg.exe` — локальный FFmpeg (опционально, может лежать рядом с `.exe`).
- `release/` — готовые portable-архивы для скачивания.

## Лицензия
Если планируется публичное распространение — добавьте LICENSE. По умолчанию «все права защищены».

