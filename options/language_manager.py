class LanguageManager:
    def __init__(self):
        self.current_language = "pl"

    def set_language(self, language):
        self.current_language = language

    def get_language(self):
        return self.current_language
