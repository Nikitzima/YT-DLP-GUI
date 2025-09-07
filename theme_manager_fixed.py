import os
import json

class ThemeManager:
    """
    РЈРїСЂР°РІР»СЏРµС‚ СЃРѕР·РґР°РЅРёРµРј Рё Р·Р°РіСЂСѓР·РєРѕР№ РєР°СЃС‚РѕРјРЅС‹С… С‚РµРј РґР»СЏ РїСЂРёР»РѕР¶РµРЅРёСЏ.
    Р­С‚РѕС‚ РєР»Р°СЃСЃ РіР°СЂР°РЅС‚РёСЂСѓРµС‚, С‡С‚Рѕ РІСЃРµ С„Р°Р№Р»С‹ С‚РµРј СЏРІР»СЏСЋС‚СЃСЏ РїРѕР»РЅС‹РјРё Рё РґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё РїСЂРё РєР°Р¶РґРѕРј Р·Р°РїСѓСЃРєРµ.
    """
    def __init__(self):
        self.themes = {
            "Classic": {
                "type": "built-in",
                "name": "blue",
                "appearance": "dark"
            },
            "codex": {
                "type": "custom",
                "appearance": "dark",
                "colors": {
                    "fg_color": "#0F1117",                   # deep neutral background
                    "button_color": "#3B82F6",                # vibrant azure-500
                    "button_hover_color": "#2563EB",          # azure-600
                    "progressbar_color": "#3B82F6",          # match primary for consistency
                    "entry_fg_color": "#161B22",              # slightly lighter surface
                    "segmented_button_selected_color": "#3B82F6",
                    "segmented_button_selected_hover_color": "#2563EB",
                }
            },
            "Youtube": {
                "type": "custom",
                "appearance": "dark",
                "colors": {
                    "fg_color": "#282828",
                    "button_color": "#ff0000",
                    "button_hover_color": "#c00000",
                    "progressbar_color": "#ff0000",
                    "entry_fg_color": "#3d3d3d",
                    "segmented_button_selected_color": "#ff0000",
                    "segmented_button_selected_hover_color": "#c00000",
                }
            },
            "Spotify": {
                "type": "custom",
                "appearance": "dark",
                "colors": {
                    "fg_color": "#191414",
                    "button_color": "#1DB954",
                    "button_hover_color": "#1AA34A",
                    "progressbar_color": "#1DB954",
                    "entry_fg_color": "#282828",
                    "segmented_button_selected_color": "#1DB954",
                    "segmented_button_selected_hover_color": "#1AA34A",
                }
            },
            "Instagram": {
                "type": "custom",
                "appearance": "light",
                "colors": {
                    "fg_color": "#fafafa",
                    "button_color": "#833AB4",
                    "button_hover_color": "#6a2e94",
                    "progressbar_color": "#FD1D1D",
                    "entry_fg_color": "#efefef",
                    "segmented_button_selected_color": "#833AB4",
                    "segmented_button_selected_hover_color": "#6a2e94",
                }
            }
        }
        
        self._create_theme_files()

    def _create_theme_files(self):
        """
        РџСЂРёРЅСѓРґРёС‚РµР»СЊРЅРѕ РїРµСЂРµР·Р°РїРёСЃС‹РІР°РµС‚ С„Р°Р№Р»С‹ С‚РµРј РїСЂРё РєР°Р¶РґРѕРј Р·Р°РїСѓСЃРєРµ, С‡С‚РѕР±С‹ СѓР±РµРґРёС‚СЊСЃСЏ, С‡С‚Рѕ РѕРЅРё РїРѕР»РЅС‹Рµ Рё РґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹Рµ,
        РїСЂРµРґРѕС‚РІСЂР°С‰Р°СЏ Р»СЋР±С‹Рµ РїСЂРѕР±Р»РµРјС‹ KeyError РёР·-Р·Р° РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р°С‚СЂРёР±СѓС‚РѕРІ С‚РµРјС‹.
        """
        # --- РР—РњР•РќР•РќРР• Р—Р”Р•РЎР¬: РЎРћР—Р”РђР•Рњ РџРђРџРљРЈ Р РЇР”РћРњ РЎРћ РЎРљР РРџРўРћРњ ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        theme_dir = os.path.join(script_dir, "themes")
        # ----------------------------------------------------

        if not os.path.exists(theme_dir):
            os.makedirs(theme_dir)

        for name, theme_data in self.themes.items():
            if theme_data["type"] == "custom":
                path = os.path.join(theme_dir, f"{name.lower()}.json")
                
                if theme_data["appearance"] == "dark":
                    text_color = "gray90"
                    text_color_disabled = "gray40"
                    placeholder_text_color = "gray50"
                    border_color = "gray28"
                    font_family = "Segoe UI"
                else: # light
                    text_color = "gray10"
                    text_color_disabled = "gray60"
                    placeholder_text_color = "gray50"
                    border_color = "gray65"
                    font_family = "Segoe UI"
                
                theme_json = {
                    "CTk": {"fg_color": theme_data["colors"]["fg_color"]},
                    "CTkToplevel": {"fg_color": theme_data["colors"]["fg_color"]},
                    "CTkFont": {
                        "family": font_family, "size": 13, "weight": "normal",
                        "slant": "roman", "underline": 0, "overstrike": 0
                    },
                    "CTkFrame": {
                        "fg_color": theme_data["colors"]["fg_color"],
                        "top_fg_color": theme_data["colors"]["fg_color"],
                        "border_color": border_color, "corner_radius": 8, "border_width": 0
                    },
                    "CTkTabView": {
                        "fg_color": theme_data["colors"]["fg_color"],
                        "border_color": border_color,
                        "border_width": 2,
                        "text_color": text_color,
                        "segmented_button_fg_color": theme_data["colors"]["fg_color"],
                        "segmented_button_selected_color": theme_data["colors"]["button_color"],
                        "segmented_button_selected_hover_color": theme_data["colors"]["button_hover_color"],
                        "segmented_button_unselected_color": theme_data["colors"]["fg_color"],
                        "segmented_button_unselected_hover_color": border_color
                    },
                    "CTkLabel": {
                        "fg_color": "transparent", "text_color": text_color, "corner_radius": 0
                    },
                    "CTkButton": {
                        "fg_color": theme_data["colors"]["button_color"],
                        "hover_color": theme_data["colors"]["button_hover_color"],
                        "border_color": border_color, "text_color": "#ffffff", "corner_radius": 6,
                        "border_width": 0, "text_color_disabled": text_color_disabled
                    },
                    "CTkEntry": { 
                        "fg_color": theme_data["colors"]["entry_fg_color"],
                        "border_color": border_color, "text_color": text_color,
                        "placeholder_text_color": placeholder_text_color,
                        "corner_radius": 6, "border_width": 2
                    },
                    "CTkOptionMenu": {
                        "fg_color": theme_data["colors"]["button_color"],
                        "button_color": theme_data["colors"]["button_color"],
                        "button_hover_color": theme_data["colors"]["button_hover_color"],
                        "text_color": "#ffffff", "corner_radius": 6,
                        "text_color_disabled": text_color_disabled
                    },
                    "DropdownMenu": {
                        "fg_color": theme_data["colors"]["button_color"],
                        "hover_color": theme_data["colors"]["button_hover_color"],
                        "text_color": "#ffffff",
                        "corner_radius": 6,
                        "border_width": 1,
                        "border_color": border_color
                    },
                    "CTkProgressBar": {
                        "progress_color": theme_data["colors"]["progressbar_color"],
                        "fg_color": theme_data["colors"]["entry_fg_color"],
                        "border_color": border_color,
                        "corner_radius": 100,
                        "border_width": 0
                    },
                    "CTkSegmentedButton": {
                        "fg_color": theme_data["colors"]["entry_fg_color"],
                        "selected_color": theme_data["colors"]["segmented_button_selected_color"],
                        "selected_hover_color": theme_data["colors"]["segmented_button_selected_hover_color"],
                        "unselected_color": theme_data["colors"]["entry_fg_color"],
                        "unselected_hover_color": border_color,
                        "text_color": text_color,
                        "text_color_disabled": text_color_disabled,
                        "corner_radius": 6, "border_width": 2
                    },
                    "CTkSwitch": {
                        "fg_color": theme_data["colors"]["entry_fg_color"],
                        "progress_color": theme_data["colors"]["button_color"],
                        "button_color": "gray50",
                        "button_hover_color": "gray65",
                        "border_color": border_color,
                        "text_color": text_color,
                        "text_color_disabled": text_color_disabled,
                        "corner_radius": 1000,
                        "border_width": 2,
                        "button_length": 0
                    },
                    "CTkTextbox": {
                        "fg_color": theme_data["colors"]["entry_fg_color"],
                        "text_color": text_color,
                        "border_color": border_color,
                        "scrollbar_button_color": theme_data["colors"]["button_color"],
                        "scrollbar_button_hover_color": theme_data["colors"]["button_hover_color"],
                        "corner_radius": 6, "border_width": 2
                    },
                    "CTkScrollbar": {
                        "fg_color": "transparent",
                        "button_color": theme_data["colors"]["button_color"],
                        "button_hover_color": theme_data["colors"]["button_hover_color"],
                        "corner_radius": 100,
                        "border_spacing": 4
                    }
                }
                
                with open(path, "w", encoding='utf-8') as f:
                    json.dump(theme_json, f, indent=4)
                
                self.themes[name]["path"] = path

    def get_theme_data(self, name):
        return self.themes.get(name)
