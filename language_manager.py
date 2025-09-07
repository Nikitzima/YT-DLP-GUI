# Файл: language_manager.py

class LanguageManager:
    """
    Управляет языками и переводами для приложения.
    Вся текстовая информация хранится здесь для легкого доступа и модификации.
    """
    def __init__(self, default_language="en"):
        self.language_map = {
            "English": "en", "Русский": "ru", "中文": "zh", "Español": "es",
            "Deutsch": "de", "Français": "fr", "日本語": "ja"
        }
        self.current_language = default_language
        app_name = "YT-DLP GUI"
        app_version = "5.3.1" 

        self.translations = {
            # --- English ---
            "en": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "Ready...",
                "home_tab": "Home", "settings_tab": "Settings", 
                "maintenance_tab": "Maintenance", "info_tab": "Info",
                "paste_placeholder": "Paste link here...", "paste_button": "Paste", 
                "select_folder_button": "Select Folder", "download_button": "Download", 
                "cancel_button": "Cancel",
                "mode_auto": "Auto", "mode_video": "Video", "mode_audio": "Audio", 
                "mode_video_only": "Video (no sound)",
                "quick_best_button": "Best Quality", "quick_compat_button": "Most Compatible",
                "show_sites_button": "Show Supported Sites", "hide_sites_button": "Hide Supported Sites",
                "search_sites_placeholder": "Search through {count} sites...",
                "loading_sites": "Loading site list...", "error_title": "Error", 
                "fetch_error_label": "Loading Error.", "clipboard_empty": "Clipboard is empty.",
                "settings_video": "Video", "settings_audio": "Audio", 
                "settings_appearance": "Appearance", "settings_advanced": "Advanced",
                "video_settings_title": "Video Settings", "video_quality": "Video Quality", 
                "quality_best": "Best",
                "video_codec": "Preferred Video Codec", "codec_h264": "h264 (compatible)", 
                "codec_av1": "av1 (modern)", "file_container": "File Container (for video)",
                "audio_settings_title": "Audio Settings", "audio_format": "Audio Format", 
                "audio_bitrate": "Audio Bitrate",
                "appearance_settings_title": "Appearance Settings", "theme_label": "Theme", 
                "language_label": "Language",
                "advanced_settings_title": "Advanced", "show_details_switch": "Show download details",
                "network_mode": "Network Mode", "network_auto": "Auto", "network_ipv4": "Force IPv4", "network_ipv6": "Force IPv6",
                "downloader_engine": "Downloader Engine", "downloader_builtin": "Built-in", "downloader_aria2c": "aria2c",
                "link_error": "Please paste a link.",
                "download_info_getting": "Getting information...", 
                "download_status_progress": "Downloading: {percentage}% ({size}) @ {speed}",
                "download_complete": "Completed", "download_error": "Error", 
                "download_cancelled": "Cancelled", "download_processing": "Processing...",
                "maintenance_title": "Application Maintenance",
                "update_button": "Update yt-dlp",
                "update_label": "Keep the core download engine up-to-date to prevent issues with YouTube and other sites.",
                "update_title": "Update", "update_status_checking": "Checking for updates...",
                "update_status_success": "yt-dlp has been successfully updated!",
                "update_status_latest": "You already have the latest version of yt-dlp.",
                "update_status_error": "An error occurred during the update.",
                "logs_button": "Open Logs Folder",
                "logs_label": "If you encounter a problem, the log files in this folder can help with troubleshooting.",
                "logs_error_open": "Could not open logs folder.",
                "clear_logs_button": "Clear Logs",
                "clear_logs_label": "Delete all log files to free space or reset logs.",
                "confirm_title": "Confirm",
                "confirm_clear_logs_text": "Delete all application log files? This cannot be undone.",
                "success_title": "Success",
                "logs_cleared_success": "All log files have been deleted.",
                "logs_cleared_error": "Could not delete log files.",
                "info_nav_what_is_this": "What is this?", "info_nav_community": "Community & Support",
                "info_nav_privacy": "Privacy", "info_nav_ethics": "Terms & Ethics",
                "info_nav_licenses": "Thanks & Licenses",
                "info_content_what_is_this": (
                    "## What is YT-DLP GUI?\n\n"
                    "This app is a user-friendly graphical interface for the powerful command-line tool **'yt-dlp'**. It allows you to easily download video and audio from thousands of websites without needing to use the terminal. Just paste a link, choose your settings, and click 'Download'!\n\n"
                    "### How It Works\n"
                    "1.  **Paste a Link**: You provide a link to the content you want to download.\n"
                    "2.  **Choose Settings**: In the 'Settings' tab, you can pre-configure your desired quality, format, and codecs for video and audio.\n"
                    "3.  **Download**: The app takes your link and settings and translates them into a command that 'yt-dlp' understands. The 'yt-dlp' engine then handles the actual download process, saving the file to your chosen folder.\n\n"
                    "### For the Curious Minds (The Geek Stuff)\n"
                    "This is a pure Python application. The user interface is built with the **'CustomTkinter'** library, which allows for modern styling and theming. The core downloading functionality is powered by the legendary **'yt-dlp'** library. My app essentially acts as a 'translator', converting your clicks into text commands for the real hero, 'yt-dlp'."
                ),
                "info_content_community": (
                    "## An Open Source Project\n\n"
                    "I believe in the power of open and free software. This application is open source, which means anyone can view, audit, and contribute to its source code. This transparency ensures the app is safe and respects your privacy.\n\n"
                    "### GitHub 🐙\n"
                    "The heart of our community is on GitHub. Here you can:\n"
                    "- **View the source code** to see exactly how the app works.\n"
                    "- **Report bugs** or suggest new features by creating an 'Issue'.\n"
                    "- **Contribute** to the project by proposing code changes.\n"
                    "*[GitHub repository link: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "For the latest news, updates, and announcements, follow my Telegram channel.\n"
                    "*[Telegram channel link: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## Your Privacy is Paramount\n\n"
                    "This application is designed with your privacy as a top priority. I adhere to a strict **zero-log policy**.\n\n"
                    "- **No Data Collection**: The app does not collect, store, or transmit any personal information. I don't know who you are or what you download.\n"
                    "- **Local Processing**: All download operations occur directly on your computer. The app communicates with the target website to fetch content, but no data ever passes through my servers.\n"
                    "- **No Tracking**: There are no analytics or tracking mechanisms built into the application. Your usage is completely private."
                ),
                "info_content_ethics": (
                    "## Terms of Use & Ethical Considerations\n\n"
                    "Please use this tool responsibly. While it is a powerful utility, it's important to respect copyright and the terms of service of the websites you download from.\n\n"
                    "- **User Responsibility**: You, the end user, are solely responsible for your actions and for any content you download. The developer of this application is not liable for how you use this tool.\n"
                    "- **Support Creators**: Many creators rely on ad revenue and views on original platforms. Please consider supporting them by watching their content on their respective sites and using this tool primarily for personal backups or offline viewing where permitted.\n"
                    "- **Fair Use**: Always respect the intellectual property of others. Do not redistribute copyrighted material without permission."
                ),
                "info_content_licenses": (
                    "## Motivation & Acknowledgements\n\n"
                    "This app was created to provide a safe, transparent, and ad-free alternative to many online downloaders that are often filled with intrusive ads and trackers. A good tool should serve the user, not exploit them.\n\n"
                    "### Key Technologies & Licenses 📜\n"
                    "This project would not be possible without the incredible work of the open-source community. Key components include:\n"
                    "- **yt-dlp**: The core download engine. (The Unlicense)\n"
                    "- **CustomTkinter**: For the beautiful graphical interface. (MIT License)\n"
                    "- **Python**: The programming language that ties it all together. (Python Software Foundation License)\n\n"
                    "The code for this application itself is also open source, distributed under the **MIT License**. You can view the full list of dependencies on GitHub.\n\n"
                    "### Gratitude & Support\n"
                    "A huge thank you to everyone who contributes to open-source software. If this little tool has been helpful to you, consider supporting its development. Every little bit helps!\n"
                    "*[Donation link: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- Русский ---
            "ru": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "Готов к работе...",
                "home_tab": "Главная", "settings_tab": "Настройки", 
                "maintenance_tab": "Обслуживание", "info_tab": "Инфо",
                "paste_placeholder": "Вставьте ссылку сюда...", "paste_button": "Вставить", 
                "select_folder_button": "Выбрать папку", "download_button": "Скачать", 
                "cancel_button": "Отмена",
                "mode_auto": "Авто", "mode_video": "Видео", "mode_audio": "Аудио", 
                "mode_video_only": "Видео (без звука)",
                "quick_best_button": "Лучшее качество", "quick_compat_button": "Макс. совместимость",
                "show_sites_button": "Показать поддерживаемые сайты", "hide_sites_button": "Скрыть поддерживаемые сайты",
                "search_sites_placeholder": "Поиск по {count} сайтам...",
                "loading_sites": "Загрузка списка сайтов...", "error_title": "Ошибка", 
                "fetch_error_label": "Ошибка загрузки.", "clipboard_empty": "Буфер обмена пуст.",
                "settings_video": "Видео", "settings_audio": "Аудио", 
                "settings_appearance": "Оформление", "settings_advanced": "Расширенные",
                "video_settings_title": "Настройки Видео", "video_quality": "Качество видео", 
                "quality_best": "Лучшее",
                "video_codec": "Предпочтительный видеокодек", "codec_h264": "h264 (совместимый)", 
                "codec_av1": "av1 (современный)", "file_container": "Контейнер файла (для видео)",
                "audio_settings_title": "Настройки Аудио", "audio_format": "Формат аудио", 
                "audio_bitrate": "Битрейт аудио",
                "appearance_settings_title": "Настройки Оформления", "theme_label": "Тема", 
                "language_label": "Язык",
                "advanced_settings_title": "Расширенные", "show_details_switch": "Показывать подробности скачивания",
                "network_mode": "Сетевой режим", "network_auto": "Авто", "network_ipv4": "Только IPv4", "network_ipv6": "Только IPv6",
                "downloader_engine": "Движок загрузки", "downloader_builtin": "Встроенный", "downloader_aria2c": "aria2c",
                "link_error": "Вставьте ссылку.",
                "download_info_getting": "Получение информации...", 
                "download_status_progress": "Скачиваю: {percentage}% ({size}) @ {speed}",
                "download_complete": "Завершено", "download_error": "Ошибка", 
                "download_cancelled": "Отменено", "download_processing": "Обработка...",
                "maintenance_title": "Обслуживание приложения",
                "update_button": "Обновить yt-dlp",
                "update_label": "Поддерживайте ядро загрузки в актуальном состоянии, чтобы избежать проблем с YouTube и другими сайтами.",
                "update_title": "Обновление", "update_status_checking": "Проверка обновлений...",
                "update_status_success": "yt-dlp был успешно обновлен!",
                "update_status_latest": "У вас уже установлена последняя версия yt-dlp.",
                "update_status_error": "Произошла ошибка во время обновления.",
                "logs_button": "Открыть папку с логами",
                "logs_label": "Если вы столкнулись с проблемой, лог-файлы в этой папке могут помочь в ее решении.",
                "logs_error_open": "Не удалось открыть папку с логами.",
                "clear_logs_button": "Очистить логи",
                "clear_logs_label": "Удалить все файлы логов, чтобы освободить место или сбросить журнал.",
                "confirm_title": "Подтверждение",
                "confirm_clear_logs_text": "Удалить все файлы логов приложения? Это действие нельзя отменить.",
                "success_title": "Готово",
                "logs_cleared_success": "Все файлы логов удалены.",
                "logs_cleared_error": "Не удалось удалить файлы логов.",
                "info_nav_what_is_this": "Что это такое?", "info_nav_community": "Сообщество и поддержка",
                "info_nav_privacy": "Конфиденциальность", "info_nav_ethics": "Условия и этика",
                "info_nav_licenses": "Благодарности и лицензии",
                "info_content_what_is_this": (
                    "## Что такое YT-DLP GUI?\n\n"
                    "Это приложение — удобный графический интерфейс для мощного инструмента командной строки **'yt-dlp'**. Оно позволяет легко скачивать видео и аудио с тысяч веб-сайтов без необходимости использовать терминал. Просто вставьте ссылку, выберите настройки и нажмите 'Скачать'!\n\n"
                    "### Как это работает\n"
                    "1.  **Вставьте ссылку**: Вы предоставляете ссылку на контент, который хотите скачать.\n"
                    "2.  **Выберите настройки**: Во вкладке 'Настройки' вы можете предварительно настроить желаемое качество, формат и кодеки для видео и аудио.\n"
                    "3.  **Скачайте**: Приложение берет вашу ссылку и настройки и преобразует их в команду, понятную для 'yt-dlp'. Затем движок 'yt-dlp' выполняет сам процесс скачивания, сохраняя файл в выбранную вами папку.\n\n"
                    "### Для любознательных (технические детали)\n"
                    "Это приложение полностью написано на Python. Пользовательский интерфейс создан с помощью библиотеки **'CustomTkinter'**, которая обеспечивает современный дизайн и поддержку тем. Основная функция скачивания реализована благодаря легендарной библиотеке **'yt-dlp'**. Моя программа, по сути, действует как 'переводчик', превращая ваши клики в текстовые команды для настоящего героя — 'yt-dlp'."
                ),
                "info_content_community": (
                    "## Проект с открытым исходным кодом\n\n"
                    "Я верю в силу открытого и свободного программного обеспечения. Это приложение имеет открытый исходный код, что означает, что любой может просматривать, проверять и вносить свой вклад в его код. Такая прозрачность гарантирует, что приложение безопасно и уважает вашу конфиденциальность.\n\n"
                    "### GitHub 🐙\n"
                    "Сердце нашего сообщества находится на GitHub. Здесь вы можете:\n"
                    "- **Посмотреть исходный код**, чтобы точно узнать, как работает приложение.\n"
                    "- **Сообщить об ошибках** или предложить новые функции, создав 'Issue'.\n"
                    "- **Внести свой вклад** в проект, предложив изменения в коде.\n"
                    "*[Ссылка на репозиторий GitHub: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "Чтобы быть в курсе последних новостей, обновлений и анонсов, подписывайтесь на мой телеграм-канал.\n"
                    "*[Ссылка на телеграм-канал: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## Ваша конфиденциальность — главный приоритет\n\n"
                    "Это приложение разработано с учетом вашей конфиденциальности как главного приоритета. Я придерживаюсь строгой **политики отсутствия логов**.\n\n"
                    "- **Никакого сбора данных**: Приложение не собирает, не хранит и не передает никакой личной информации. Я не знаю, кто вы и что вы скачиваете.\n"
                    "- **Локальная обработка**: Все операции по скачиванию происходят непосредственно на вашем компьютере. Приложение связывается с целевым веб-сайтом для получения контента, но никакие данные никогда не проходят через мои серверы.\n"
                    "- **Никакого отслеживания**: В приложение не встроены механизмы аналитики или отслеживания. Ваше использование полностью конфиденциально."
                ),
                "info_content_ethics": (
                    "## Условия использования и этические соображения\n\n"
                    "Пожалуйста, используйте этот инструмент ответственно. Хотя это мощная утилита, важно уважать авторские права и условия использования веб-сайтов, с которых вы скачиваете контент.\n\n"
                    "- **Ответственность пользователя**: Вы, конечный пользователь, несете полную ответственность за свои действия и за любой скачиваемый контент. Разработчик этого приложения не несет ответственности за то, как вы используете этот инструмент.\n"
                    "- **Поддерживайте авторов**: Многие авторы контента зависят от доходов от рекламы и просмотров на оригинальных платформах. Пожалуйста, поддерживайте их, просматривая их контент на соответствующих сайтах, и используйте этот инструмент в основном для личных резервных копий или офлайн-просмотра, где это разрешено.\n"
                    "- **Добросовестное использование**: Всегда уважайте интеллектуальную собственность других. Не распространяйте материалы, защищенные авторским правом, без разрешения."
                ),
                "info_content_licenses": (
                    "## Мотивация и благодарности\n\n"
                    "Это приложение было создано, чтобы предоставить безопасную, прозрачную и свободную от рекламы альтернативу многим онлайн-загрузчикам, которые часто наполнены навязчивой рекламой и трекерами. Хороший инструмент должен служить пользователю, а не эксплуатировать его.\n\n"
                    "### Ключевые технологии и лицензии 📜\n"
                    "Этот проект был бы невозможен без невероятной работы сообщества open-source. Ключевые компоненты включают:\n"
                    "- **yt-dlp**: Ядро для скачивания. (The Unlicense)\n"
                    "- **CustomTkinter**: Для красивого графического интерфейса. (MIT License)\n"
                    "- **Python**: Язык программирования, который все это связывает. (Python Software Foundation License)\n\n"
                    "Код самого этого приложения также является открытым и распространяется по **лицензии MIT**. Полный список зависимостей вы можете посмотреть на GitHub.\n\n"
                    "### Благодарности и поддержка\n"
                    "Огромное спасибо всем, кто вносит свой вклад в программное обеспечение с открытым исходным кодом. Если этот небольшой инструмент был вам полезен, вы можете поддержать его разработку. Любая помощь важна!\n"
                    "*[Ссылка для донатов: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- Chinese ---
            "zh": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "准备就绪...",
                "home_tab": "主页", "settings_tab": "设置", "maintenance_tab": "维护", "info_tab": "信息",
                "paste_placeholder": "在此处粘贴链接...", "paste_button": "粘贴", "select_folder_button": "选择文件夹",
                "download_button": "下载", "cancel_button": "取消",
                "mode_auto": "自动", "mode_video": "视频", "mode_audio": "音频", "mode_video_only": "仅视频 (无声)",
                "quick_best_button": "最佳质量", "quick_compat_button": "最佳兼容性",
                "show_sites_button": "显示支持的网站", "hide_sites_button": "隐藏支持的网站",
                "search_sites_placeholder": "搜索 {count} 个网站...",
                "loading_sites": "正在加载网站列表...", "error_title": "错误", 
                "fetch_error_label": "加载错误。", "clipboard_empty": "剪贴板为空。",
                "settings_video": "视频", "settings_audio": "音频", "settings_appearance": "外观", "settings_advanced": "高级",
                "video_settings_title": "视频设置", "video_quality": "视频质量", "quality_best": "最佳",
                "video_codec": "首选视频编解码器", "codec_h264": "h264 (兼容)", "codec_av1": "av1 (现代)",
                "file_container": "文件容器 (视频)",
                "audio_settings_title": "音频设置", "audio_format": "音频格式", "audio_bitrate": "音频比特率",
                "appearance_settings_title": "外观设置", "theme_label": "主题", "language_label": "语言",
                "advanced_settings_title": "高级设置", "show_details_switch": "显示下载详情",
                "network_mode": "网络模式", "network_auto": "自动", "network_ipv4": "强制IPv4", "network_ipv6": "强制IPv6",
                "downloader_engine": "下载引擎", "downloader_builtin": "内置", "downloader_aria2c": "aria2c",
                "link_error": "请粘贴链接。",
                "download_info_getting": "正在获取信息...", "download_status_progress": "下载中: {percentage}% ({size}) @ {speed}",
                "download_complete": "已完成", "download_error": "错误", "download_cancelled": "已取消", "download_processing": "处理中...",
                "maintenance_title": "应用程序维护",
                "update_button": "更新 yt-dlp",
                "update_label": "保持核心下载引擎为最新版本，以防止出现YouTube和其他网站的问题。",
                "update_title": "更新", "update_status_checking": "正在检查更新...",
                "update_status_success": "yt-dlp 已成功更新！",
                "update_status_latest": "您已拥有最新版本的 yt-dlp。",
                "update_status_error": "更新过程中发生错误。",
                "logs_button": "打开日志文件夹",
                "logs_label": "如果您遇到问题，此文件夹中的日志文件可以帮助进行故障排除。",
                "logs_error_open": "无法打开日志文件夹。",
                "clear_logs_button": "清除日志",
                "clear_logs_label": "删除所有日志文件以释放空间或重置日志。",
                "confirm_title": "确认",
                "confirm_clear_logs_text": "确定要删除所有应用日志文件吗？此操作无法恢复。",
                "success_title": "成功",
                "logs_cleared_success": "所有日志文件已删除。",
                "logs_cleared_error": "无法删除日志文件。",
                "info_nav_what_is_this": "这是什么？", "info_nav_community": "社区与支持",
                "info_nav_privacy": "隐私", "info_nav_ethics": "条款与道德",
                "info_nav_licenses": "致谢与许可",
                "info_content_what_is_this": (
                    "## YT-DLP GUI 是什么？\n\n"
                    "本应用是功能强大的命令行工具 **'yt-dlp'** 的一个用户友好型图形界面。它能让您轻松地从数千个网站下载视频和音频，而无需使用终端。只需粘贴链接，选择设置，然后点击“下载”即可！\n\n"
                    "### 工作原理\n"
                    "1.  **粘贴链接**：您提供想要下载的内容链接。\n"
                    "2.  **选择设置**：在“设置”选项卡中，您可以预先配置视频和音频所需的质量、格式和编解码器。\n"
                    "3.  **下载**：应用会接收您的链接和设置，并将其转换为 'yt-dlp' 能理解的命令。然后，'yt-dlp' 引擎会处理实际的下载过程，将文件保存到您选择的文件夹中。\n\n"
                    "### 为好奇者准备 (技术细节)\n"
                    "这是一个纯 Python 应用程序。用户界面是使用 **'CustomTkinter'** 库构建的，它支持现代化的样式和主题。核心下载功能由传奇的 **'yt-dlp'** 库提供支持。我的应用实质上充当了一个“翻译器”，将您的点击操作转换为真正的英雄 'yt-dlp' 的文本命令。"
                ),
                "info_content_community": (
                    "## 一个开源项目\n\n"
                    "我相信开放和免费软件的力量。本应用程序是开源的，这意味着任何人都可以查看、审计和贡献其源代码。这种透明度确保了应用的安全性并尊重您的隐私。\n\n"
                    "### GitHub 🐙\n"
                    "我们社区的核心在 GitHub 上。在这里您可以：\n"
                    "- **查看源代码**，确切了解应用的工作方式。\n"
                    "- **报告错误**或通过创建“Issue”提出新功能建议。\n"
                    "- 通过提出代码更改来**贡献**于项目。\n"
                    "*[GitHub 仓库链接: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "要获取最新消息、更新和公告，请关注我的 Telegram 频道。\n"
                    "*[Telegram 频道链接: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## 您的隐私至关重要\n\n"
                    "本应用程序的设计将您的隐私放在首位。我严格遵守**零日志政策**。\n\n"
                    "- **无数据收集**：本应用不收集、存储或传输任何个人信息。我不知道您是谁，也不知道您下载了什么。\n"
                    "- **本地处理**：所有下载操作都直接在您的计算机上进行。应用与目标网站通信以获取内容，但数据绝不会通过我的服务器。\n"
                    "- **无跟踪**：应用程序中没有内置任何分析或跟踪机制。您的使用是完全私密的。"
                ),
                "info_content_ethics": (
                    "## 使用条款与道德考量\n\n"
                    "请负责任地使用本工具。虽然它是一个功能强大的实用程序，但尊重版权和您下载来源网站的服务条款非常重要。\n\n"
                    "- **用户责任**：您，最终用户，对您的行为和您下载的任何内容负全部责任。本应用的开发者对您如何使用此工具不承担任何责任。\n"
                    "- **支持创作者**：许多创作者依赖于原始平台上的广告收入和观看次数。请考虑通过在他们各自的网站上观看他们的内容来支持他们，并主要在允许的情况下将此工具用于个人备份或离线观看。\n"
                    "- **合理使用**：始终尊重他人的知识产权。未经许可，请勿重新分发受版权保护的材料。"
                ),
                "info_content_licenses": (
                    "## 动机与致谢\n\n"
                    "创建此应用的目的是为了提供一个安全、透明且无广告的替代方案，以取代许多充斥着侵入性广告和跟踪器的在线下载器。一个好的工具应该为用户服务，而不是利用他们。\n\n"
                    "### 关键技术与许可证 📜\n"
                    "没有开源社区的卓越工作，这个项目是不可能实现的。关键组件包括：\n"
                    "- **yt-dlp**：核心下载引擎。(The Unlicense)\n"
                    "- **CustomTkinter**：用于美观的图形界面。(MIT 许可证)\n"
                    "- **Python**：将所有这些联系在一起的编程语言。(Python 软件基金会许可证)\n\n"
                    "本应用程序本身的代码也是开源的，根据 **MIT 许可证**分发。您可以在 GitHub 上查看完整的依赖项列表。\n\n"
                    "### 感激与支持\n"
                    "非常感谢所有为开源软件做出贡献的人。如果这个小工具对您有所帮助，请考虑支持其开发。每一份支持都很有帮助！\n"
                    "*[捐赠链接: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- Spanish ---
            "es": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "Listo...",
                "home_tab": "Inicio", "settings_tab": "Ajustes", "maintenance_tab": "Mantenimiento", "info_tab": "Info",
                "paste_placeholder": "Pega el enlace aquí...", "paste_button": "Pegar", "select_folder_button": "Seleccionar carpeta",
                "download_button": "Descargar", "cancel_button": "Cancelar",
                "mode_auto": "Auto", "mode_video": "Vídeo", "mode_audio": "Audio", "mode_video_only": "Vídeo (sin sonido)",
                "quick_best_button": "Mejor Calidad", "quick_compat_button": "Más Compatible",
                "show_sites_button": "Mostrar sitios compatibles", "hide_sites_button": "Ocultar sitios compatibles",
                "search_sites_placeholder": "Buscar en {count} sitios...",
                "loading_sites": "Cargando lista de sitios...", "error_title": "Error",
                "fetch_error_label": "Error de carga.", "clipboard_empty": "El portapapeles está vacío.",
                "settings_video": "Vídeo", "settings_audio": "Audio", "settings_appearance": "Apariencia", "settings_advanced": "Avanzado",
                "video_settings_title": "Ajustes de vídeo", "video_quality": "Calidad de vídeo", "quality_best": "La mejor",
                "video_codec": "Códec de vídeo preferido", "codec_h264": "h264 (compatible)", "codec_av1": "av1 (moderno)",
                "file_container": "Contenedor de archivo (para vídeo)",
                "audio_settings_title": "Ajustes de audio", "audio_format": "Formato de audio", "audio_bitrate": "Tasa de bits de audio",
                "appearance_settings_title": "Ajustes de apariencia", "theme_label": "Tema", "language_label": "Idioma",
                "advanced_settings_title": "Avanzado", "show_details_switch": "Mostrar detalles de la descarga",
                "network_mode": "Modo de Red", "network_auto": "Auto", "network_ipv4": "Forzar IPv4", "network_ipv6": "Forzar IPv6",
                "downloader_engine": "Motor de Descarga", "downloader_builtin": "Integrado", "downloader_aria2c": "aria2c",
                "link_error": "Por favor, pega un enlace.",
                "download_info_getting": "Obteniendo información...", "download_status_progress": "Descargando: {percentage}% ({size}) @ {speed}",
                "download_complete": "Completado", "download_error": "Error", "download_cancelled": "Cancelado", "download_processing": "Procesando...",
                "maintenance_title": "Mantenimiento de la Aplicación",
                "update_button": "Actualizar yt-dlp",
                "update_label": "Mantén actualizado el motor de descarga principal para evitar problemas con YouTube y otros sitios.",
                "update_title": "Actualizar", "update_status_checking": "Buscando actualizaciones...",
                "update_status_success": "¡yt-dlp se ha actualizado correctamente!",
                "update_status_latest": "Ya tienes la última versión de yt-dlp.",
                "update_status_error": "Ocurrió un error durante la actualización.",
                "logs_button": "Abrir Carpeta de Registros",
                "logs_label": "Si encuentras un problema, los archivos de registro en esta carpeta pueden ayudar a solucionarlo.",
                "logs_error_open": "No se pudo abrir la carpeta de registros.",
                "clear_logs_button": "Borrar registros",
                "clear_logs_label": "Eliminar todos los archivos de registro para liberar espacio o restablecer los registros.",
                "confirm_title": "Confirmación",
                "confirm_clear_logs_text": "¿Eliminar todos los archivos de registro de la aplicación? Esta acción no se puede deshacer.",
                "success_title": "Éxito",
                "logs_cleared_success": "Todos los archivos de registro han sido eliminados.",
                "logs_cleared_error": "No se pudieron eliminar los archivos de registro.",
                "info_nav_what_is_this": "¿Qué es esto?", "info_nav_community": "Comunidad y Soporte",
                "info_nav_privacy": "Privacidad", "info_nav_ethics": "Términos y Ética",
                "info_nav_licenses": "Agradecimientos y Licencias",
                "info_content_what_is_this": (
                    "## ¿Qué es YT-DLP GUI?\n\n"
                    "Esta aplicación es una interfaz gráfica fácil de usar para la potente herramienta de línea de comandos **'yt-dlp'**. Te permite descargar fácilmente vídeo y audio de miles de sitios web sin necesidad de usar la terminal. ¡Solo pega un enlace, elige tus ajustes y haz clic en 'Descargar'!\n\n"
                    "### Cómo funciona\n"
                    "1.  **Pega un enlace**: Proporcionas un enlace al contenido que quieres descargar.\n"
                    "2.  **Elige los ajustes**: En la pestaña 'Ajustes', puedes preconfigurar la calidad, el formato y los códecs deseados para vídeo y audio.\n"
                    "3.  **Descarga**: La aplicación toma tu enlace y tus ajustes y los traduce en un comando que 'yt-dlp' entiende. El motor 'yt-dlp' se encarga del proceso de descarga real, guardando el archivo en la carpeta que elijas.\n\n"
                    "### Para las Mentes Curiosas (Lo Técnico)\n"
                    "Esta es una aplicación puramente de Python. La interfaz de usuario está construida con la biblioteca **'CustomTkinter'**, que permite un estilo y temas modernos. La funcionalidad principal de descarga está impulsada por la legendaria biblioteca **'yt-dlp'**. Mi aplicación actúa esencialmente como un 'traductor', convirtiendo tus clics en comandos de texto para el verdadero héroe, 'yt-dlp'."
                ),
                "info_content_community": (
                    "## Un Proyecto de Código Abierto\n\n"
                    "Creo en el poder del software libre y de código abierto. Esta aplicación es de código abierto, lo que significa que cualquiera puede ver, auditar y contribuir a su código fuente. Esta transparencia garantiza que la aplicación es segura y respeta tu privacidad.\n\n"
                    "### GitHub 🐙\n"
                    "El corazón de nuestra comunidad está en GitHub. Aquí puedes:\n"
                    "- **Ver el código fuente** para saber exactamente cómo funciona la aplicación.\n"
                    "- **Informar de errores** o sugerir nuevas características creando un 'Issue'.\n"
                    "- **Contribuir** al proyecto proponiendo cambios en el código.\n"
                    "*[Enlace al repositorio de GitHub: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "Para las últimas noticias, actualizaciones y anuncios, sigue mi canal de Telegram.\n"
                    "*[Enlace al canal de Telegram: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## Tu Privacidad es Primordial\n\n"
                    "Esta aplicación está diseñada con tu privacidad como máxima prioridad. Me adhiero a una estricta **política de cero registros**.\n\n"
                    "- **Sin Recopilación de Datos**: La aplicación no recopila, almacena ni transmite ninguna información personal. No sé quién eres ni qué descargas.\n"
                    "- **Procesamiento Local**: Todas las operaciones de descarga ocurren directamente en tu ordenador. La aplicación se comunica con el sitio web de destino para obtener el contenido, pero ningún dato pasa jamás por mis servidores.\n"
                    "- **Sin Seguimiento**: No hay mecanismos de análisis o seguimiento integrados en la aplicación. Tu uso es completamente privado."
                ),
                "info_content_ethics": (
                    "## Términos de Uso y Consideraciones Éticas\n\n"
                    "Por favor, utiliza esta herramienta de manera responsable. Aunque es una utilidad potente, es importante respetar los derechos de autor y los términos de servicio de los sitios web desde los que descargas.\n\n"
                    "- **Responsabilidad del Usuario**: Tú, el usuario final, eres el único responsable de tus acciones y de cualquier contenido que descargues. El desarrollador de esta aplicación no se hace responsable de cómo uses esta herramienta.\n"
                    "- **Apoya a los Creadores**: Muchos creadores dependen de los ingresos por publicidad y las visualizaciones en las plataformas originales. Por favor, considera apoyarlos viendo su contenido en sus respectivos sitios y usando esta herramienta principalmente para copias de seguridad personales o visualización sin conexión cuando esté permitido.\n"
                    "- **Uso Justo**: Respeta siempre la propiedad intelectual de los demás. No redistribuyas material con derechos de autor sin permiso."
                ),
                "info_content_licenses": (
                    "## Motivación y Agradecimientos\n\n"
                    "Esta aplicación fue creada para proporcionar una alternativa segura, transparente y sin anuncios a muchos descargadores en línea que a menudo están llenos de anuncios intrusivos y rastreadores. Una buena herramienta debe servir al usuario, no explotarlo.\n\n"
                    "### Tecnologías Clave y Licencias 📜\n"
                    "Este proyecto no sería posible sin el increíble trabajo de la comunidad de código abierto. Los componentes clave incluyen:\n"
                    "- **yt-dlp**: El motor de descarga principal. (The Unlicense)\n"
                    "- **CustomTkinter**: Para la hermosa interfaz gráfica. (Licencia MIT)\n"
                    "- **Python**: El lenguaje de programación que lo une todo. (Licencia de la Python Software Foundation)\n\n"
                    "El código de esta aplicación también es de código abierto, distribuido bajo la **Licencia MIT**. Puedes ver la lista completa de dependencias en GitHub.\n\n"
                    "### Gratitud y Apoyo\n"
                    "Un enorme agradecimiento a todos los que contribuyen al software de código abierto. Si esta pequeña herramienta te ha sido útil, considera apoyar su desarrollo. ¡Cada pequeña ayuda cuenta!\n"
                    "*[Enlace de donación: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- German ---
            "de": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "Bereit...",
                "home_tab": "Start", "settings_tab": "Einstellungen", "maintenance_tab": "Wartung", "info_tab": "Info",
                "paste_placeholder": "Link hier einfügen...", "paste_button": "Einfügen", "select_folder_button": "Ordner auswählen",
                "download_button": "Herunterladen", "cancel_button": "Abbrechen",
                "mode_auto": "Auto", "mode_video": "Video", "mode_audio": "Audio", "mode_video_only": "Video (ohne Ton)",
                "quick_best_button": "Beste Qualität", "quick_compat_button": "Größte Kompatibilität",
                "show_sites_button": "Unterstützte Seiten anzeigen", "hide_sites_button": "Unterstützte Seiten ausblenden",
                "search_sites_placeholder": "Suche in {count} Seiten...",
                "loading_sites": "Lade Seitenliste...", "error_title": "Fehler",
                "fetch_error_label": "Ladefehler.", "clipboard_empty": "Zwischenablage ist leer.",
                "settings_video": "Video", "settings_audio": "Audio", "settings_appearance": "Erscheinungsbild", "settings_advanced": "Erweitert",
                "video_settings_title": "Video-Einstellungen", "video_quality": "Videoqualität", "quality_best": "Beste",
                "video_codec": "Bevorzugter Video-Codec", "codec_h264": "h264 (kompatibel)", "codec_av1": "av1 (modern)",
                "file_container": "Datei-Container (für Video)",
                "audio_settings_title": "Audio-Einstellungen", "audio_format": "Audioformat", "audio_bitrate": "Audio-Bitrate",
                "appearance_settings_title": "Erscheinungsbild-Einstellungen", "theme_label": "Thema", "language_label": "Sprache",
                "advanced_settings_title": "Erweitert", "show_details_switch": "Download-Details anzeigen",
                "network_mode": "Netzwerkmodus", "network_auto": "Auto", "network_ipv4": "IPv4 erzwingen", "network_ipv6": "IPv6 erzwingen",
                "downloader_engine": "Download-Engine", "downloader_builtin": "Eingebaut", "downloader_aria2c": "aria2c",
                "link_error": "Bitte fügen Sie einen Link ein.",
                "download_info_getting": "Informationen werden abgerufen...", "download_status_progress": "Wird heruntergeladen: {percentage}% ({size}) @ {speed}",
                "download_complete": "Abgeschlossen", "download_error": "Fehler", "download_cancelled": "Abgebrochen", "download_processing": "Verarbeite...",
                "maintenance_title": "Anwendungswartung",
                "update_button": "yt-dlp aktualisieren",
                "update_label": "Halten Sie die Kern-Download-Engine auf dem neuesten Stand, um Probleme mit YouTube und anderen Websites zu vermeiden.",
                "update_title": "Aktualisieren", "update_status_checking": "Suche nach Updates...",
                "update_status_success": "yt-dlp wurde erfolgreich aktualisiert!",
                "update_status_latest": "Sie haben bereits die neueste Version von yt-dlp.",
                "update_status_error": "Während des Updates ist ein Fehler aufgetreten.",
                "logs_button": "Protokollordner öffnen",
                "logs_label": "Wenn ein Problem auftritt, können die Protokolldateien in diesem Ordner bei der Fehlerbehebung helfen.",
                "logs_error_open": "Protokollordner konnte nicht geöffnet werden.",
                "clear_logs_button": "Protokolle löschen",
                "clear_logs_label": "Alle Protokolldateien löschen, um Speicher freizugeben oder die Protokolle zurückzusetzen.",
                "confirm_title": "Bestätigung",
                "confirm_clear_logs_text": "Alle Anwendungsprotokolle löschen? Dies kann nicht rückgängig gemacht werden.",
                "success_title": "Erfolg",
                "logs_cleared_success": "Alle Protokolldateien wurden gelöscht.",
                "logs_cleared_error": "Protokolldateien konnten nicht gelöscht werden.",
                "info_nav_what_is_this": "Was ist das?", "info_nav_community": "Community & Support",
                "info_nav_privacy": "Datenschutz", "info_nav_ethics": "Nutzungsbedingungen & Ethik",
                "info_nav_licenses": "Dank & Lizenzen",
                "info_content_what_is_this": (
                    "## Was ist YT-DLP GUI?\n\n"
                    "Diese App ist eine benutzerfreundliche grafische Oberfläche für das leistungsstarke Kommandozeilen-Tool **'yt-dlp'**. Sie ermöglicht es Ihnen, Videos und Audios von Tausenden von Websites einfach herunterzuladen, ohne das Terminal verwenden zu müssen. Fügen Sie einfach einen Link ein, wählen Sie Ihre Einstellungen und klicken Sie auf 'Herunterladen'!\n\n"
                    "### Wie es funktioniert\n"
                    "1.  **Link einfügen**: Sie geben einen Link zu dem Inhalt an, den Sie herunterladen möchten.\n"
                    "2.  **Einstellungen wählen**: Im Tab 'Einstellungen' können Sie die gewünschte Qualität, das Format und die Codecs für Video und Audio vorkonfigurieren.\n"
                    "3.  **Herunterladen**: Die App nimmt Ihren Link und Ihre Einstellungen und übersetzt sie in einen Befehl, den 'yt-dlp' versteht. Die 'yt-dlp'-Engine kümmert sich dann um den eigentlichen Download-Prozess und speichert die Datei in dem von Ihnen gewählten Ordner.\n\n"
                    "### Für Neugierige (Der technische Kram)\n"
                    "Dies ist eine reine Python-Anwendung. Die Benutzeroberfläche wurde mit der **'CustomTkinter'**-Bibliothek erstellt, die modernes Styling und Theming ermöglicht. Die Kernfunktionalität des Herunterladens wird von der legendären **'yt-dlp'**-Bibliothek angetrieben. Meine App fungiert im Wesentlichen als 'Übersetzer', der Ihre Klicks in Textbefehle für den wahren Helden, 'yt-dlp', umwandelt."
                ),
                "info_content_community": (
                    "## Ein Open-Source-Projekt\n\n"
                    "Ich glaube an die Kraft von offener und freier Software. Diese Anwendung ist Open Source, was bedeutet, dass jeder den Quellcode einsehen, überprüfen und dazu beitragen kann. Diese Transparenz stellt sicher, dass die App sicher ist und Ihre Privatsphäre respektiert.\n\n"
                    "### GitHub 🐙\n"
                    "Das Herz unserer Community ist auf GitHub. Hier können Sie:\n"
                    "- **Den Quellcode einsehen**, um genau zu sehen, wie die App funktioniert.\n"
                    "- **Fehler melden** oder neue Funktionen vorschlagen, indem Sie ein 'Issue' erstellen.\n"
                    "- Zum Projekt **beitragen**, indem Sie Code-Änderungen vorschlagen.\n"
                    "*[Link zum GitHub-Repository: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "Für die neuesten Nachrichten, Updates und Ankündigungen folgen Sie meinem Telegram-Kanal.\n"
                    "*[Link zum Telegram-Kanal: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## Ihre Privatsphäre ist von größter Bedeutung\n\n"
                    "Diese Anwendung wurde mit Ihrer Privatsphäre als oberster Priorität entwickelt. Ich halte mich an eine strikte **Null-Protokoll-Richtlinie**.\n\n"
                    "- **Keine Datenerfassung**: Die App sammelt, speichert oder überträgt keine persönlichen Informationen. Ich weiß nicht, wer Sie sind oder was Sie herunterladen.\n"
                    "- **Lokale Verarbeitung**: Alle Download-Vorgänge finden direkt auf Ihrem Computer statt. Die App kommuniziert mit der Ziel-Website, um Inhalte abzurufen, aber es werden niemals Daten über meine Server geleitet.\n"
                    "- **Kein Tracking**: Es sind keine Analyse- oder Tracking-Mechanismen in die Anwendung integriert. Ihre Nutzung ist vollständig privat."
                ),
                "info_content_ethics": (
                    "## Nutzungsbedingungen & Ethische Überlegungen\n\n"
                    "Bitte verwenden Sie dieses Tool verantwortungsbewusst. Obwohl es ein leistungsstarkes Dienstprogramm ist, ist es wichtig, das Urheberrecht und die Nutzungsbedingungen der Websites, von denen Sie herunterladen, zu respektieren.\n\n"
                    "- **Benutzerverantwortung**: Sie, der Endbenutzer, sind allein für Ihre Handlungen und für alle von Ihnen heruntergeladenen Inhalte verantwortlich. Der Entwickler dieser Anwendung haftet nicht dafür, wie Sie dieses Tool verwenden.\n"
                    "- **Unterstützen Sie die Ersteller**: Viele Ersteller sind auf Werbeeinnahmen und Aufrufe auf den Originalplattformen angewiesen. Bitte erwägen Sie, sie zu unterstützen, indem Sie ihre Inhalte auf ihren jeweiligen Websites ansehen und dieses Tool hauptsächlich für persönliche Sicherungen oder die Offline-Anzeige verwenden, wo dies gestattet ist.\n"
                    "- **Faire Nutzung**: Respektieren Sie immer das geistige Eigentum anderer. Verteilen Sie urheberrechtlich geschütztes Material nicht ohne Erlaubnis weiter."
                ),
                "info_content_licenses": (
                    "## Motivation & Danksagungen\n\n"
                    "Diese App wurde entwickelt, um eine sichere, transparente und werbefreie Alternative zu vielen Online-Downloadern zu bieten, die oft mit aufdringlicher Werbung und Trackern gefüllt sind. Ein gutes Werkzeug sollte dem Benutzer dienen, nicht ihn ausnutzen.\n\n"
                    "### Schlüsseltechnologien & Lizenzen 📜\n"
                    "Dieses Projekt wäre ohne die unglaubliche Arbeit der Open-Source-Community nicht möglich. Zu den Schlüsselkomponenten gehören:\n"
                    "- **yt-dlp**: Die Kern-Download-Engine. (The Unlicense)\n"
                    "- **CustomTkinter**: Für die schöne grafische Oberfläche. (MIT-Lizenz)\n"
                    "- **Python**: Die Programmiersprache, die alles zusammenhält. (Python Software Foundation License)\n\n"
                    "Der Code für diese Anwendung selbst ist ebenfalls Open Source und wird unter der **MIT-Lizenz** vertrieben. Sie können die vollständige Liste der Abhängigkeiten auf GitHub einsehen.\n\n"
                    "### Dankbarkeit & Unterstützung\n"
                    "Ein riesiges Dankeschön an alle, die zu Open-Source-Software beitragen. Wenn Ihnen dieses kleine Werkzeug geholfen hat, erwägen Sie, seine Entwicklung zu unterstützen. Jede Kleinigkeit hilft!\n"
                    "*[Spendenlink: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- French ---
            "fr": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "Prêt...",
                "home_tab": "Accueil", "settings_tab": "Paramètres", "maintenance_tab": "Maintenance", "info_tab": "Info",
                "paste_placeholder": "Collez le lien ici...", "paste_button": "Coller", "select_folder_button": "Sélectionner un dossier",
                "download_button": "Télécharger", "cancel_button": "Annuler",
                "mode_auto": "Auto", "mode_video": "Vidéo", "mode_audio": "Audio", "mode_video_only": "Vidéo (sans son)",
                "quick_best_button": "Meilleure Qualité", "quick_compat_button": "Plus Compatible",
                "show_sites_button": "Afficher les sites pris en charge", "hide_sites_button": "Masquer les sites pris en charge",
                "search_sites_placeholder": "Rechercher parmi {count} sites...",
                "loading_sites": "Chargement de la liste des sites...", "error_title": "Erreur",
                "fetch_error_label": "Erreur de chargement.", "clipboard_empty": "Le presse-papiers est vide.",
                "settings_video": "Vidéo", "settings_audio": "Audio", "settings_appearance": "Apparence", "settings_advanced": "Avancé",
                "video_settings_title": "Paramètres vidéo", "video_quality": "Qualité vidéo", "quality_best": "Meilleure",
                "video_codec": "Codec vidéo préféré", "codec_h264": "h264 (compatible)", "codec_av1": "av1 (moderne)",
                "file_container": "Conteneur de fichier (pour vidéo)",
                "audio_settings_title": "Paramètres audio", "audio_format": "Format audio", "audio_bitrate": "Débit audio",
                "appearance_settings_title": "Paramètres d'apparence", "theme_label": "Thème", "language_label": "Langue",
                "advanced_settings_title": "Avancé", "show_details_switch": "Afficher les détails du téléchargement",
                "network_mode": "Mode Réseau", "network_auto": "Auto", "network_ipv4": "Forcer IPv4", "network_ipv6": "Forcer IPv6",
                "downloader_engine": "Moteur de Téléchargement", "downloader_builtin": "Intégré", "downloader_aria2c": "aria2c",
                "link_error": "Veuillez coller un lien.",
                "download_info_getting": "Obtention des informations...", "download_status_progress": "Téléchargement : {percentage}% ({size}) @ {speed}",
                "download_complete": "Terminé", "download_error": "Erreur", "download_cancelled": "Annulé", "download_processing": "Traitement...",
                "maintenance_title": "Maintenance de l'application",
                "update_button": "Mettre à jour yt-dlp",
                "update_label": "Maintenez le moteur de téléchargement principal à jour pour éviter les problèmes avec YouTube et d'autres sites.",
                "update_title": "Mise à jour", "update_status_checking": "Recherche de mises à jour...",
                "update_status_success": "yt-dlp a été mis à jour avec succès !",
                "update_status_latest": "Vous disposez déjà de la dernière version de yt-dlp.",
                "update_status_error": "Une erreur s'est produite lors de la mise à jour.",
                "logs_button": "Ouvrir le dossier des journaux",
                "logs_label": "Si vous rencontrez un problème, les fichiers journaux de ce dossier peuvent aider au dépannage.",
                "logs_error_open": "Impossible d'ouvrir le dossier des journaux.",
                "clear_logs_button": "Effacer les journaux",
                "clear_logs_label": "Supprimer tous les fichiers journaux pour libérer de l'espace ou réinitialiser les journaux.",
                "confirm_title": "Confirmation",
                "confirm_clear_logs_text": "Supprimer tous les journaux de l'application ? Cette action est irréversible.",
                "success_title": "Succès",
                "logs_cleared_success": "Tous les fichiers journaux ont été supprimés.",
                "logs_cleared_error": "Impossible de supprimer les fichiers journaux.",
                "info_nav_what_is_this": "Qu'est-ce que c'est ?", "info_nav_community": "Communauté et Support",
                "info_nav_privacy": "Confidentialité", "info_nav_ethics": "Conditions & Éthique",
                "info_nav_licenses": "Remerciements et Licences",
                "info_content_what_is_this": (
                    "## Qu'est-ce que YT-DLP GUI ?\n\n"
                    "Cette application est une interface graphique conviviale pour le puissant outil en ligne de commande **'yt-dlp'**. Elle vous permet de télécharger facilement des vidéos et de l'audio depuis des milliers de sites web sans avoir à utiliser le terminal. Collez simplement un lien, choisissez vos paramètres et cliquez sur 'Télécharger' !\n\n"
                    "### Comment ça marche\n"
                    "1.  **Collez un lien** : Vous fournissez un lien vers le contenu que vous souhaitez télécharger.\n"
                    "2.  **Choisissez les paramètres** : Dans l'onglet 'Paramètres', vous pouvez pré-configurer la qualité, le format et les codecs souhaités pour la vidéo et l'audio.\n"
                    "3.  **Téléchargez** : L'application prend votre lien et vos paramètres et les traduit en une commande que 'yt-dlp' comprend. Le moteur 'yt-dlp' gère ensuite le processus de téléchargement réel, en enregistrant le fichier dans le dossier de votre choix.\n\n"
                    "### Pour les Esprits Curieux (Le Truc de Geek)\n"
                    "Ceci est une application purement en Python. L'interface utilisateur est construite avec la bibliothèque **'CustomTkinter'**, qui permet un style et des thèmes modernes. La fonctionnalité de téléchargement de base est alimentée par la légendaire bibliothèque **'yt-dlp'**. Mon application agit essentiellement comme un 'traducteur', convertissant vos clics en commandes textuelles pour le vrai héros, 'yt-dlp'."
                ),
                "info_content_community": (
                    "## Un Projet Open Source\n\n"
                    "Je crois en la puissance des logiciels libres et open source. Cette application est open source, ce qui signifie que n'importe qui peut voir, auditer et contribuer à son code source. Cette transparence garantit que l'application est sûre et respecte votre vie privée.\n\n"
                    "### GitHub 🐙\n"
                    "Le cœur de notre communauté se trouve sur GitHub. Ici, vous pouvez :\n"
                    "- **Voir le code source** pour savoir exactement comment fonctionne l'application.\n"
                    "- **Signaler des bugs** ou suggérer de nouvelles fonctionnalités en créant une 'Issue'.\n"
                    "- **Contribuer** au projet en proposant des modifications de code.\n"
                    "*[Lien vers le dépôt GitHub: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "Pour les dernières nouvelles, mises à jour et annonces, suivez ma chaîne Telegram.\n"
                    "*[Lien vers la chaîne Telegram: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## Votre Vie Privée est Primordiale\n\n"
                    "Cette application est conçue avec votre vie privée comme priorité absolue. J'adhère à une politique stricte de **non-conservation des journaux**.\n\n"
                    "- **Aucune Collecte de Données** : L'application ne collecte, ne stocke ni ne transmet aucune information personnelle. Je ne sais pas qui vous êtes ni ce que vous téléchargez.\n"
                    "- **Traitement Local** : Toutes les opérations de téléchargement se déroulent directement sur votre ordinateur. L'application communique avec le site web cible pour récupérer le contenu, mais aucune donnée ne transite jamais par mes serveurs.\n"
                    "- **Aucun Suivi** : Il n'y a aucun mécanisme d'analyse ou de suivi intégré à l'application. Votre utilisation est entièrement privée."
                ),
                "info_content_ethics": (
                    "## Conditions d'Utilisation & Considérations Éthiques\n\n"
                    "Veuillez utiliser cet outil de manière responsable. Bien qu'il s'agisse d'un utilitaire puissant, il est important de respecter les droits d'auteur et les conditions d'utilisation des sites web à partir desquels vous téléchargez.\n\n"
                    "- **Responsabilité de l'Utilisateur** : Vous, l'utilisateur final, êtes seul responsable de vos actions et de tout contenu que vous téléchargez. Le développeur de cette application n'est pas responsable de la manière dont vous utilisez cet outil.\n"
                    "- **Soutenez les Créateurs** : De nombreux créateurs dépendent des revenus publicitaires et des vues sur les plateformes originales. Veuillez envisager de les soutenir en regardant leur contenu sur leurs sites respectifs et en utilisant cet outil principalement pour des sauvegardes personnelles ou une visualisation hors ligne lorsque cela est autorisé.\n"
                    "- **Usage Loyal** : Respectez toujours la propriété intellectuelle des autres. Ne redistribuez pas de matériel protégé par le droit d'auteur sans permission."
                ),
                "info_content_licenses": (
                    "## Motivation & Remerciements\n\n"
                    "Cette application a été créée pour fournir une alternative sûre, transparente et sans publicité à de nombreux téléchargeurs en ligne qui sont souvent remplis de publicités intrusives et de traqueurs. Un bon outil doit servir l'utilisateur, pas l'exploiter.\n\n"
                    "### Technologies Clés & Licences 📜\n"
                    "Ce projet ne serait pas possible sans le travail incroyable de la communauté open source. Les composants clés incluent :\n"
                    "- **yt-dlp** : Le moteur de téléchargement principal. (The Unlicense)\n"
                    "- **CustomTkinter** : Pour la belle interface graphique. (Licence MIT)\n"
                    "- **Python** : Le langage de programmation qui lie le tout. (Licence de la Python Software Foundation)\n\n"
                    "Le code de cette application elle-même est également open source, distribué sous la **Licence MIT**. Vous pouvez consulter la liste complète des dépendances sur GitHub.\n\n"
                    "### Gratitude & Soutien\n"
                    "Un immense merci à tous ceux qui contribuent aux logiciels open source. Si ce petit outil vous a été utile, envisagez de soutenir son développement. Chaque petit geste compte !\n"
                    "*[Lien de don: https://boosty.to/namitskevi/donate]*"
                )
            },
            # --- Japanese ---
            "ja": {
                "app_title": f"{app_name} v{app_version}",
                "ready_status": "準備完了...",
                "home_tab": "ホーム", "settings_tab": "設定", "maintenance_tab": "メンテナンス", "info_tab": "情報",
                "paste_placeholder": "ここにリンクを貼り付けてください...", "paste_button": "貼り付け", "select_folder_button": "フォルダを選択",
                "download_button": "ダウンロード", "cancel_button": "キャンセル",
                "mode_auto": "自動", "mode_video": "ビデオ", "mode_audio": "オーディオ", "mode_video_only": "ビデオ (音声なし)",
                "quick_best_button": "最高品質", "quick_compat_button": "最大互換性",
                "show_sites_button": "対応サイトを表示", "hide_sites_button": "対応サイトを非表示",
                "search_sites_placeholder": "{count}サイトを検索...",
                "loading_sites": "サイトリストを読み込み中...", "error_title": "エラー",
                "fetch_error_label": "読み込みエラー。", "clipboard_empty": "クリップボードは空です。",
                "settings_video": "ビデオ", "settings_audio": "オーディオ", "settings_appearance": "外観", "settings_advanced": "詳細設定",
                "video_settings_title": "ビデオ設定", "video_quality": "ビデオ品質", "quality_best": "最高",
                "video_codec": "優先ビデオコーデック", "codec_h264": "h264 (互換)", "codec_av1": "av1 (最新)",
                "file_container": "ファイルコンテナ (ビデオ用)",
                "audio_settings_title": "オーディオ設定", "audio_format": "オーディオ形式", "audio_bitrate": "オーディオビットレート",
                "appearance_settings_title": "外観設定", "theme_label": "テーマ", "language_label": "言語",
                "advanced_settings_title": "詳細設定", "show_details_switch": "ダウンロード詳細を表示",
                "network_mode": "ネットワークモード", "network_auto": "自動", "network_ipv4": "IPv4を強制", "network_ipv6": "IPv6を強制",
                "downloader_engine": "ダウンロードエンジン", "downloader_builtin": "内蔵", "downloader_aria2c": "aria2c",
                "link_error": "リンクを貼り付けてください。",
                "download_info_getting": "情報を取得中...", "download_status_progress": "ダウンロード中: {percentage}% ({size}) @ {speed}",
                "download_complete": "完了", "download_error": "エラー", "download_cancelled": "キャンセルされました", "download_processing": "処理中...",
                "maintenance_title": "アプリケーションのメンテナンス",
                "update_button": "yt-dlpを更新",
                "update_label": "YouTubeや他のサイトでの問題を避けるため、コアダウンロードエンジンを最新の状態に保ってください。",
                "update_title": "更新", "update_status_checking": "更新を確認中...",
                "update_status_success": "yt-dlpは正常に更新されました！",
                "update_status_latest": "すでに最新バージョンのyt-dlpを使用しています。",
                "update_status_error": "更新中にエラーが発生しました。",
                "logs_button": "ログフォルダを開く",
                "logs_label": "問題が発生した場合、このフォルダ内のログファイルがトラブルシューティングに役立ちます。",
                "logs_error_open": "ログフォルダを開けませんでした。",
                "clear_logs_button": "ログを削除",
                "clear_logs_label": "すべてのログファイルを削除して容量を空ける、またはログをリセットします。",
                "confirm_title": "確認",
                "confirm_clear_logs_text": "アプリのログファイルをすべて削除しますか？この操作は元に戻せません。",
                "success_title": "完了",
                "logs_cleared_success": "すべてのログファイルを削除しました。",
                "logs_cleared_error": "ログファイルを削除できませんでした。",
                "info_nav_what_is_this": "これは何ですか？", "info_nav_community": "コミュニティとサポート",
                "info_nav_privacy": "プライバシー", "info_nav_ethics": "規約と倫理",
                "info_nav_licenses": "謝辞とライセンス",
                "info_content_what_is_this": (
                    "## YT-DLP GUIとは？\n\n"
                    "このアプリは、強力なコマンドラインツール**'yt-dlp'**の使いやすいグラフィカルインターフェースです。ターミナルを使わずに、何千ものウェブサイトからビデオやオーディオを簡単にダウンロードできます。リンクを貼り付け、設定を選択し、「ダウンロード」をクリックするだけです！\n\n"
                    "### 仕組み\n"
                    "1.  **リンクを貼り付け**：ダウンロードしたいコンテンツへのリンクを提供します。\n"
                    "2.  **設定を選択**：「設定」タブで、ビデオとオーディオの希望の品質、フォーマット、コーデックを事前設定できます。\n"
                    "3.  **ダウンロード**：アプリはあなたのリンクと設定を受け取り、'yt-dlp'が理解できるコマンドに変換します。その後、'yt-dlp'エンジンが実際のダウンロードプロセスを処理し、選択したフォルダにファイルを保存します。\n\n"
                    "### 好奇心旺盛な方へ (技術的なこと)\n"
                    "これは純粋なPythonアプリケーションです。ユーザーインターフェースは**'CustomTkinter'**ライブラリで構築されており、モダンなスタイリングとテーマ設定が可能です。中核となるダウンロード機能は、伝説的な**'yt-dlp'**ライブラリによって提供されています。私のアプリは、本質的に、あなたのクリックを真のヒーローである'yt-dlp'のためのテキストコマンドに変換する「翻訳者」として機能します。"
                ),
                "info_content_community": (
                    "## オープンソースプロジェクト\n\n"
                    "私はオープンで自由なソフトウェアの力を信じています。このアプリケーションはオープンソースであり、誰でもそのソースコードを閲覧、監査、貢献することができます。この透明性は、アプリが安全であり、あなたのプライバシーを尊重することを保証します。\n\n"
                    "### GitHub 🐙\n"
                    "私たちのコミュニティの中心はGitHubにあります。ここでは、次のことができます：\n"
                    "- **ソースコードを表示**して、アプリがどのように機能するかを正確に確認する。\n"
                    "- 「Issue」を作成して**バグを報告**したり、新機能を提案したりする。\n"
                    "- コードの変更を提案してプロジェクトに**貢献**する。\n"
                    "*[GitHubリポジトリへのリンク: https://github.com/Nikitzima/YT-DLP-GUI]*\n\n"
                    "### Telegram ✈️\n"
                    "最新のニュース、アップデート、お知らせについては、私のTelegramチャンネルをフォローしてください。\n"
                    "*[Telegramチャンネルへのリンク: https://t.me/YT_DLP_GUI]*"
                ),
                "info_content_privacy": (
                    "## あなたのプライバシーは最優先事項です\n\n"
                    "このアプリケーションは、あなたのプライバシーを最優先に設計されています。私は厳格な**ゼロログポリシー**を遵守しています。\n\n"
                    "- **データ収集なし**：アプリは個人情報を収集、保存、送信しません。私はあなたが誰であるか、何をダウンロードしたかを知りません。\n"
                    "- **ローカル処理**：すべてのダウンロード操作は、お使いのコンピュータで直接行われます。アプリはターゲットのウェブサイトと通信してコンテンツを取得しますが、私のサーバーを介してデータが渡されることはありません。\n"
                    "- **追跡なし**：アプリケーションには分析や追跡のメカニズムは組み込まれていません。あなたの使用は完全にプライベートです。"
                ),
                "info_content_ethics": (
                    "## 利用規約と倫理的配慮\n\n"
                    "このツールは責任を持って使用してください。これは強力なユーティリティですが、著作権とダウンロード元のウェブサイトの利用規約を尊重することが重要です。\n\n"
                    "- **ユーザーの責任**：あなた、エンドユーザーは、あなたの行動とダウンロードしたコンテンツに対して単独で責任を負います。このアプリケーションの開発者は、あなたがこのツールをどのように使用するかについて責任を負いません。\n"
                    "- **クリエイターをサポート**：多くのクリエイターは、元のプラットフォームでの広告収入と視聴回数に依存しています。彼らのコンテンツをそれぞれのサイトで視聴し、許可されている場合は主に個人用のバックアップやオフラインでの視聴にこのツールを使用することで、彼らをサポートすることを検討してください。\n"
                    "- **公正な使用**：常に他者の知的財産を尊重してください。許可なく著作権で保護された素材を再配布しないでください。"
                ),
                "info_content_licenses": (
                    "## 動機と謝辞\n\n"
                    "このアプリは、しばしば押し付けがましい広告やトラッカーで満たされている多くのオンラインダウンローダーに代わる、安全で透明性のある広告なしの代替手段を提供するために作成されました。良いツールはユーザーに奉仕するべきであり、ユーザーを搾取するべきではありません。\n\n"
                    "### 主要技術とライセンス 📜\n"
                    "このプロジェクトは、オープンソースコミュニティの素晴らしい仕事なしには不可能でした。主要なコンポーネントは次のとおりです：\n"
                    "- **yt-dlp**：コアダウンロードエンジン。(The Unlicense)\n"
                    "- **CustomTkinter**：美しいグラフィカルインターフェースのため。(MITライセンス)\n"
                    "- **Python**：すべてを結びつけるプログラミング言語。(Python Software Foundation License)\n\n"
                    "このアプリケーション自体のコードもオープンソースであり、**MITライセンス**の下で配布されています。依存関係の完全なリストはGitHubで確認できます。\n\n"
                    "### 感謝とサポート\n"
                    "オープンソースソフトウェアに貢献してくださるすべての方に心から感謝します。この小さなツールが役に立った場合は、その開発をサポートすることを検討してください。どんな小さな支援も助けになります！\n"
                    "*[寄付リンク: https://boosty.to/namitskevi/donate]*"
                )
            }
        }

    def get_language_name(self, code):
        """Возвращает полное имя языка по его коду."""
        return next((name for name, c in self.language_map.items() if c == code), None)

    def set_language(self, lang_name):
        """Устанавливает текущий язык по его полному имени."""
        code = self.language_map.get(lang_name)
        if code:
            self.current_language = code
            return True
        return False

    def get(self, key, **kwargs):
        """Получает переведенную строку по ключу для текущего языка."""
        lang_dict = self.translations.get(self.current_language, self.translations.get("en", {}))
        return lang_dict.get(key, key).format(**kwargs)

