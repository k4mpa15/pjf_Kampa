from datetime import datetime

from options.translator import Translator


class EquationHistory:
    def __init__(self, language_manager):
        self.language_manager = language_manager
        self.history_file_path = "eq_history.txt"
        self.translator = Translator(self.language_manager)

    def add_equation(self, equation, result):
        time = datetime.now()
        formated_time = time.strftime("%d/%m/%Y, %H:%M:%S")
        with open(self.history_file_path, "a") as f:
            f.write(f"{equation} > > > {result},   [{formated_time}]\n")

    def get_history(self):
        with open(self.history_file_path, "r") as f:
            history_content = f.read()
        return history_content
