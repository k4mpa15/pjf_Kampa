import json


class Translator:
    def __init__(self, language_manager):
        self.language_manager = language_manager
        self.translations = self.load_translations()

    def load_translations(self):
        with open("options/translations.json", "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations

    def translate(self, key):
        self.language = self.language_manager.get_language()
        translation = self.translations.get(key, {}).get(self.language, key)
        return translation
